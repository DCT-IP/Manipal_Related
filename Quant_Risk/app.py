
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from config import (
    INITIAL_CAPITAL,
    DEFAULT_SIMULATIONS,
    DEFAULT_TIME_HORIZON,
    DEFAULT_STEPS,
    DEFAULT_RANDOM_SEED,
    DEFAULT_CONFIDENCE_LEVELS,
    DEFAULT_ASSETS,
    NUMERICAL_TOLERANCE,
)

from simulation import simulate_gbm
from risk_metrics import calculate_risk_metrics
from portfolio import calculate_portfolio_value
from risk_analysis import (
    run_volatility_sensitivity,
    run_terminal_stress_tests,
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="QUANT//RISK",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("QUANT//RISK")
st.caption("Monte Carlo Portfolio Risk & Scenario Analysis Engine")

st.warning(
    "Illustrative simulations only. Results depend on model assumptions "
    "and are not investment advice."
)


# --------------------------------------------------
# Sidebar: simulation settings
# --------------------------------------------------
st.sidebar.header("Simulation Settings")

n_simulations = st.sidebar.slider(
    "Number of simulations",
    min_value=100,
    max_value=50_000,
    value=int(DEFAULT_SIMULATIONS),
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
    value=int(DEFAULT_STEPS),
)

seed = st.sidebar.number_input(
    "Random seed",
    min_value=0,
    max_value=2_147_483_647,
    value=int(DEFAULT_RANDOM_SEED),
    step=1,
)


# --------------------------------------------------
# Sidebar: portfolio settings
# --------------------------------------------------
st.sidebar.header("Portfolio")

initial_capital = st.sidebar.number_input(
    "Initial capital ($)",
    min_value=100.0,
    max_value=100_000_000.0,
    value=float(INITIAL_CAPITAL),
    step=10_000.0,
)

target_wealth = st.sidebar.number_input(
    "Target wealth goal ($)",
    min_value=100.0,
    max_value=1_000_000_000.0,
    value=float(INITIAL_CAPITAL) * 1.5,
    step=10_000.0,
)

st.sidebar.caption("Set the percentage allocation for each asset.")

weight_a = st.sidebar.slider("Asset A (%)", 0, 100, 40)
weight_b = st.sidebar.slider("Asset B (%)", 0, 100, 35)
weight_c = st.sidebar.slider("Asset C (%)", 0, 100, 25)

weight_percentages = np.array(
    [weight_a, weight_b, weight_c],
    dtype=float,
)

weight_total = float(weight_percentages.sum())

if not np.isclose(
    weight_total,
    100.0,
    atol=NUMERICAL_TOLERANCE,
):
    st.sidebar.error(
        f"Allocations currently total {weight_total:.0f}%. "
        "Adjust them to total 100%."
    )
    st.stop()

weights = weight_percentages / 100.0


# --------------------------------------------------
# Sidebar: asset assumptions
# --------------------------------------------------
st.sidebar.header("Asset Assumptions")

default_names = list(DEFAULT_ASSETS)

# This dashboard currently models exactly three assets.
if len(default_names) != 3:
    default_names = ["Asset A", "Asset B", "Asset C"]

default_drifts = [0.08, 0.10, 0.06]
default_vols = [0.15, 0.25, 0.10]
default_prices = [100.0, 100.0, 100.0]

asset_names = []
annual_drifts = []
annual_volatilities = []
initial_prices = []

with st.sidebar.expander(
    "Advanced Asset Parameters",
    expanded=False,
):
    for i in range(3):
        name = st.text_input(
            f"Name {i + 1}",
            value=default_names[i],
            key=f"asset_name_{i}",
        )
        asset_names.append(name.strip())

        drift = st.number_input(
            f"{name or f'Asset {i + 1}'} Annual Drift",
            min_value=-1.0,
            max_value=1.0,
            value=default_drifts[i],
            step=0.01,
            format="%.4f",
            key=f"asset_drift_{i}",
        )
        annual_drifts.append(drift)

        volatility = st.number_input(
            f"{name or f'Asset {i + 1}'} Annual Volatility",
            min_value=0.0,
            max_value=3.0,
            value=default_vols[i],
            step=0.01,
            format="%.4f",
            key=f"asset_volatility_{i}",
        )
        annual_volatilities.append(volatility)

        price = st.number_input(
            f"{name or f'Asset {i + 1}'} Initial Price",
            min_value=0.01,
            max_value=1_000_000.0,
            value=default_prices[i],
            step=10.0,
            format="%.2f",
            key=f"asset_price_{i}",
        )
        initial_prices.append(price)

    st.caption(
        "Drift represents annualized expected growth under GBM. "
        "Volatility is annualized standard deviation and must be "
        "non-negative."
    )

annual_drifts = np.asarray(annual_drifts, dtype=float)
annual_volatilities = np.asarray(annual_volatilities, dtype=float)
initial_prices = np.asarray(initial_prices, dtype=float)

if any(not name for name in asset_names):
    st.sidebar.error("Asset names cannot be empty.")
    st.stop()

if len(set(asset_names)) != len(asset_names):
    st.sidebar.error("Asset names must be unique.")
    st.stop()


# --------------------------------------------------
# Correlation assumptions
# --------------------------------------------------
correlation = np.array([
    [1.00, 0.30, 0.20],
    [0.30, 1.00, 0.15],
    [0.20, 0.15, 1.00],
])

st.sidebar.caption(
    "Drift, volatility, initial prices and correlation are illustrative "
    "assumptions, not estimates derived from historical market data. "
    "The correlation matrix is currently fixed."
)


# --------------------------------------------------
# Simulation execution
# --------------------------------------------------
if st.button("Run Monte Carlo Simulation", type="primary"):
    st.session_state["run_simulation"] = True

if not st.session_state.get("run_simulation", False):
    st.info(
        "Configure your assumptions in the sidebar, "
        "then run the simulation."
    )
    st.stop()


try:
    price_paths = simulate_gbm(
        initial_prices=initial_prices,
        drift=annual_drifts,
        volatility=annual_volatilities,
        correlation=correlation,
        time_horizon=float(time_horizon),
        steps=int(round(steps * time_horizon)),
        n_simulations=int(n_simulations),
        seed=int(seed),
    )

    portfolio_values = calculate_portfolio_value(
        price_paths,
        weights,
        initial_capital=float(initial_capital),
    )

    metrics = calculate_risk_metrics(
        portfolio_values,
        confidence_levels=DEFAULT_CONFIDENCE_LEVELS,
    )

    terminal_values = portfolio_values[:, -1]

    probability_of_success = float(
        np.mean(terminal_values >= target_wealth)
    )

except (ValueError, np.linalg.LinAlgError) as exc:
    st.error(f"Simulation failed: {exc}")
    st.stop()


# --------------------------------------------------
# Dashboard tabs
# --------------------------------------------------
(
    tab_overview,
    tab_paths,
    tab_dist,
    tab_alloc,
    tab_data,
    tab_sensitivity,
    tab_stress,
) = st.tabs([
    "Overview & Metrics",
    "Trajectories",
    "Terminal Distribution",
    "Allocation",
    "Data Explorer",
    "Sensitivity Analysis",
    "Stress Testing",
])


# --------------------------------------------------
# Tab 1: risk and return overview
# --------------------------------------------------
with tab_overview:
    st.subheader("Risk & Return Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Expected Terminal Value",
        f"${metrics['expected_terminal_value']:,.2f}",
    )

    c2.metric(
        "Expected Return",
        f"{metrics['expected_return']:.2%}",
    )

    c3.metric(
        "Probability of Loss",
        f"{metrics['probability_of_loss']:.2%}",
    )

    c4.metric(
        f"Probability of Target (${target_wealth:,.0f})",
        f"{probability_of_success:.2%}",
    )

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "VaR (95%)",
        f"${metrics['var_95']:,.2f}",
    )

    c6.metric(
        "CVaR / Expected Shortfall (95%)",
        f"${metrics['cvar_95']:,.2f}",
    )

    c7.metric(
        "VaR (99%)",
        f"${metrics['var_99']:,.2f}",
    )

    st.caption(
        "VaR and CVaR are terminal loss amounts relative to initial "
        "capital. Negative values indicate gains under the selected "
        "loss convention."
    )

    st.subheader("Simulation Configuration")

    config_df = pd.DataFrame({
        "Parameter": [
            "Simulations",
            "Time horizon (years)",
            "Steps per year",
            "Total time steps",
            "Random seed",
            "Initial capital",
            "Target wealth",
        ],
        "Value": [
            n_simulations,
            time_horizon,
            steps,
            portfolio_values.shape[1] - 1,
            seed,
            initial_capital,
            target_wealth,
        ],
    })

    st.dataframe(
        config_df,
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# Tab 2: simulated portfolio paths
# --------------------------------------------------
with tab_paths:
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
        labels={
            "Year": "Time (years)",
            "Portfolio Value": "Portfolio value ($)",
        },
    )

    fig_paths.update_layout(showlegend=False)

    st.plotly_chart(
        fig_paths,
        use_container_width=True,
    )


