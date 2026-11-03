import numpy as np
import pytest

from src.propagation import (
    HEALTHY,
    BURNING,
    BURNT,
    step,
    run_sim,
)


def test_cell_states():
    assert HEALTHY == 0
    assert BURNING == 1
    assert BURNT == -1


def test_grid_does_not_change_shape():
    grid = np.zeros((10, 10), dtype=np.int8)
    grid[5, 5] = BURNING
    next_grid = step(grid, p=0.5, rng=np.random.default_rng(42))
    assert next_grid.shape == grid.shape


def test_burning_cell_becomes_burnt():
    grid = np.zeros((5, 5), dtype=np.int8)
    grid[2, 2] = BURNING
    next_grid = step(grid, p=0.0, rng=np.random.default_rng(42))
    assert next_grid[2, 2] == BURNT


def test_burnt_cell_stays_burnt():
    grid = np.zeros((5, 5), dtype=np.int8)
    grid[2, 2] = BURNT
    next_grid = step(grid, p=1.0, rng=np.random.default_rng(42))
    assert next_grid[2, 2] == BURNT


def test_zero_probability_prevents_ignition():
    grid = np.zeros((5, 5), dtype=np.int8)
    grid[2, 2] = BURNING
    next_grid = step(grid, p=0.0, rng=np.random.default_rng(42))
    assert np.count_nonzero(next_grid == BURNING) == 0


def test_probability_one_ignites_neighbours():
    grid = np.zeros((5, 5), dtype=np.int8)
    grid[2, 2] = BURNING
    next_grid = step(grid, p=1.0, rng=np.random.default_rng(42))
    assert next_grid[1, 1] == BURNING
    assert next_grid[1, 2] == BURNING
    assert next_grid[1, 3] == BURNING
    assert next_grid[2, 1] == BURNING
    assert next_grid[2, 3] == BURNING
    assert next_grid[3, 1] == BURNING
    assert next_grid[3, 2] == BURNING
    assert next_grid[3, 3] == BURNING


def test_updates_are_synchronous():
    grid = np.zeros((5, 5), dtype=np.int8)
    grid[2, 2] = BURNING
    next_grid = step(grid, p=1.0, rng=np.random.default_rng(42))
    assert next_grid[0, 0] == HEALTHY
    assert next_grid[2, 2] == BURNT


def test_seeded_simulation_is_reproducible():
    grid = np.zeros((20, 20), dtype=np.int8)
    grid[10, 10] = BURNING
    result_a = run_sim(
        grid.copy(), p=0.3, seed=42
    )
    result_b = run_sim(
        grid.copy(), p=0.3, seed=42
    )
    np.testing.assert_array_equal(result_a, result_b)


def test_invalid_probability_raises_error():
    grid = np.zeros((5, 5), dtype=np.int8)
    with pytest.raises(ValueError):
        step(grid, p=1.5, rng=np.random.default_rng(42))
