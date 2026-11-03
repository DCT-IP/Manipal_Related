import numpy as np
from src.propagation import HEALTHY, BURNING, _validate_grid

def create_forest(rows, cols):
    """
    Create a forest where every cell initially contains
    a healthy tree.
    """
    if not isinstance(rows, int) or not isinstance(cols, int):
        raise TypeError("Dimensions must be integers")
    if rows <= 0 or cols <= 0:
        raise ValueError("Dimensions must be positive")
    return np.full((rows, cols), HEALTHY, dtype=np.int8)


def ignite(grid, row, col):
    """
    Ignite one healthy tree and return a new grid.
    """
    _validate_grid(grid)
    if not isinstance(row, int) or not isinstance(col, int):
        raise TypeError("Coordinates must be integers")

    rows, cols = grid.shape
    if not (0 <= row < rows and 0 <= col < cols):
        raise ValueError("Ignition coordinates out of bounds")
    if grid[row, col] != HEALTHY:
        raise ValueError("Ignition point must be a healthy tree")
    new_grid = grid.copy()
    new_grid[row, col] = BURNING
    return new_grid
