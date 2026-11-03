
import numpy as np

HEALTHY = 0
BURNING = 1
BURNT = -1

VALID_STATES = {HEALTHY, BURNING, BURNT}


def _validate_grid(grid):
    if not isinstance(grid, np.ndarray):
        raise TypeError("Grid needs to be a numpy array")
    if grid.ndim != 2:
        raise ValueError("Grid needs to be 2d")
    if grid.size == 0:
        raise ValueError("Grid can't be empty")
    if not np.isin(grid, list(VALID_STATES)).all():
        raise ValueError("Grid has invalid states")


def step(grid, p, rng):
    """
    Advance the cellular automaton by one timestep.
    Uses an eight-cell Moore neighbourhood and synchronous state updates.
    """
    _validate_grid(grid)
    if not 0 <= p <= 1.0:
        raise ValueError("Invalid probability given")
    if not isinstance(rng, np.random.Generator):
        raise TypeError("rng should be a NumPy generator")

    rows, cols = grid.shape
    burning = (grid == BURNING)
    neighbour_count = np.zeros(grid.shape, dtype=np.int8)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            shifted = np.zeros(grid.shape, dtype=bool)
            # Source boundaries
            sr_start = max(0, -dr)
            sr_end = min(rows, rows - dr)
            sc_start = max(0, -dc)
            sc_end = min(cols, cols - dc)
            # Destination boundaries
            tr_start = max(0, dr)
            tr_end = min(rows, rows + dr)
            tc_start = max(0, dc)
            tc_end = min(cols, cols + dc)
            shifted[tr_start:tr_end, tc_start:tc_end] = burning[
                sr_start:sr_end, sc_start:sc_end
            ]
            neighbour_count += shifted

    # Calculate ignition probability.
    ignition_probability = 1 - (1 - p) ** neighbour_count
    healthy = (grid == HEALTHY)
    random_values = rng.random(grid.shape)
    newly_burning = (
        healthy &
        (random_values < ignition_probability)
    )
    # Construct the next generation.
    next_grid = grid.copy()
    # Existing fire burns out.
    next_grid[burning] = BURNT
    # Newly ignited trees start burning.
    next_grid[newly_burning] = BURNING
    return next_grid


def run_sim(grid, p, seed):
    """
    Run until no burning cells remain.
    Returns the final grid.
    """
    _validate_grid(grid)
    if not 0 <= p <= 1.0:
        raise ValueError("Invalid probability given")
    rng = np.random.default_rng(seed)
    current_grid = grid.copy()
    while np.any(current_grid == BURNING):
        current_grid = step(current_grid, p, rng)
    return current_grid
