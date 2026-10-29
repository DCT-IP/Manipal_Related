import numpy as np
import pytest
from risk_analysis import (
    run_volatility_sensitivity,
    run_terminal_stress_tests,
)

@pytest.fixture
def setup_data():
    return {
        "initial_prices": np.array([100.0, 120.0]),
        "drift": np.array([0.06, 0.08]),
        "volatility": np.array([0.15, 0.20]),
        "correlation": np.array([
            [1.0, 0.25],
            [0.25, 1.0],
        ]),
        "weights": np.array([0.60, 0.40]),
        "initial_capital": 100_000.0,
        "time_horizon": 1.0,
        "steps": 20,
        "n_simulations": 200,
        "seed": 42,
    }


def test_volatility_sensitivity_returns_expected_scenarios(setup_data):
    result = run_volatility_sensitivity(
        **setup_data,
        volatility_multipliers=(0.75, 1.0, 1.25),
        target_wealth=120_000.0,
    )
    assert len(result) == 3
    assert result["Volatility Multiplier"].tolist() == [
        0.75, 1.0, 1.25
    ]
    assert np.all(np.isfinite(
        result.select_dtypes(include=[np.number]).to_numpy()
    ))
    assert "VaR 95% ($)" in result.columns
    assert "CVaR 95% ($)" in result.columns
    assert "Probability of Target (%)" in result.columns


def test_baseline_sensitivity_matches_direct_simulation(setup_data):
    from simulation import simulate_gbm
    from portfolio import calculate_portfolio_value
    from risk_metrics import calculate_risk_metrics
    result = run_volatility_sensitivity(
        **setup_data,
        volatility_multipliers=(1.0,),
    )
    paths = simulate_gbm(
        initial_prices=setup_data["initial_prices"],
        drift=setup_data["drift"],
        volatility=setup_data["volatility"],
        correlation=setup_data["correlation"],
        time_horizon=setup_data["time_horizon"],
        steps=setup_data["steps"],
        n_simulations=setup_data["n_simulations"],
        seed=setup_data["seed"],
    )
    values = calculate_portfolio_value(
        paths,
        setup_data["weights"],
        setup_data["initial_capital"],
    )
    direct = calculate_risk_metrics(values)
    assert result.iloc[0]["VaR 95% ($)"] == pytest.approx(
        direct["var_95"]
    )
    assert result.iloc[0]["CVaR 95% ($)"] == pytest.approx(
        direct["cvar_95"]
    )


def test_stress_test_baseline_and_market_decline(setup_data):
    from simulation import simulate_gbm
    paths = simulate_gbm(
        initial_prices=setup_data["initial_prices"],
        drift=setup_data["drift"],
        volatility=setup_data["volatility"],
        correlation=setup_data["correlation"],
        time_horizon=setup_data["time_horizon"],
        steps=setup_data["steps"],
        n_simulations=setup_data["n_simulations"],
        seed=setup_data["seed"],
    )
    result = run_terminal_stress_tests(
        price_paths=paths,
        weights=setup_data["weights"],
        initial_capital=setup_data["initial_capital"],
        scenarios={
            "Market decline": np.array([-0.20, -0.10]),
            "Asset A shock": np.array([-0.30, 0.0]),
        },
    )
    assert set(result["Scenario"]) == {
        "Baseline",
        "Market decline",
        "Asset A shock",
    }
    baseline = result[result["Scenario"] == "Baseline"].iloc[0]
    market_decline = result[
        result["Scenario"] == "Market decline"
    ].iloc[0]
    assert baseline["Mean Change vs Baseline ($)"] == pytest.approx(0.0)
    assert market_decline["Mean Change vs Baseline ($)"] < 0.0


def test_invalid_stress_shock_rejected(setup_data):
    from simulation import simulate_gbm
    paths = simulate_gbm(
        initial_prices=setup_data["initial_prices"],
        drift=setup_data["drift"],
        volatility=setup_data["volatility"],
        correlation=setup_data["correlation"],
        time_horizon=setup_data["time_horizon"],
        steps=setup_data["steps"],
        n_simulations=setup_data["n_simulations"],
        seed=setup_data["seed"],
    )
    with pytest.raises(ValueError):
        run_terminal_stress_tests(
            price_paths=paths,
            weights=setup_data["weights"],
            initial_capital=setup_data["initial_capital"],
            scenarios={
                "Invalid": np.array([-1.1, 0.0]),
            },
        )


def test_invalid_volatility_multiplier_rejected(setup_data):
    with pytest.raises(ValueError):
        run_volatility_sensitivity(
            **setup_data,
            volatility_multipliers=(-1.0,),
        )


def test_stress_mean_change_matches_expected_value_difference(setup_data):
    from simulation import simulate_gbm

    paths = simulate_gbm(
        initial_prices=setup_data["initial_prices"],
        drift=setup_data["drift"],
        volatility=setup_data["volatility"],
        correlation=setup_data["correlation"],
        time_horizon=setup_data["time_horizon"],
        steps=setup_data["steps"],
        n_simulations=setup_data["n_simulations"],
        seed=setup_data["seed"],
    )

    result = run_terminal_stress_tests(
        price_paths=paths,
        weights=setup_data["weights"],
        initial_capital=setup_data["initial_capital"],
        scenarios={"Market decline": np.array([-0.20, -0.20])},
    )

    baseline = result.loc[result["Scenario"] == "Baseline"].iloc[0]
    stressed = result.loc[
        result["Scenario"] == "Market decline"
    ].iloc[0]

    expected_difference = (
        stressed["Expected Terminal Value ($)"]
        - baseline["Expected Terminal Value ($)"]
    )

    assert stressed["Mean Change vs Baseline ($)"] == pytest.approx(
        expected_difference
    )
