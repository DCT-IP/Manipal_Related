import csv
import gc
import time
import tracemalloc
from pathlib import Path
import numpy as np
import psutil
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from simulation import simulate_gbm

SIMULATION_COUNTS = [1_000,10_000,50_000,100_000]
ASSET_COUNT = 3
STEPS = 252
REPEATS = 3
SEED = 45

def benchmark(n_sim):
    initial_prices = np.array([100.0,120.0,80.0])
    drift = np.array([0.09, 0.1, 0.06])
    volatility = np.array([0.2, 0.25,0.15])
    corr = np.array([
        [1.0, 0.7, 0.2],
        [0.7, 1.0, 0.4],
        [0.2, 0.4, 1.0],
    ])
    gc.collect()
    process =psutil.Process()
    mem_before = process.memory_info().rss
    tracemalloc.start()
    start = time.perf_counter()

    paths = simulate_gbm(
        initial_prices=initial_prices,
        drift=drift,
        volatility=volatility,
        correlation=corr,
        time_horizon=1.0,
        steps=STEPS,
        n_simulations=n_sim,
        seed=SEED,
    )

    elapsed = time.perf_counter() - start
    _, peak_traced_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_after = process.memory_info().rss

    return {
        "runtime_seconds": elapsed,
        "peak_traced_memory_mb": peak_traced_memory / (1024 ** 2),
        "rss_change_mb": (memory_after - mem_before) / (1024 ** 2),
        "output_shape": paths.shape,
        "terminal_mean": float(paths[:, -1, :].mean()),
    }


def run_benchmarks():
    results = []

    for count in SIMULATION_COUNTS:
        print(f"\nBenchmarking {count:,} simulations...")

        runs = [
            benchmark(count)
            for _ in range(REPEATS)
        ]

        result = {
            "simulations": count,
            "assets": ASSET_COUNT,
            "steps": STEPS,
            "median_runtime_seconds": float(
                np.median([r["runtime_seconds"] for r in runs])
            ),
            "median_peak_traced_memory_mb": float(
                np.median([r["peak_traced_memory_mb"] for r in runs])
            ),
            "median_rss_change_mb": float(
                np.median([r["rss_change_mb"] for r in runs])
            ),
            "terminal_mean": runs[-1]["terminal_mean"],
        }

        results.append(result)

        print(result)

    return results


if __name__ == "__main__":
    run_benchmarks()

