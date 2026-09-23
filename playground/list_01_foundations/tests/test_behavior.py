from playground.list_01_foundations.grader.tracked import TrackedSequence


def test_first_index_stops_after_first_match(solution):
    values = TrackedSequence([8, 3, 5, 3, 9, 10])
    assert solution.first_index(values, 3) == 1
    assert values.reads <= 2
    assert values.writes == 0
    assert values.slice_reads == 0


def test_min_max_does_not_copy_or_mutate(solution):
    values = TrackedSequence(range(100))
    assert solution.min_max(values) == (0, 99)
    assert values.writes == 0
    assert values.slice_reads == 0
    assert values.reads <= 3 * len(values)


def test_reverse_is_in_place_and_linear(solution):
    values = TrackedSequence(range(20))
    result = solution.reverse_in_place(values)
    assert result is None
    assert values.snapshot() == list(reversed(range(20)))
    assert values.slice_reads == 0
    assert values.reads <= 2 * len(values)
    assert values.writes <= 2 * len(values)


def test_running_sum_early_exit(solution):
    values = TrackedSequence([-1] + [10] * 10_000)
    assert solution.first_negative_running_sum(values) == 0
    assert values.reads == 1


def test_analyse_scores_is_single_pass_in_behavior(solution):
    values = TrackedSequence([10, 50, 70, 100, 0, 90])
    assert solution.analyse_scores(values, 50) == (320 / 6, 0, 100, 4)
    assert values.writes == 0
    assert values.slice_reads == 0
    assert values.reads <= 2 * len(values)
