import numpy as np
import pytest
from portfolio import (
    calculate_portfolio_value,
    calc_portfolio_return,
    compare_portfolios,
)


def test_initial_portfolio_value_is_preserved():
    paths = np.array([
        [[100.0, 200.0], [110.0, 190.0]],
        [[100.0, 200.0], [90.0, 210.0]],
    ])
    values = calculate_portfolio_value(
        paths,
        np.array([0.6, 0.4]),
        initial_capital=100_000.0,
    )
    np.testing.assert_allclose(values[:, 0], 100_000.0)


def test_single_asset_portfolio():
    paths = np.array([
        [[100.0], [110.0], [120.0]],
    ])
    values = calculate_portfolio_value(
        paths,
        np.array([1.0]),
        initial_capital=10_000.0,
    )
    np.testing.assert_allclose(
        values,
        [[10_000.0, 11_000.0, 12_000.0]],
    )


def test_portfolio_returns():
    values = np.array([
        [100_000.0, 110_000.0, 90_000.0],
        [100_000.0, 105_000.0, 120_000.0],
    ])
    returns = calc_portfolio_return(values)
    np.testing.assert_allclose(
        returns,
        [[0.0, 0.1, -0.1], [0.0, 0.05, 0.2]],
    )


def test_compare_portfolios():
    paths = np.array([
        [[100.0, 200.0], [110.0, 180.0]],
    ])
    results = compare_portfolios(
        paths,
        {
            "Equal": np.array([0.5, 0.5]),
            "Asset A": np.array([1.0, 0.0]),
        },
        initial_capital=10_000.0,
    )
    assert set(results) == {"Equal", "Asset A"}
    assert results["Equal"].shape == (1, 2)
    np.testing.assert_allclose(results["Asset A"], [[10_000.0, 11_000.0]])


def test_invalid_weights_rejected():
    paths = np.array([[[100.0, 200.0], [110.0, 190.0]]])
    with pytest.raises(ValueError):
        calculate_portfolio_value(paths, np.array([0.6, 0.6]))


def test_negative_weights_rejected():
    paths = np.array([[[100.0, 200.0], [110.0, 190.0]]])
    with pytest.raises(ValueError):
        calculate_portfolio_value(paths, np.array([1.2, -0.2]))
