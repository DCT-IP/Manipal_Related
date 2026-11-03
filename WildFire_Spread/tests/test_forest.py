import numpy as np
import pytest
from src.forest import create_forest, ignite
from src.propagation import HEALTHY, BURNING


def test_forest_dimensions():
    grid = create_forest(20, 30)
    assert grid.shape == (20, 30)


def test_forest_starts_healthy():
    grid = create_forest(10, 10)
    assert np.all(grid == HEALTHY)


def test_forest_uses_integer_states():
    grid = create_forest(10, 10)
    assert np.issubdtype(grid.dtype, np.integer)


def test_ignite_sets_correct_cell():
    grid = create_forest(10, 10)
    new_grid = ignite(grid, 5, 5)
    assert new_grid[5, 5] == BURNING


def test_ignite_does_not_change_other_cells():
    grid = create_forest(10, 10)
    new_grid = ignite(grid, 5, 5)
    assert np.count_nonzero(new_grid == BURNING) == 1
    assert np.count_nonzero(new_grid == HEALTHY) == 99


def test_ignite_does_not_modify_original_grid():
    grid = create_forest(10, 10)
    original = grid.copy()
    ignite(grid, 5, 5)
    np.testing.assert_array_equal(grid, original)


def test_ignite_rejects_out_of_bounds_coordinates():
    grid = create_forest(10, 10)
    with pytest.raises(ValueError):
        ignite(grid, 10, 5)


def test_create_forest_rejects_invalid_dimensions():
    with pytest.raises(ValueError):
        create_forest(0, 10)
    with pytest.raises(ValueError):
        create_forest(10, -5)