# --------------------------------------------------
# Tab 3: terminal distribution
# --------------------------------------------------
with tab_dist:
    st.subheader("Terminal Portfolio Value Distribution")

    fig_distribution = px.histogram(
        x=terminal_values,
        nbins=60,
        title="Distribution of Simulated Terminal Values",
        labels={
            "x": "Terminal portfolio value ($)",
            "count": "Scenarios",
        },
    )

    fig_distribution.add_vline(
        x=initial_capital,
        line_dash="dash",
        line_color="orange",
        annotation_text="Initial capital",
    )

    fig_distribution.add_vline(
        x=target_wealth,
        line_dash="dash",
        line_color="green",
        annotation_text="Target wealth",
    )

    fig_distribution.update_layout(
        xaxis_title="Terminal portfolio value ($)",
        yaxis_title="Number of scenarios",
    )

    st.plotly_chart(
        fig_distribution,
        use_container_width=True,
    )

    st.caption(
        "The target success probability is estimated from the fraction "
        "of simulated terminal values that meet or exceed the target. "
        "Its accuracy depends on the number of simulations and model "
        "assumptions."
    )


# --------------------------------------------------
# Tab 4: portfolio allocation
# --------------------------------------------------
with tab_alloc:
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

    st.plotly_chart(
        fig_allocation,
        use_container_width=True,
    )

    st.dataframe(
        pd.DataFrame({
            "Asset": asset_names,
            "Weight (%)": weight_percentages,
            "Initial Asset Price": initial_prices,
            "Annual Drift": annual_drifts,
            "Annual Volatility": annual_volatilities,
        }),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# Tab 5: metrics and CSV export
# --------------------------------------------------
with tab_data:
    st.subheader("Complete Risk Metrics & Export")

    metric_df = pd.DataFrame([
        {"Metric": name, "Value": value}
        for name, value in metrics.items()
    ])

    st.dataframe(
        metric_df,
        use_container_width=True,
        hide_index=True,
    )

    csv_data = metric_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Metrics as CSV",
        data=csv_data,
        file_name="quant_risk_metrics.csv",
        mime="text/csv",
    )

    st.subheader("Terminal Simulation Data")

    terminal_df = pd.DataFrame({
        "Simulation": np.arange(1, len(terminal_values) + 1),
        "Terminal Value": terminal_values,
        "Terminal Return (%)": (
            terminal_values / initial_capital - 1.0
        ) * 100.0,
        "Loss": initial_capital - terminal_values,
        "Reached Target": terminal_values >= target_wealth,
    })

    st.dataframe(
        terminal_df.head(100),
        use_container_width=True,
        hide_index=True,
    )

    terminal_csv = terminal_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Terminal Simulation Data as CSV",
        data=terminal_csv,
        file_name="quant_risk_terminal_scenarios.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# Tab 6: sensitivity analysis
