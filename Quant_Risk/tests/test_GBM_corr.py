import numpy as np
from simulation import simulate_gbm

def test_simulated_returns_match_target_correlation():
    initial_prices = np.array([100.0, 120.0, 80.0])
    drift = np.array([0.08, 0.10, 0.06])
    volatility = np.array([0.20, 0.25, 0.15])
    correlation = np.array([
        [1.0, 0.7, 0.2],
        [0.7, 1.0, 0.4],
        [0.2, 0.4, 1.0],
    ])

    paths = simulate_gbm(
        initial_prices=initial_prices,
        drift=drift,
        volatility=volatility,
        correlation=correlation,
        time_horizon=1.0,
        steps=252,
        n_simulations=20_000,
        seed=42,
    )

    log_returns = np.diff(
        np.log(paths),
        axis=1,
    )
    log_returns = log_returns.reshape(-1, 3)

    simulated_correlation = np.corrcoef(
        log_returns,
        rowvar=False,
    )
    np.testing.assert_allclose(
        simulated_correlation,
        correlation,
        atol=0.01,
    )

    """
    This validation is to prove cholesky based correlation works
    each asset's simulated returns have the intended relationships with others
    corr is preserved across the generated time stpes
    """