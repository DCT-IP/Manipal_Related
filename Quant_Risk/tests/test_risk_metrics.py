
import numpy as np
import pytest

from risk_metrics import (
    calc_var_cvar,
    calculate_probability_of_loss,
    calculate_expected_return,
    calculate_risk_metrics,
)


@pytest.fixture
def portfolio_values():
    # Initial value is 100 for every simulation.
    # Terminal values: 120, 110, 100, 90, 80.
    return np.array([
        [100.0, 120.0],
        [100.0, 110.0],
        [100.0, 100.0],
        [100.0, 90.0],
        [100.0, 80.0],
    ])


def test_var_and_cvar(portfolio_values):
    # Terminal losses are -20, -10, 0, 10, 20.
    result = calc_var_cvar(
        portfolio_values,
        confidence_level=0.80,
    )

    # 80th percentile using NumPy's default linear quantile.
    assert result["var"] == pytest.approx(12.0)

    # Worst 20% = the single worst loss, 20.
    assert result["cvar"] == pytest.approx(20.0)


def test_probability_of_loss(portfolio_values):
    # Two of five scenarios end below initial value.
    probability = calculate_probability_of_loss(portfolio_values)

    assert probability == pytest.approx(0.4)


def test_expected_return(portfolio_values):
    # Terminal returns: 20%, 10%, 0%, -10%, -20%.
    expected = calculate_expected_return(portfolio_values)

    assert expected == pytest.approx(0.0)


def test_summary_metrics(portfolio_values):
    result = calculate_risk_metrics(
        portfolio_values,
        confidence_levels=(0.80, 0.95),
    )

    assert result["initial_value"] == pytest.approx(100.0)
    assert result["expected_terminal_value"] == pytest.approx(100.0)
    assert result["expected_return"] == pytest.approx(0.0)
    assert result["probability_of_loss"] == pytest.approx(0.4)

    assert "var_80" in result
    assert "cvar_80" in result
    assert "var_95" in result
    assert "cvar_95" in result


@pytest.mark.parametrize("confidence", [0.0, 1.0, -0.1, 1.1])
def test_invalid_confidence_level_rejected(
    portfolio_values,
    confidence,
):
    with pytest.raises(ValueError):
        calc_var_cvar(portfolio_values, confidence)


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        calc_var_cvar(np.empty((0, 2)))


def test_non_finite_input_rejected():
    values = np.array([
        [100.0, 110.0],
        [100.0, np.nan],
    ])

    with pytest.raises(ValueError):
        calculate_risk_metrics(values)


def test_non_positive_portfolio_value_rejected():
    values = np.array([
        [100.0, 110.0],
        [100.0, 0.0],
    ])

    with pytest.raises(ValueError):
        calculate_expected_return(values)


def test_empty_confidence_levels_rejected(portfolio_values):
    with pytest.raises(ValueError):
        calculate_risk_metrics(portfolio_values, confidence_levels=())
