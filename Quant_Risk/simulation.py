import numpy as np
def simulate_gbm(
    initial_prices: np.ndarray,
    drift: np.ndarray,
    volatility: np.ndarray,
    correlation: np.ndarray,
    time_horizon: float = 1.0,
    steps: int = 252,
    n_simulations: int = 10_000,
    seed: int | None = 42,
) -> np.ndarray:
    """
    Simulate correlated Geometric Brownian Motion price paths.

    Parameters
    ----------
    initial_prices : array of shape (n_assets,)
        Initial asset prices.
    drift : array of shape (n_assets,)
        Annualized expected returns.
    volatility : array of shape (n_assets,)
        Annualized volatilities.
    correlation : array of shape (n_assets, n_assets)
        Positive-definite correlation matrix.
    time_horizon : float
        Simulation horizon in years.
    steps : int
        Number of time steps.
    n_simulations : int
        Number of independent simulated paths.
    seed : int or None
        Random seed for reproducibility.

        The usage of the GBM for as single asset gives us two theoretical benchmarks:
                                    E[St] = S(0)*e^(myu*T)
                                    Var(St) = S(0)^2*e^(2myuT) * ((e^(sigma^2)*T) - 1)
    Returns
    -------
    np.ndarray
        Price paths with shape
        (n_simulations, steps + 1, n_assets).
    """
    initial_prices = np.asarray(initial_prices, dtype=float)
    drift = np.asarray(drift, dtype=float)
    volatility = np.asarray(volatility, dtype=float)
    correlation = np.asarray(correlation, dtype=float)

    if initial_prices.ndim != 1 or initial_prices.size == 0:
        raise ValueError("initial_prices must be a non-empty 1D array.")

    n_assets = initial_prices.size

    if drift.shape != (n_assets,) or volatility.shape != (n_assets,):
        raise ValueError("drift and volatility must match the asset count.")

    if correlation.shape != (n_assets, n_assets):
        raise ValueError("correlation must be an n_assets x n_assets matrix.")

    if not all(
        np.all(np.isfinite(array))
        for array in (initial_prices, drift, volatility, correlation)
    ):
        raise ValueError("All inputs must contain finite values.")

    if np.any(initial_prices <= 0):
        raise ValueError("Initial prices must be positive.")

    if np.any(volatility < 0):
        raise ValueError("Volatility cannot be negative.")

    if not np.isfinite(time_horizon) or time_horizon <= 0:
        raise ValueError("time_horizon must be positive and finite.")

    if not isinstance(steps, (int, np.integer)) or isinstance(steps, bool) or steps < 1:
        raise ValueError("steps must be a positive integer.")

    if (
        not isinstance(n_simulations, (int, np.integer))
        or isinstance(n_simulations, bool)
        or n_simulations < 1
    ):
        raise ValueError("n_simulations must be a positive integer.")

    if not np.allclose(correlation, correlation.T, atol=1e-10):
        raise ValueError("correlation must be symmetric.")

    if not np.allclose(np.diag(correlation), 1.0, atol=1e-10):
        raise ValueError("Correlation matrix diagonal must equal 1.")

    if np.any(np.abs(correlation) > 1.0 + 1e-10):
        raise ValueError("Correlation values must lie between -1 and 1.")

    try:
        cholesky = np.linalg.cholesky(correlation)
    except np.linalg.LinAlgError as exc:
        raise ValueError(
            "Correlation matrix must be positive definite."
        ) from exc

    rng = np.random.default_rng(seed)

    dt = time_horizon / steps
    prices = np.empty(
        (n_simulations, steps + 1, n_assets),
        dtype=float,
    )
    prices[:, 0, :] = initial_prices

    independent_shocks = rng.standard_normal(
        (n_simulations, steps, n_assets)
    )

    correlated_shocks = independent_shocks @ cholesky.T

    increments = (
        (drift - 0.5 * volatility**2) * dt
        + volatility * np.sqrt(dt) * correlated_shocks
    )

    prices[:, 1:, :] = (
        initial_prices[None, None, :]
        * np.exp(np.cumsum(increments, axis=1))
    )

    return prices