# --------------------------------------------------
with tab_sensitivity:
    st.subheader("Volatility Sensitivity Analysis")

    st.write(
        "Examine how portfolio risk changes when every asset's "
        "annual volatility is scaled while drift, allocation, "
        "correlation, and the random seed remain fixed."
    )

    st.caption(
        "The baseline multiplier of 1.0 uses the original volatility "
        "assumptions. These are controlled model experiments, not forecasts."
    )

    if st.button(
        "Run Sensitivity Analysis",
        key="run_sensitivity",
        type="primary",
    ):
        try:
            sensitivity_df = run_volatility_sensitivity(
                initial_prices=initial_prices,
                drift=annual_drifts,
                volatility=annual_volatilities,
                correlation=correlation,
                weights=weights,
                initial_capital=float(initial_capital),
                time_horizon=float(time_horizon),
                steps=int(round(steps * time_horizon)),
                n_simulations=int(n_simulations),
                seed=int(seed),
                volatility_multipliers=(0.75, 1.0, 1.25, 1.50),
                confidence_levels=tuple(DEFAULT_CONFIDENCE_LEVELS),
                target_wealth=float(target_wealth),
            )

            st.session_state["sensitivity_df"] = sensitivity_df

        except (ValueError, np.linalg.LinAlgError) as exc:
            st.error(f"Sensitivity analysis failed: {exc}")

    sensitivity_df = st.session_state.get("sensitivity_df")

    if sensitivity_df is not None:
        st.dataframe(
            sensitivity_df,
            use_container_width=True,
            hide_index=True,
        )

        fig_sensitivity = px.line(
            sensitivity_df,
            x="Volatility Multiplier",
            y=["VaR 95% ($)", "CVaR 95% ($)"],
            markers=True,
            title="Tail Risk vs. Volatility",
        )

        fig_sensitivity.update_layout(
            xaxis_title="Volatility multiplier",
            yaxis_title="Terminal loss ($)",
        )

        st.plotly_chart(
            fig_sensitivity,
            use_container_width=True,
        )

        fig_target = px.line(
            sensitivity_df,
            x="Volatility Multiplier",
            y="Probability of Target (%)",
            markers=True,
            title="Target Success Probability vs. Volatility",
        )

        st.plotly_chart(
            fig_target,
            use_container_width=True,
        )

        st.download_button(
            "Download Sensitivity Results",
            data=sensitivity_df.to_csv(index=False).encode("utf-8"),
            file_name="quant_risk_sensitivity.csv",
            mime="text/csv",
            key="download_sensitivity",
        )
    else:
        st.info("Run the analysis to generate sensitivity results.")


