import numpy as np
from simulation import simulate_gbm

def test_monte_carlo_error_decreases_with_more_simulations():
    initial_price = 100.0
    drift = 0.08
    volatility = 0.20
    time_horizon = 1.0
    simulation_counts = [1_000, 10_000, 100_000]
    errors = []

    theoretical_mean = initial_price * np.exp(
        drift * time_horizon
    )

    for count in simulation_counts:
        paths = simulate_gbm(
            initial_prices=np.array([initial_price]),
            drift=np.array([drift]),
            volatility=np.array([volatility]),
            correlation=np.array([[1.0]]),
            time_horizon=time_horizon,
            steps=1,
            n_simulations=count,
            seed=42,
        )

        estimated_mean = paths[:, -1, 0].mean()
        errors.append(
            abs(estimated_mean - theoretical_mean)
        )
    assert errors[2] < errors[0]

"""
The monte carlo error approx follows:-
SE = std dev of simulated quantity/sqrt(Number of independent sims), but 
this test checks that the error decreases for a fixed seed and these particular sample sizes. 
It is a useful regression test, not a mathematical guarantee that every larger run will be closer to the theoretical value.
"""