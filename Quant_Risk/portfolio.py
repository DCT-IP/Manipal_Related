import numpy as np

def _validate_weights(weights: np.ndarray, n_assets: int) -> np.ndarray: 
    weights = np.asarray(weights, dtype=float)
    if weights.shape != (n_assets,):
        raise ValueError("weights must contain one value per asset.\n")

    if not np.all(np.isfinite(weights)):
        raise ValueError("Weights must be finite!!\n")

    if np.any(weights < 0):
        raise ValueError("Weights must be positive or 0!\n")

    total = weights.sum()
    if not np.isclose(total, 1.0, atol=1e-8):
        raise ValueError("Values should sum to 1!\n")
    return weights/total

def calculate_portfolio_value(
        price_path: np.ndarray,
        weights: np.ndarray,
        initial_capital: float = 100_000.0,
) -> np.ndarray:
    """
    Calculate portfolio values from simulated asset-price paths.

    Parameters
    ----------
    price_paths : ndarray, shape (n_simulations, n_steps, n_assets)
        Simulated asset prices.
    weights : ndarray, shape (n_assets,)
        Portfolio allocation weights, summing to 1.
    initial_capital : float
        Initial portfolio investment.

    Returns
    -------
    ndarray, shape (n_simulations, n_steps)
        Portfolio value at every simulated time step.
    """
    price_path = np.asarray(price_path, dtype=float)
    if price_path.ndim != 3:
        raise ValueError("price_path must be of the shape (n_simulations, n_steps, n_assets)")
    if any(size == 0 for size in price_path.shape):
        raise ValueError("price_paths cannot have empty dimensions.")
    if not np.all(np.isfinite(price_path)):
        raise ValueError("Price Path should be finite")
    if np.any(price_path <= 0):
        raise ValueError("Asset Prices should be positive.")
    n_assets = price_path.shape[2]
    weights = _validate_weights(weights, n_assets)

    if not np.isfinite(initial_capital) or initial_capital <= 0:
        raise ValueError("initial_capital should be positive and finite\n")
    
    initial_prices = price_path[:, 0, :]

    shares = (
        initial_capital * weights[None, :]
    ) / initial_prices

    portfolio_val = np.sum(
        price_path * shares[:, None, :], 
        axis=2
    )
    return portfolio_val

def calc_portfolio_return(
        portfolio_values: np.ndarray,
) -> np.ndarray:
    """
    Calculate cumulative portfolio returns relative to initial value.

    Returns an array with shape (n_simulations, n_steps).
    """
    portfolio_values = np.asarray(portfolio_values, dtype=float)
    if portfolio_values.ndim != 2 or any(
        size == 0 for size in portfolio_values.shape
    ):
        raise ValueError("portfolio_values must be non empty 2d array")
    if not np.all(np.isfinite(portfolio_values)):
        raise ValueError("portfolio_values must be finite")
    if np.any(portfolio_values <= 0):
        raise ValueError("portfolio_values must be positive")

    initial_val = portfolio_values[:, 0:1]
    return portfolio_values / initial_val - 1.0


def compare_portfolios(
    price_paths: np.ndarray,
    allocations: dict[str, np.ndarray],
    initial_capital: float = 100_000.0,
) -> dict[str, np.ndarray]:
    """
    Compare portfolios using identical simulated price paths.

    Returns a mapping of portfolio names to their simulated values.
    """
    if not allocations:
        raise ValueError("At least one portfolio allocation is required.")
    return {
        name: calculate_portfolio_value( 
            price_paths,
            weights,
            initial_capital,
        )
        for name, weights in allocations.items()
    }