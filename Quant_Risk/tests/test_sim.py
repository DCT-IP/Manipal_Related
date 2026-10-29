import numpy as np
import pytest
from simulation import simulate_gbm

def test_output_shape():
    prices = simulate_gbm(
        initial_prices=np.array([100.0, 200.0]),
        drift=np.array([0.08, 0.06]),
        volatility=np.array([0.20, 0.15]),
        correlation=np.array([[1.0, 0.5], [0.5, 1.0]]),
        steps=252,
        n_simulations=1000,
        seed=42,
    )
    assert prices.shape == (1000, 253, 2)
  
def test_initial_prices_are_preserved():
    initial = np.array([100.0, 200.0])

    prices = simulate_gbm(
        initial_prices=initial,
        drift=np.array([0.08, 0.06]),
        volatility=np.array([0.20, 0.15]),
        correlation=np.eye(2),
        n_simulations=100,
        seed=42,
    )

    assert prices.shape == (100, 253, 2)
    np.testing.assert_allclose(
    prices[:, 0, :],
    np.tile(initial, (prices.shape[0], 1)),
)


def test_reproducibility():
    kwargs = {
        "initial_prices": np.array([100.0]),
        "drift": np.array([0.08]),
        "volatility": np.array([0.20]),
        "correlation": np.array([[1.0]]),
        "n_simulations": 100,
        "seed": 123,
    }
    first = simulate_gbm(**kwargs)
    second = simulate_gbm(**kwargs)
    np.testing.assert_array_equal(first, second)


def test_prices_remain_positive():
    prices = simulate_gbm(
        initial_prices=np.array([100.0, 200.0]),
        drift=np.array([0.08, 0.06]),
        volatility=np.array([0.20, 0.15]),
        correlation=np.array([[1.0, 0.5], [0.5, 1.0]]),
        n_simulations=1000,
        seed=42,
    )
    assert np.all(prices > 0)


def test_rejects_invalid_volatility():
    with pytest.raises(ValueError):
        simulate_gbm(
            initial_prices=np.array([100.0]),
            drift=np.array([0.08]),
            volatility=np.array([-0.20]),
            correlation=np.array([[1.0]]),
        )


def test_rejects_invalid_correlation():
    with pytest.raises(ValueError):
        simulate_gbm(
            initial_prices=np.array([100.0, 200.0]),
            drift=np.array([0.08, 0.06]),
            volatility=np.array([0.20, 0.15]),
            correlation=np.array([[1.0, 1.5], [1.5, 1.0]]),
        )
