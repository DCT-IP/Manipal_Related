import numpy as np
from simulation import simulate_gbm
from portfolio import calculate_portfolio_value
from risk_metrics import calculate_risk_metrics


def test_full_simulation_pipeline():
    initial_prices = np.array([100.0, 150.0, 80.0])
    drift = np.array([0.07, 0.09, 0.05])
    volatility = np.array([0.15, 0.22, 0.10])
    correlation = np.array([
        [1.00, 0.30, 0.20],
        [0.30, 1.00, 0.15],
        [0.20, 0.15, 1.00],
    ])

    weights = np.array([0.40, 0.35, 0.25])
    price_paths = simulate_gbm(
        initial_prices=initial_prices,
        drift=drift,
        volatility=volatility,
        correlation=correlation,
        time_horizon=1.0,
        steps=20,
        n_simulations=500,
        seed=123,
    )
    assert price_paths.shape == (500, 21, 3)
    assert np.all(np.isfinite(price_paths))
    assert np.all(price_paths > 0)
    np.testing.assert_allclose(
        price_paths[:, 0, :],
        np.tile(initial_prices, (500, 1)),
    )
    portfolio_values = calculate_portfolio_value(
        price_paths,
        weights,
        initial_capital=100_000.0,
    )
    assert portfolio_values.shape == (500, 21)
    np.testing.assert_allclose(
        portfolio_values[:, 0],
        100_000.0,
    )
    metrics = calculate_risk_metrics(
        portfolio_values,
        confidence_levels=(0.95, 0.99),
    )
    expected_keys = {
        "initial_value",
        "expected_terminal_value",
        "expected_return",
        "probability_of_loss",
        "var_95",
        "cvar_95",
        "var_99",
        "cvar_99",
    }
    assert expected_keys.issubset(metrics.keys())
    assert all(np.isfinite(value) for value in metrics.values())
    assert 0.0 <= metrics["probability_of_loss"] <= 1.0


def test_simulation_is_reproducible():
    arguments = {
        "initial_prices": np.array([100.0, 120.0]),
        "drift": np.array([0.05, 0.08]),
        "volatility": np.array([0.15, 0.20]),
        "correlation": np.array([
            [1.0, 0.25],
            [0.25, 1.0],
        ]),
        "time_horizon": 1.0,
        "steps": 10,
        "n_simulations": 100,
        "seed": 42,
    }
    first = simulate_gbm(**arguments)
    second = simulate_gbm(**arguments)
    np.testing.assert_array_equal(first, second)
