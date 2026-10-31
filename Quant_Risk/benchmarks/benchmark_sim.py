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
from config import DEFAULT_CHUNK_SIZE
SIMULATION_COUNTS = [1_000,10_000,50_000,100_000]
CHUNK_SIZES = [1_000, 5_000, 10_000, 20_000]
ASSET_COUNT = 3
STEPS = 252
REPEATS = 3
SEED = 45
ASSET_COUNTS = [1, 3, 5, 10, 20]
STEP_COUNTS = [63, 126, 252, 504, 1008]
SCALING_SIMULATIONS = 10_000
SCALING_REPEATS = 3


def benchmark(
    n_sim: int,
    chunk_size: int,
) -> dict:

    initial_prices = np.array([100.0, 120.0, 80.0])
    drift = np.array([0.08, 0.10, 0.06])
    volatility = np.array([0.20, 0.25, 0.15])
    corr = np.array([
        [1.0, 0.7, 0.2],
        [0.7, 1.0, 0.4],
        [0.2, 0.4, 1.0],
    ])

    gc.collect()
    process = psutil.Process()
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
        chunk_size=chunk_size,
    )
    elapsed = time.perf_counter() - start
    _, peak_traced_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memory_after = process.memory_info().rss
    return {
        "simulations": n_sim,
        "chunk_size": chunk_size,
        "runtime_seconds": elapsed,
        "peak_traced_memory_mb": peak_traced_memory / (1024 ** 2),
        "rss_change_mb": (memory_after - mem_before) / (1024 ** 2),
        "output_shape": paths.shape,
        "terminal_mean": float(paths[:, -1, :].mean()),
    }


def run_chunk_benchmarks():
    simulation_count = 100_000
    chunk_sizes = [1_000, 5_000, 10_000, 20_000]
    repeats = 5
    results = []

    for chunk in chunk_sizes:
        print(f"\nWarm-up: chunk size {chunk:,}")
        benchmark(simulation_count, chunk)
        print(f"Testing chunk size: {chunk:,}")
        runs = [
            benchmark(simulation_count, chunk)
            for _ in range(repeats)
        ]
        result = {
            "simulations": simulation_count,
            "chunk_size": chunk,
            "median_runtime_seconds": float(
                np.median([r["runtime_seconds"] for r in runs])
            ),
            "median_peak_traced_memory_mb": float(
                np.median([
                    r["peak_traced_memory_mb"] for r in runs
                ])
            ),
            "median_rss_change_mb": float(
                np.median([r["rss_change_mb"] for r in runs])
            ),
            "terminal_mean": runs[-1]["terminal_mean"],
        }
        results.append(result)
        print(result)
    return results


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


def benchmark_scaling():
    results = []
    STEP_COUNTS = [63, 126, 252, 504, 1008]
    rng = np.random.default_rng(SEED)
    for asset_count in ASSET_COUNTS:
        print(f"\nTesting {asset_count} assets")
        initial_prices = rng.uniform(50, 150, asset_count)
        drift = rng.uniform(0.04, 0.12, asset_count)
        volatility = rng.uniform(0.10, 0.30, asset_count)
        raw = rng.normal(size=(asset_count, asset_count))
        covariance = raw @ raw.T
        scale = np.sqrt(np.diag(covariance))
        correlation = covariance / np.outer(scale, scale)
        for steps in STEP_COUNTS:
            runs = []
            for _ in range(SCALING_REPEATS):
                gc.collect()
                process = psutil.Process()
                mem_before = process.memory_info().rss
                tracemalloc.start()
                start = time.perf_counter()
                paths = simulate_gbm(
                    initial_prices=initial_prices,
                    drift=drift,
                    volatility=volatility,
                    correlation=correlation,
                    time_horizon=1.0,
                    steps=steps,
                    n_simulations=SCALING_SIMULATIONS,
                    seed=SEED,
                    chunk_size=DEFAULT_CHUNK_SIZE,
                )
                runtime = time.perf_counter() - start
                _, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                mem_after = process.memory_info().rss
                runs.append({
                    "runtime_seconds": runtime,
                    "peak_traced_memory_mb": peak_memory / (1024 ** 2),
                    "rss_change_mb": (mem_after - mem_before) / (1024 ** 2),
                })
                del paths
            results.append({
                "asset_count": asset_count,
                "steps": steps,
                "simulations": SCALING_SIMULATIONS,
                "chunk_size": DEFAULT_CHUNK_SIZE,
                "median_runtime_seconds": float(np.median(
                    [r["runtime_seconds"] for r in runs]
                )),
                "median_peak_traced_memory_mb": float(np.median(
                    [r["peak_traced_memory_mb"] for r in runs]
                )),
                "median_rss_change_mb": float(np.median(
                    [r["rss_change_mb"] for r in runs]
                )),
            })
            print(results[-1])
    return results

