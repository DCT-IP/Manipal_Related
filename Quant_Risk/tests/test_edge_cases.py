import numpy as np
import pytest
from simulation import simulate_gbm

def test_zero_volatility_produces_deterministic_paths():
    paths = simulate_gbm(
        initial_prices=np.array([100.0]),
        drift=np.array([0.08]),
        volatility=np.array([0.0]),
        correlation=np.array([[1.0]]),
        time_horizon=1.0,
        steps=252,
        n_simulations=100,
        seed=42,
    )
    expected_terminal = 100.0 * np.exp(0.08)
    np.testing.assert_allclose(
        paths[:, -1, 0],
        expected_terminal,
        rtol=1e-10,
    )


def test_zero_drift_and_zero_volatility_keep_price_constant():
    paths = simulate_gbm(
        initial_prices=np.array([100.0]),
        drift=np.array([0.0]),
        volatility=np.array([0.0]),
        correlation=np.array([[1.0]]),
        time_horizon=1.0,
        steps=252,
        n_simulations=100,
        seed=42,
    )

    np.testing.assert_allclose(
        paths,
        100.0,
        rtol=1e-10,
    )


def test_simulation_is_reproducible():
    kwargs = {
        "initial_prices": np.array([100.0, 120.0]),
        "drift": np.array([0.08, 0.10]),
        "volatility": np.array([0.20, 0.25]),
        "correlation": np.array([
            [1.0, 0.5],
            [0.5, 1.0],
        ]),
        "time_horizon": 1.0,
        "steps": 252,
        "n_simulations": 100,
        "seed": 42,
    }

    first = simulate_gbm(**kwargs)
    second = simulate_gbm(**kwargs)
    np.testing.assert_array_equal(first, second)


@pytest.mark.parametrize(
    "invalid_value",
    [0.0, -1.0, -100.0],
)
def test_non_positive_initial_prices_are_rejected(invalid_value):
    with pytest.raises((ValueError, AssertionError)):
        simulate_gbm(
            initial_prices=np.array([invalid_value]),
            drift=np.array([0.08]),
            volatility=np.array([0.20]),
            correlation=np.array([[1.0]]),
            time_horizon=1.0,
            steps=252,
            n_simulations=100,
            seed=42,
        )
"""
THIS TEST: assumes the sim will explicitly reject non positive inital price(done in our handling of values for portfolio)
Test	                            Expected behaviour
Zero volatility	             Deterministic exponential growth
Zero drift and volatility	      Constant prices
Same seed	                      Identical paths
Invalid initial prices	          Clear validation error
"""