import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from config import(
    INITIAL_CAPITAL,
    DEFAULT_SIMULATIONS,
    DEFAULT_TIME_HORIZON,
    DEFAULT_STEPS,
    DEFAULT_RANDOM_SEED,
    DEFAULT_CONFIDENCE_LEVELS,
    DEFAULT_ASSETS,
    NUMERICAL_TOLERANCE
)

from simulation import simulate_gbm
from risk_metrics import calculate_risk_metrics
from portfolio import calculate_portfolio_value

st.set_page_config(
    page_title="QUANT//RISK",
    layout="wide",
)
st.title("QUANT//RISK")
st.caption("Monte Carlo Portfolio Risk & Scenario Analysis Engine")
st.warning(
    "Illustrative simulations only. Results depend on model assumptions "
    "and are not investment advice."
)

st.sidebar.header("Simulation Settings")

n_simulations = st.sidebar.slider(
    "Number of simulations",
    min_value=100,
    max_value=50_000,
    value=DEFAULT_SIMULATIONS,
    step=100,
)

time_horizon = st.sidebar.slider(
    "Time horizon (years)",
    min_value=0.25,
    max_value=5.0,
    value=float(DEFAULT_TIME_HORIZON),
    step=0.25,
)

steps = st.sidebar.select_slider(
    "Steps per year",
    options=[12, 52, 252],
    value=DEFAULT_STEPS,
)

seed = st.sidebar.number_input(
    "Random seed",
    min_value=0,
    max_value=2_147_483_647,
    value=DEFAULT_RANDOM_SEED,
    step=1,
)

st.sidebar.header("Portfolio")

initial_capital = st.sidebar.number_input(
    "Initial capital",
    min_value=100.0,
    max_value=100_000_000.0,
    value=float(INITIAL_CAPITAL),
    step=10_000.0,
)

asset_names = ["Asset A", "Asset B", "Asset C"]

st.sidebar.caption("Set the percentage allocation for each asset.")

weight_a = st.sidebar.slider("Asset A (%)", 0, 100, 40)
weight_b = st.sidebar.slider("Asset B (%)", 0, 100, 35)
weight_c = st.sidebar.slider("Asset C (%)", 0, 100, 25)

weight_percentages = np.array([weight_a, weight_b, weight_c], dtype=float)
weight_total = float(weight_percentages.sum())

if not np.isclose(weight_total, 100.0):
    st.sidebar.error(
        f"Allocations currently total {weight_total:.0f}%. "
        "Adjust them to total 100%."
    )
    st.stop()

weights = weight_percentages / 100.0

st.sidebar.header("Asset Assumptions")

initial_prices = np.array([100.0, 100.0, 100.0])
annual_drifts = np.array([0.08, 0.10, 0.06])
annual_volatilities = np.array([0.15, 0.25, 0.10])

correlation = np.array([
    [1.00, 0.30, 0.20],
    [0.30, 1.00, 0.15],
    [0.20, 0.15, 1.00],
])

st.sidebar.caption(
    "Drift, volatility and correlation are illustrative assumptions, "
    "not estimates derived from historical market data."
)

if st.button("Run Monte Carlo Simulation", type="primary"):
    st.session_state["run_simulation"] = True

if not st.session_state.get("run_simulation", False):
    st.info("Configure the assumptions, then run the simulation.")
    st.stop()

try:
    price_paths = simulate_gbm(
        initial_prices=initial_prices,
        drift=annual_drifts,
        volatility=annual_volatilities,
        correlation=correlation,
        time_horizon=time_horizon,
        steps=int(round(steps * time_horizon)),
        n_simulations=int(n_simulations),
        seed=int(seed),
    )

    portfolio_values = calculate_portfolio_value(
        price_paths,
        weights,
        initial_capital=initial_capital,
    )

    metrics = calculate_risk_metrics(
        portfolio_values,
        confidence_levels=DEFAULT_CONFIDENCE_LEVELS,
    )

except (ValueError, np.linalg.LinAlgError) as exc:
    st.error(f"Simulation failed: {exc}")
    st.stop()

st.subheader("Risk Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Expected terminal value",
    f"${metrics['expected_terminal_value']:,.2f}",
)

c2.metric(
    "Expected return",
    f"{metrics['expected_return']:.2%}",
)

c3.metric(
    "Probability of loss",
    f"{metrics['probability_of_loss']:.2%}",
)

c4.metric(
    "VaR (95%)",
    f"${metrics['var_95']:,.2f}",
)

c5, c6 = st.columns(2)

c5.metric(
    "CVaR / Expected Shortfall (95%)",
    f"${metrics['cvar_95']:,.2f}",
)

c6.metric(
    "VaR (99%)",
    f"${metrics['var_99']:,.2f}",
)

st.caption(
    "VaR and CVaR are terminal loss amounts relative to initial capital. "
    "Negative values indicate gains under the selected loss convention."
)

st.subheader("Simulated Portfolio Paths")

n_display = min(100, portfolio_values.shape[0])
time_axis = np.linspace(
    0.0,
    time_horizon,
    portfolio_values.shape[1],
)

path_df = pd.DataFrame({
    "Year": np.tile(time_axis, n_display),
    "Portfolio Value": portfolio_values[:n_display].reshape(-1),
    "Simulation": np.repeat(
        [f"Path {i + 1}" for i in range(n_display)],
        portfolio_values.shape[1],
    ),
})

fig_paths = px.line(
    path_df,
    x="Year",
    y="Portfolio Value",
    color="Simulation",
    title="Sample of Simulated Portfolio Trajectories",
    labels={"Year": "Time (years)", "Portfolio Value": "Portfolio value ($)"},
)

fig_paths.update_layout(showlegend=False)
st.plotly_chart(fig_paths, use_container_width=True)

st.subheader("Terminal Portfolio Value Distribution")

terminal_values = portfolio_values[:, -1]

fig_distribution = px.histogram(
    x=terminal_values,
    nbins=60,
    title="Distribution of Simulated Terminal Values",
    labels={"x": "Terminal portfolio value ($)", "count": "Scenarios"},
)

fig_distribution.add_vline(
    x=initial_capital,
    line_dash="dash",
    annotation_text="Initial capital",
)

fig_distribution.update_layout(
    xaxis_title="Terminal portfolio value ($)",
    yaxis_title="Number of scenarios",
)

st.plotly_chart(fig_distribution, use_container_width=True)
st.subheader("Portfolio Allocation")

allocation_df = pd.DataFrame({
    "Asset": asset_names,
    "Weight": weights,
})

fig_allocation = px.pie(
    allocation_df,
    names="Asset",
    values="Weight",
    hole=0.45,
    title="Capital Allocation",
)

st.plotly_chart(fig_allocation, use_container_width=True)
st.subheader("Complete Risk Metrics")

metric_df = pd.DataFrame(
    [{"Metric": name, "Value": value} for name, value in metrics.items()]
)
st.dataframe(metric_df, use_container_width=True, hide_index=True)
st.caption(
    "GBM assumes constant drift and volatility and uses the supplied "
    "correlation matrix. Real market returns may exhibit fat tails, "
    "volatility clustering and changing correlations."
)