def benchmark_step_scaling():
    results = []
    asset_count = 3
    initial_prices = np.array([100.0, 120.0, 80.0])
    drift = np.array([0.08, 0.10, 0.06])
    volatility = np.array([0.20, 0.25, 0.15])
    correlation = np.array([
        [1.0, 0.7, 0.2],
        [0.7, 1.0, 0.4],
        [0.2, 0.4, 1.0],
    ])

    for steps in STEP_COUNTS:
        print(f"\nTesting {steps:,} time steps")

        benchmark(
            n_sim=1_000,
            chunk_size=DEFAULT_CHUNK_SIZE,
        )  
        runs = []
        for _ in range(3):
            gc.collect()
            process = psutil.Process()
            mem_before = process.memory_info().rss
            tracemalloc.start()
            start = time.perf_counter()
            paths = simulate_gbm(
                initial_prices=initial_prices,
                drift=drift,
                volatility=volatility,
                correlation=correlation,
                time_horizon=1.0,
                steps=steps,
                n_simulations=SCALING_SIMULATIONS,
                seed=SEED,
                chunk_size=DEFAULT_CHUNK_SIZE,
            )
            runtime = time.perf_counter() - start
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss
            runs.append({
                "runtime_seconds": runtime,
                "peak_traced_memory_mb": peak_memory / (1024 ** 2),
                "rss_change_mb": (
                    mem_after - mem_before
                ) / (1024 ** 2),
            })
            del paths
        result = {
            "asset_count": asset_count,
            "steps": steps,
            "simulations": SCALING_SIMULATIONS,
            "chunk_size": DEFAULT_CHUNK_SIZE,
            "median_runtime_seconds": float(np.median(
                [r["runtime_seconds"] for r in runs]
            )),
            "median_peak_traced_memory_mb": float(np.median(
                [r["peak_traced_memory_mb"] for r in runs]
            )),
            "median_rss_change_mb": float(np.median(
                [r["rss_change_mb"] for r in runs]
            )),
        }
        results.append(result)
        print(result)
    return results


if __name__ == "__main__":
    results = run_chunk_benchmarks()
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "chunk_size_benchmark.csv"
    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to: {output_file}")

    scaling_results = benchmark_scaling()
    scaling_path = (
        PROJECT_ROOT
        / "benchmarks"
        / "results"
        / "asset_scaling_benchmark.csv"
    )
    with scaling_path.open("w", newline="") as file:
        writer = csv.DictWriter(
        file,
        fieldnames=scaling_results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(scaling_results)
    print(f"\nAsset scaling results saved to: {scaling_path}")
    step_results = benchmark_step_scaling()

    step_path = (
    PROJECT_ROOT
    / "benchmarks"
    / "results"
    / "time_step_scaling_benchmark.csv"
    )

    with step_path.open("w", newline="") as file:
        writer = csv.DictWriter(
        file,
        fieldnames=step_results[0].keys(),
        )
        writer.writeheader()
        writer.writerows(step_results)

    print(f"\nTime-step scaling results saved to: {step_path}")


