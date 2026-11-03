from pathlib import Path
import numpy as np
from src.forest import create_forest, ignite
from src.propagation import run_sim, BURNT
from src.visualization import (
    plot_forest,
    plot_burn_probability,
    plot_burned_area
)
from experiments.exp import run_monte_carlo

ROWS = 50
COLS = 50
IGNITION = (25, 25)
BASE_PROBABILITY = 0.3
N_RUNS = 300
SEED = 42

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

grid = create_forest(ROWS, COLS)
grid = ignite(grid, *IGNITION)

final_grid = run_sim(
    grid,
    p=BASE_PROBABILITY,
    seed=SEED
)

burned = np.count_nonzero(final_grid == BURNT)

print("Individual simulation")
print("---------------------")
print("Total cells:", ROWS * COLS)
print("Burned cells:", burned)
print("Burned percentage:", burned / (ROWS * COLS) * 100)


print("\nRunning Monte Carlo experiments...")
burn_probability, burned_areas = run_monte_carlo(
    rows=ROWS,
    cols=COLS,
    ignition=IGNITION,
    p=BASE_PROBABILITY,
    n_runs=N_RUNS,
    seed=SEED
)


print("\nMonte Carlo results")
print("-------------------")
print("Number of runs:", N_RUNS)
print("Mean burned area:", np.mean(burned_areas))
print("Median burned area:", np.median(burned_areas))
print("Minimum burned area:", np.min(burned_areas))
print("Maximum burned area:", np.max(burned_areas))
print("Standard deviation:", np.std(burned_areas))


plot_forest(
    final_grid,
    RESULTS_DIR / "final_forest.png"
)

plot_burn_probability(
    burn_probability,
    RESULTS_DIR / "burn_probability.png"
)

plot_burned_area(
    burned_areas,
    RESULTS_DIR / "burned_area_histogram.png"
)


np.save(
    RESULTS_DIR / "burn_probability.npy",
    burn_probability
)

np.save(
    RESULTS_DIR / "burned_areas.npy",
    burned_areas
)

print("\nResults saved in:", RESULTS_DIR)
