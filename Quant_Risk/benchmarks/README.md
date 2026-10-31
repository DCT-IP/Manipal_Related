# Simulation Benchmarks

## Overview

This directory contains performance benchmarks for the correlated Geometric Brownian Motion (GBM) simulation engine used in QUANT//RISK.

The benchmarks evaluate:

- Runtime performance before and after chunked simulation.
- Memory consumption across different chunk sizes.
- Scaling behaviour with increasing asset counts.
- Scaling behaviour with increasing time steps.

The objective is to measure the effects of optimization and identify the simulator's current performance limitations.

## Benchmark Methodology

Measurements use:

| Metric | Method |
|---|---|
| Runtime | `time.perf_counter()` |
| Peak traced memory | `tracemalloc` |
| RSS change | `psutil` |
| Statistical aggregation | Median of repeated runs |

A fixed random seed is used to support reproducibility.

RSS change represents the difference between process RSS before and after a benchmark. It is not a measurement of peak RSS.

Peak traced memory measures Python-traced allocations and should not be interpreted as total system memory consumption.

## 1. Baseline vs Chunked Implementation

Configuration:

- Assets: 3
- Time steps: 252
- Seed: 42

| Simulations | Original Runtime (s) | Chunked Runtime (s) | Original Peak (MB) | Chunked Peak (MB) |
|---:|---:|---:|---:|---:|
| 1,000 | 0.0343 | 0.0178 | 34.70 | 17.33 |
| 10,000 | 0.2933 | 0.1809 | 346.36 | 173.27 |
| 50,000 | 2.4629 | 0.9044 | 1,731.56 | 462.57 |
| 100,000 | 4.4762 | 1.7796 | 3,463.05 | 752.11 |

At 100,000 simulations:

- Runtime decreased by approximately 60.3%.
- Execution became approximately 2.52 times faster.
- Peak traced memory decreased by approximately 78.3%.

Terminal means remained identical between the original and chunked implementations at each tested simulation count.

The optimization reduced temporary memory allocations without changing the underlying GBM calculation.

## 2. Chunk-Size Comparison

Configuration:

- Simulations: 100,000
- Assets: 3
- Time steps: 252
- Five measured repetitions after warm-up.

| Chunk Size | Median Runtime (s) | Peak Traced Memory (MB) |
|---:|---:|---:|
| 1,000 | 1.8593 | 596.39 |
| 5,000 | 1.9498 | 665.59 |
| 10,000 | 1.9572 | 752.11 |
| 20,000 | 1.9807 | 925.14 |

Smaller chunks reduce the size of temporary arrays, lowering peak traced memory.

However, very small chunks can introduce additional loop and processing overhead.

Chunk size 1,000 provided the lowest measured runtime and memory consumption in the latest experiment.

It is therefore the current default, rather than a universally optimal value.

Configuration:

`config.py`

`DEFAULT_CHUNK_SIZE = 1_000`

## 3. Asset Scaling

Configuration:

- Simulations: 10,000
- Time steps: 252
- Chunk size: 1,000

| Assets | Median Runtime (s) | Peak Traced Memory (MB) |
|---:|---:|---:|
| 1 | 0.1141 | 25.07 |
| 3 | 0.4741 | 75.21 |
| 5 | 0.8164 | 125.36 |
| 10 | 1.4418 | 250.71 |
| 20 | 2.9063 | 501.41 |

Peak memory increases approximately linearly with the number of assets.

This is consistent with the dimensions of the simulation output array.

## 4. Time-Step Scaling

Configuration:

- Simulations: 10,000
- Assets: 3
- Chunk size: 1,000

| Time Steps | Median Runtime (s) | Peak Traced Memory (MB) |
|---:|---:|---:|
| 63 | 0.0463 | 18.98 |
| 126 | 0.0905 | 37.72 |
| 252 | 0.1916 | 75.21 |
| 504 | 0.4056 | 150.20 |
| 1,008 | 0.8115 | 300.16 |

Runtime and peak memory increase approximately linearly with the number of time steps.

## 5. Memory Scaling Model

The simulation returns an array with dimensions:

`(n_simulations, steps + 1, n_assets)`

For float64 values, the approximate output memory requirement is:

\[
M = 8N(T+1)A
\]

Where:

- \(N\) = number of simulations
- \(T\) = number of time steps
- \(A\) = number of assets
- \(M\) = memory in bytes

This explains why memory grows with simulation count, asset count and time steps.

Chunking reduces temporary allocations but does not remove the requirement to store the complete output array.

## 6. Findings

1. Chunked simulation substantially reduces temporary memory consumption.
2. Runtime improved by approximately 60.3% at 100,000 simulations in the baseline comparison.
3. The current chunk size of 1,000 provides a good measured balance between runtime and memory.
4. Memory consumption scales approximately linearly with the output dimensions.
5. The complete path matrix remains the primary memory constraint for larger workloads.
6. Fixed-seed terminal means remained consistent in the baseline and chunked comparisons.

## 7. Limitations

- Measurements are hardware- and environment-dependent.
- System load can influence runtime.
- RSS change is not peak RSS.
- `tracemalloc` does not represent every native allocation made by numerical libraries.
- Chunk-size rankings may vary across machines and workloads.
- Full path storage limits the maximum practical simulation size.

## 8. Future Work

The next optimization milestone is memory-efficient simulation output.

Potential extensions:

- Terminal-value-only simulation.
- Streaming simulation chunks.
- Online statistical aggregation.
- Portfolio-level terminal-value calculation without storing every asset path.
- Risk metric calculation over streamed simulation results.

These improvements would allow larger Monte Carlo workloads without requiring the entire trajectory matrix to remain in memory.

## Benchmark Files

| File | Description |
|---|---|
| `simulation_benchmark.csv` | Original pre-optimization baseline |
| `chunk_size_benchmark.csv` | Chunk-size comparison |
| `asset_scaling_benchmark.csv` | Asset and time-step scaling grid |
| `time_step_scaling_benchmark.csv` | Independent time-step scaling |