# --------------------------------------------------
# Tab 7: stress testing
# --------------------------------------------------
with tab_stress:
    st.subheader("Terminal Price Shock Analysis")

    st.write(
        "Apply instantaneous shocks to terminal asset prices in the "
        "simulated scenarios while keeping the original holdings fixed."
    )

    st.caption(
        "These shocks are illustrative. They are not probabilities, "
        "market forecasts, or dynamically simulated crash paths."
    )

    stress_scenarios = {
        "Broad market decline": np.array([-0.20, -0.20, -0.20]),
        "Severe market decline": np.array([-0.35, -0.35, -0.35]),
        "High-volatility asset shock": np.array([0.0, -0.30, 0.0]),
        "Defensive asset decline": np.array([0.0, 0.0, -0.15]),
        "Mixed stress": np.array([-0.25, -0.35, -0.10]),
    }

    if st.button(
        "Run Stress Tests",
        key="run_stress_tests",
        type="primary",
    ):
        try:
            stress_df = run_terminal_stress_tests(
                price_paths=price_paths,
                weights=weights,
                initial_capital=float(initial_capital),
                scenarios=stress_scenarios,
                confidence_levels=tuple(DEFAULT_CONFIDENCE_LEVELS),
            )

            st.session_state["stress_df"] = stress_df

        except (ValueError, np.linalg.LinAlgError) as exc:
            st.error(f"Stress testing failed: {exc}")

    stress_df = st.session_state.get("stress_df")

    if stress_df is not None:
        st.dataframe(
            stress_df,
            use_container_width=True,
            hide_index=True,
        )

        fig_stress = px.bar(
            stress_df,
            x="Scenario",
            y="Mean Change vs Baseline ($)",
            title="Mean Terminal Value Change Under Stress",
        )

        fig_stress.update_layout(
            xaxis_title="Stress scenario",
            yaxis_title="Change in terminal portfolio value ($)",
        )

        st.plotly_chart(
            fig_stress,
            use_container_width=True,
        )

        st.download_button(
            "Download Stress Test Results",
            data=stress_df.to_csv(index=False).encode("utf-8"),
            file_name="quant_risk_stress_tests.csv",
            mime="text/csv",
            key="download_stress",
        )
    else:
        st.info("Run the stress tests to generate scenario results.")


# --------------------------------------------------
# Model limitations
# --------------------------------------------------
st.caption(
    "Model limitations: GBM assumes constant drift and volatility "
    "and uses a fixed correlation matrix. Real market returns may "
    "exhibit fat tails, volatility clustering, jumps and changing "
    "correlations. Outputs are scenario estimates, not forecasts."
)
