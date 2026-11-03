import numpy as np
from experiments.exp import run_monte_carlo

def test_burn_probability_map_shape():
    probability, burned_areas = run_monte_carlo(
        rows=10,
        cols=10,
        ignition=(5, 5),
        p=0.3,
        n_runs=5,
        seed=42
    )
    assert probability.shape == (10, 10)


def test_burn_probability_is_between_zero_and_one():
    probability, _ = run_monte_carlo(
        rows=10,
        cols=10,
        ignition=(5, 5),
        p=0.3,
        n_runs=5,
        seed=42
    )
    assert np.all(probability >= 0)
    assert np.all(probability <= 1)


def test_ignition_cell_always_burns():
    probability, _ = run_monte_carlo(
        rows=10,
        cols=10,
        ignition=(5, 5),
        p=0.3,
        n_runs=5,
        seed=42
    )
    assert probability[5, 5] == 1.0


def test_burned_areas_count_matches_runs():
    _, burned_areas = run_monte_carlo(
        rows=10,
        cols=10,
        ignition=(5, 5),
        p=0.3,
        n_runs=5,
        seed=42
    )
    assert len(burned_areas) == 5


def test_burned_areas_are_valid_percentages():
    _, burned_areas = run_monte_carlo(
        rows=10,
        cols=10,
        ignition=(5, 5),
        p=0.3,
        n_runs=5,
        seed=42
    )
    assert np.all(burned_areas >= 0)
    assert np.all(burned_areas <= 100)


def test_experiment_is_reproducible():
    result_a = run_monte_carlo(
        rows=10, cols=10, ignition=(5, 5),
        p=0.3, n_runs=5, seed=42
    )
    result_b = run_monte_carlo(
        rows=10, cols=10, ignition=(5, 5),
        p=0.3, n_runs=5, seed=42
    )
    np.testing.assert_array_equal(result_a[0], result_b[0])
    np.testing.assert_array_equal(result_a[1], result_b[1])


def test_zero_probability_burns_only_ignition_cell():
    probability, burned_areas = run_monte_carlo(
        rows=10,
        cols=10,
        ignition=(5, 5),
        p=0.0,
        n_runs=5,
        seed=42
    )
    assert np.count_nonzero(probability) == 1
    assert np.all(burned_areas == 1.0)
