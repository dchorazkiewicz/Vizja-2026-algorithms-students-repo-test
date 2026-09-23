import random

from demo.list_02.private_grader.complexity import adjacent_exponents, median
from demo.list_02.private_grader.instrumentation import InstrumentedSequence, Ledger, TrackedItem


def comparison_cost_in_place(function, data):
    values = InstrumentedSequence(data, track_items=True)
    function(values)
    return max(1, values.count("comparison"))


def test_insertion_sort_worst_case_is_quadratic(solution):
    measurements = []
    for n in (32, 64, 128, 256):
        cost = comparison_cost_in_place(
            solution.insertion_sort_in_place,
            list(range(n - 1, -1, -1)),
        )
        measurements.append((n, cost))

    exponent = median(adjacent_exponents(measurements))
    assert exponent is not None
    assert 1.75 <= exponent <= 2.25


def test_insertion_sort_sorted_input_is_adaptive(solution):
    measurements = []
    for n in (32, 64, 128, 256):
        cost = comparison_cost_in_place(
            solution.insertion_sort_in_place,
            list(range(n)),
        )
        measurements.append((n, cost))

    exponent = median(adjacent_exponents(measurements))
    assert exponent is not None
    assert 0.75 <= exponent <= 1.25


def test_selection_sort_comparisons_are_quadratic(solution):
    measurements = []
    for n in (32, 64, 128, 256):
        cost = comparison_cost_in_place(
            solution.selection_sort_in_place,
            list(range(n - 1, -1, -1)),
        )
        measurements.append((n, cost))

    exponent = median(adjacent_exponents(measurements))
    assert exponent is not None
    assert 1.75 <= exponent <= 2.25


def test_merge_sorted_comparison_growth_is_linear(solution):
    measurements = []
    for n in (128, 256, 512, 1024):
        ledger = Ledger()
        left = InstrumentedSequence(range(0, n, 2), track_items=True, ledger=ledger)
        right = InstrumentedSequence(range(1, n, 2), track_items=True, ledger=ledger, tag_offset=n // 2)
        solution.merge_sorted(left, right)
        measurements.append((n, max(1, ledger.counts["comparison"])))

    exponent = median(adjacent_exponents(measurements))
    assert exponent is not None
    assert 0.75 <= exponent <= 1.25


def test_merge_sort_comparison_growth_is_nlogn_like(solution):
    measurements = []
    for n in (64, 128, 256, 512):
        data = list(range(n))
        random.Random(1000 + n).shuffle(data)
        ledger = Ledger()
        tracked = [TrackedItem(value, index, ledger) for index, value in enumerate(data)]
        solution.merge_sort(tracked)
        measurements.append((n, max(1, ledger.counts["comparison"])))

    exponent = median(adjacent_exponents(measurements))
    assert exponent is not None
    assert 0.90 <= exponent <= 1.50


def test_quick_sort_comparison_growth_is_nlogn_like_on_shuffled_input(solution):
    measurements = []
    for n in (64, 128, 256, 512):
        data = list(range(n))
        random.Random(2000 + n).shuffle(data)
        cost = comparison_cost_in_place(solution.quick_sort_in_place, data)
        measurements.append((n, cost))

    exponent = median(adjacent_exponents(measurements))
    assert exponent is not None
    assert 0.85 <= exponent <= 1.55
