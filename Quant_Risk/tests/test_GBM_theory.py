import numpy as np
from simulation import simulate_gbm

def test_gbm_terminal_mean_matches_theory():
    initial_price = 100.0
    drift = 0.08
    volatility = 0.20
    time_horizon = 1.0
    n_simulations = 50_000
    paths = simulate_gbm(
        initial_prices=np.array([initial_price]),
        drift=np.array([drift]),
        volatility=np.array([volatility]),
        correlation=np.array([[1.0]]),
        time_horizon=time_horizon,
        steps=1,
        n_simulations=n_simulations,
        seed=42,
    )
    terminal_prices = paths[:, -1, 0]
    theoretical_mean = initial_price * np.exp(
        drift * time_horizon
    )
    theoretical_variance = (
        initial_price**2
        * np.exp(2 * drift * time_horizon)
        * (np.exp(volatility**2 * time_horizon) - 1)
    )
    standard_error = np.sqrt(
        theoretical_variance / n_simulations
    )
    assert abs(
        terminal_prices.mean() - theoretical_mean
    ) < 5 * standard_error


def test_gbm_terminal_variance_matches_theory():
    initial_price = 100.0
    drift = 0.08
    volatility = 0.20
    time_horizon = 1.0
    n_simulations = 50_000
    paths = simulate_gbm(
        initial_prices=np.array([initial_price]),
        drift=np.array([drift]),
        volatility=np.array([volatility]),
        correlation=np.array([[1.0]]),
        time_horizon=time_horizon,
        steps=1,
        n_simulations=n_simulations,
        seed=123,
    )
    terminal_prices = paths[:, -1, 0]
    theoretical_variance = (
        initial_price**2
        * np.exp(2 * drift * time_horizon)
        * (np.exp(volatility**2 * time_horizon) - 1)
    )
    sample_variance = np.var(
        terminal_prices,
        ddof=1,
    )
    relative_error = abs(
        sample_variance - theoretical_variance
    ) / theoretical_variance
    assert relative_error < 0.03

"""
Since the tests passed, that checks the avg sim terminal price is close to the theoretical expectedprice
The var test checks for dispersion of simulated prices being close to the theoretical var
These tolerances account for finite-sample Monte Carlo var; do not require exact equality
"""