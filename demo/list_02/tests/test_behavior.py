import random

from demo.list_02.private_grader.instrumentation import (
    InstrumentedSequence,
    Ledger,
    is_stable_tagged,
    tagged_output,
)


def test_binary_search_has_logarithmic_access_pattern(solution):
    values = InstrumentedSequence(range(4096))
    assert solution.binary_search(values, 4097) == -1
    assert values.count("read") <= 20
    assert values.count("write") == 0


def test_insertion_sort_is_stable_and_adaptive(solution):
    sorted_values = InstrumentedSequence(range(64), track_items=True)
    solution.insertion_sort_in_place(sorted_values)
    assert sorted_values.count("comparison") <= 2 * 64

    stable_values = InstrumentedSequence([2, 1, 2, 1, 2], track_items=True)
    solution.insertion_sort_in_place(stable_values)
    assert is_stable_tagged(stable_values.tagged_snapshot())


def test_selection_sort_has_canonical_comparison_count_and_limited_writes(solution):
    values = InstrumentedSequence(range(63, -1, -1), track_items=True)
    solution.selection_sort_in_place(values)
    n = len(values)
    assert values.count("comparison") == n * (n - 1) // 2
    assert values.count("write") <= 2 * (n - 1)


def test_merge_sorted_is_stable_and_does_not_mutate_inputs(solution):
    ledger = Ledger()
    left = InstrumentedSequence([1, 2, 2, 5], track_items=True, ledger=ledger, tag_offset=0)
    right = InstrumentedSequence([2, 2, 3, 6], track_items=True, ledger=ledger, tag_offset=4)
    result = solution.merge_sorted(left, right)
    tagged = tagged_output(result)

    assert [key for key, _ in tagged] == [1, 2, 2, 2, 2, 3, 5, 6]
    assert is_stable_tagged(tagged)
    assert ledger.counts["write"] == 0


def test_merge_sort_is_stable_and_preserves_input(solution):
    values = InstrumentedSequence([4, 2, 4, 1, 2, 3, 1], track_items=True)
    before = values.tagged_snapshot()
    result = solution.merge_sort(values)
    assert values.tagged_snapshot() == before
    assert is_stable_tagged(tagged_output(result))


def test_quick_sort_is_in_place_without_slicing(solution):
    data = list(range(128))
    random.Random(2026).shuffle(data)
    values = InstrumentedSequence(data, track_items=True)
    result = solution.quick_sort_in_place(values)
    assert result is None
    assert values.snapshot() == sorted(data)
    assert values.count("slice_read") == 0
    assert values.count("slice_write") == 0
