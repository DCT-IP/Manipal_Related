import numpy as np

def _validate_portfolio_values(
        portfolio_val: np.ndarray,
) -> np.ndarray:
    """Validation of simulated portfolio path"""
    val = np.asarray(portfolio_val, dtype=float)
    if val.ndim != 2 or any(size == 0 for size in val.shape):
        raise ValueError(
            "portfolio_values must be non empty 2d array"
            "with shape (n_simulation, n_steps)."
        )

    if not np.all(np.isfinite(val)):
        raise ValueError("portfolio values must be finite")

    if np.any(val <= 0):
        raise ValueError("portfolio values must be positive.")
    return val

def calc_var_cvar(
        portfolio_val: np.ndarray,
        confidence_level: float=0.95,
) -> dict[str,float]:
    """"calculation of emperical value and expected shortfall
    
        Loss is defined as Portfolio_initial - terminal value
        Positive result shows loss, negative shows gains
        
        CVaR uses AVG of worst (1-confidence region)
        fraction of outcomes, including fractional weightign when needed
        
        Returns
        ------
        dict with:(
        var: Value at Risk, in portfolio currency units.
        cvar: Conditional Value at Risk / Expected Shortfal
    """

    values = _validate_portfolio_values(portfolio_val)
    if not np.isfinite(confidence_level) or not (
        0.0 < confidence_level < 1
    ):
        raise ValueError("confidence_level must be between 0 and 1")
    initial_val = values[:,0]
    terminal_val = values[:,-1]
    losses = initial_val - terminal_val
    var = float(np.quantile(losses, confidence_level))
    sorted_losses = np.sort(losses)[::-1]
    tail_count = (1.0 - confidence_level) * len(sorted_losses)
    full_count = int(np.floor(tail_count))
    fractional_count = tail_count - full_count
    tail_sum = float(np.sum(sorted_losses[:full_count]))
    if fractional_count > 0.0:
        tail_sum += fractional_count * float(sorted_losses[full_count])
    cvar = tail_sum / tail_count
    return {
        "var": var,
        "cvar": float(cvar),
    }

def calculate_probability_of_loss(
        portfolio_values: np.ndarray,
) -> float :
    values = _validate_portfolio_values(portfolio_values)
    initial_values = values[:, 0]
    terminal_values = values[:, -1]
    return float(np.mean(terminal_values < initial_values))

def calculate_expected_return(
    portfolio_values: np.ndarray,
) -> float:
    """
    Calculate mean cumulative terminal return across simulations.
    Returns a decimal: 0.08 represents an 8% expected return.
    """
    values = _validate_portfolio_values(portfolio_values)
    initial_values = values[:, 0]
    terminal_values = values[:, -1]
    terminal_returns = terminal_values / initial_values - 1.0
    return float(np.mean(terminal_returns))


def calculate_risk_metrics(
    portfolio_values: np.ndarray,
    confidence_levels: tuple[float, ...] = (0.95, 0.99),
) -> dict[str, float]:
    """
    Calculate a summary of terminal portfolio risk and return.

    VaR and CVaR are returned separately for each confidence level.
    """
    values = _validate_portfolio_values(portfolio_values)

    if not confidence_levels:
        raise ValueError("At least one confidence level is required.")

    metrics = {
        "initial_value": float(np.mean(values[:, 0])),
        "expected_terminal_value": float(np.mean(values[:, -1])),
        "expected_return": calculate_expected_return(values),
        "probability_of_loss": calculate_probability_of_loss(values),
    }

    for confidence in confidence_levels:
        if not np.isfinite(confidence) or not 0.0 < confidence < 1.0:
            raise ValueError(
                "Every confidence level must be between 0 and 1."
            )
        risk = calc_var_cvar(values, confidence)
        label = f"{confidence * 100:g}"
        metrics[f"var_{label}"] = risk["var"]
        metrics[f"cvar_{label}"] = risk["cvar"]
    return metrics
