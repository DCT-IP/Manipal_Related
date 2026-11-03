import numpy as np
from src.forest import create_forest, ignite
from src.propagation import run_sim, BURNT

def run_monte_carlo(
    rows,
    cols,
    ignition,
    p,
    n_runs,
    seed
):
    """
    Run multiple independent wildfire simulations.
    Returns:
        burn_probability: Probability of each cell burning.
        burned_areas: Percentage of forest burned in each run.
    """

    if not isinstance(n_runs, int) or n_runs <= 0:
        raise ValueError("Number of runs must be a positive integer")
    if not 0 <= p <= 1:
        raise ValueError("Probability must be between 0 and 1")

    burn_counts = np.zeros((rows, cols), dtype=np.int32)
    burned_areas = np.zeros(n_runs, dtype=float)
    for run in range(n_runs):
        # Generate an identical initial forest.
        grid = create_forest(rows, cols)
        # Ignite the same starting location.
        grid = ignite(grid, ignition[0], ignition[1])
        # Run with a different seed each time.
        final_grid = run_sim(
            grid,
            p=p,
            seed=seed + run
        )

        # Record which cells burned.
        burned_mask = (final_grid == BURNT)
        burn_counts += burned_mask

        # Calculate burned area as a percentage.
        burned_areas[run] = (
            np.count_nonzero(burned_mask) / (rows * cols)
        ) * 100
    # Convert total burn counts into probabilities.
    burn_probability = burn_counts / n_runs
    return burn_probability, burned_areas
