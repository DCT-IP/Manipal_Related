import numpy as np
import pandas as pd
from simulation import simulate_gbm
from portfolio import calculate_portfolio_value
from risk_metrics import calculate_risk_metrics


def run_volatility_sensitivity(
    initial_prices: np.ndarray,
    drift: np.ndarray,
    volatility: np.ndarray,
    correlation: np.ndarray,
    weights: np.ndarray,
    initial_capital: float,
    time_horizon: float,
    steps: int,
    n_simulations: int,
    seed: int,
    volatility_multipliers: tuple[float, ...] = (
        0.75, 1.0, 1.25, 1.50
    ),
    confidence_levels: tuple[float, ...] = (0.95, 0.99),
    target_wealth: float | None = None,
) -> pd.DataFrame:
    """
    Measure how volatility changes affect simulated portfolio risk.
    All scenarios use the same seed to improve comparability.
    A multiplier of 1.0 represents the baseline volatility.
    """
    initial_prices = np.asarray(initial_prices, dtype=float)
    drift = np.asarray(drift, dtype=float)
    volatility = np.asarray(volatility, dtype=float)
    weights = np.asarray(weights, dtype=float)

    if initial_prices.ndim != 1 or initial_prices.size == 0:
        raise ValueError("initial_prices must be a non-empty 1D array.")
    n_assets = initial_prices.size
    if drift.shape != (n_assets,) or volatility.shape != (n_assets,):
        raise ValueError("drift and volatility must match the asset count.")
    if weights.shape != (n_assets,):
        raise ValueError("weights must match the asset count.")
    if not np.all(np.isfinite(initial_prices)) or np.any(initial_prices <= 0):
        raise ValueError("Initial prices must be positive and finite.")
    if not np.all(np.isfinite(drift)):
        raise ValueError("drift must contain finite values.")
    if not np.all(np.isfinite(volatility)) or np.any(volatility < 0):
        raise ValueError("volatility must be finite and non-negative.")
    if not np.all(np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError("weights must be finite and non-negative.")
    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("weights must sum to 1.")
    if not np.isfinite(initial_capital) or initial_capital <= 0:
        raise ValueError("initial_capital must be positive and finite.")
    if not np.isfinite(time_horizon) or time_horizon <= 0:
        raise ValueError("time_horizon must be positive and finite.")
    if not isinstance(steps, (int, np.integer)) or steps < 1:
        raise ValueError("steps must be a positive integer.")
    if not isinstance(n_simulations, (int, np.integer)) or n_simulations < 1:
        raise ValueError("n_simulations must be a positive integer.")
    if not volatility_multipliers:
        raise ValueError("At least one volatility multiplier is required.")
    if any(
        not np.isfinite(multiplier) or multiplier < 0
        for multiplier in volatility_multipliers
    ):
        raise ValueError("Volatility multipliers must be finite and non-negative.")
    if target_wealth is not None and (
        not np.isfinite(target_wealth) or target_wealth <= 0
    ):
        raise ValueError("target_wealth must be positive and finite.")

    rows = []

    for multiplier in volatility_multipliers:
        paths = simulate_gbm(
            initial_prices=initial_prices,
            drift=drift,
            volatility=volatility * multiplier,
            correlation=correlation,
            time_horizon=time_horizon,
            steps=steps,
            n_simulations=n_simulations,
            seed=seed,
        )
        values = calculate_portfolio_value(
            paths,
            weights,
            initial_capital=initial_capital,
        )
        metrics = calculate_risk_metrics(
            values,
            confidence_levels=confidence_levels,
        )
        row = {
            "Volatility Multiplier": multiplier,
            "Expected Return (%)": metrics["expected_return"] * 100,
            "Probability of Loss (%)": metrics["probability_of_loss"] * 100,
            "VaR 95% ($)": metrics["var_95"],
            "CVaR 95% ($)": metrics["cvar_95"],
            "VaR 99% ($)": metrics["var_99"],
            "Expected Terminal Value ($)": metrics["expected_terminal_value"],
        }
        if target_wealth is not None:
            row["Probability of Target (%)"] = (
                np.mean(values[:, -1] >= target_wealth) * 100
            )
        rows.append(row)
    return pd.DataFrame(rows)


def run_terminal_stress_tests(
    price_paths: np.ndarray,
    weights: np.ndarray,
    initial_capital: float,
    scenarios: dict[str, np.ndarray],
    confidence_levels: tuple[float, ...] = (0.95, 0.99),
) -> pd.DataFrame:
    """
    Apply instantaneous asset-price shocks to simulated terminal prices.
    Each scenario maps a name to one shock per asset.
    A shock of -0.20 represents a 20% price decline.
    The initial holdings are held fixed. Shocks are applied to terminal
    asset prices, not to the starting prices or portfolio weights.
    """
    price_paths = np.asarray(price_paths, dtype=float)
    weights = np.asarray(weights, dtype=float)
    if price_paths.ndim != 3 or any(size == 0 for size in price_paths.shape):
        raise ValueError("price_paths must be a non-empty 3D array.")
    if not np.all(np.isfinite(price_paths)) or np.any(price_paths <= 0):
        raise ValueError("price_paths must contain positive finite prices.")
    n_assets = price_paths.shape[2]
    if weights.shape != (n_assets,):
        raise ValueError("weights must match the asset count.")
    if not np.all(np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError("weights must be finite and non-negative.")
    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("weights must sum to 1.")
    if not np.isfinite(initial_capital) or initial_capital <= 0:
        raise ValueError("initial_capital must be positive and finite.")
    if not scenarios:
        raise ValueError("At least one stress scenario is required.")
    
    initial_prices = price_paths[:, 0, :]
    terminal_prices = price_paths[:, -1, :]
    shares = (
        initial_capital * weights[None, :]
    ) / initial_prices
    baseline_terminal_values = np.sum(
        terminal_prices * shares,
        axis=1,
    )

    scenario_rows = []
    all_scenarios = {
        "Baseline": np.zeros(n_assets),
        **scenarios,
    }

    for name, shocks in all_scenarios.items():
        shocks = np.asarray(shocks, dtype=float)
        if shocks.shape != (n_assets,):
            raise ValueError(
                f"Scenario '{name}' must contain one shock per asset."
            )
        if not np.all(np.isfinite(shocks)) or np.any(shocks < -1.0):
            raise ValueError(
                f"Scenario '{name}' shocks must be finite and at least -1."
            )
        shocked_terminal_prices = terminal_prices * (1.0 + shocks)
        shocked_terminal_values = np.sum(
            shocked_terminal_prices * shares,
            axis=1,
        )
        metric_paths = np.column_stack((
            np.full(len(shocked_terminal_values), initial_capital),
            shocked_terminal_values,
        ))
        metrics = calculate_risk_metrics(
            metric_paths,
            confidence_levels=confidence_levels,
        )
        scenario_rows.append({
            "Scenario": name,
            "Expected Terminal Value ($)": metrics["expected_terminal_value"],
            "Expected Return (%)": metrics["expected_return"] * 100,
            "Probability of Loss (%)": metrics["probability_of_loss"] * 100,
            "VaR 95% ($)": metrics["var_95"],
            "CVaR 95% ($)": metrics["cvar_95"],
            "VaR 99% ($)": metrics["var_99"],
            "Mean Change vs Baseline ($)": float(
                np.mean(shocked_terminal_values - baseline_terminal_values)
            ),
        })
        print(
    name,
    "Expected terminal value:",
    metrics["expected_terminal_value"],
    "Mean change:",
    np.mean(shocked_terminal_values - baseline_terminal_values),
)
    return pd.DataFrame(scenario_rows)
