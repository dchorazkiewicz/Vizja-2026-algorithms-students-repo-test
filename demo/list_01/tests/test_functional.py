import copy

import pytest
from hypothesis import given, strategies as st


@pytest.mark.parametrize(
    ("value", "lower", "upper", "expected"),
    [
        (5, 0, 10, 5),
        (-4, 0, 10, 0),
        (14, 0, 10, 10),
        (0, 0, 10, 0),
        (10, 0, 10, 10),
        (-5, -10, -1, -5),
    ],
)
def test_clamp_examples(solution, value, lower, upper, expected):
    assert solution.clamp(value, lower, upper) == expected


@given(
    lower=st.integers(-10_000, 10_000),
    width=st.integers(0, 10_000),
    value=st.integers(-20_000, 20_000),
)
def test_clamp_property(solution, lower, width, value):
    upper = lower + width
    result = solution.clamp(value, lower, upper)
    assert lower <= result <= upper
    if value < lower:
        assert result == lower
    elif value > upper:
        assert result == upper
    else:
        assert result == value


@pytest.mark.parametrize(
    ("values", "target", "expected"),
    [
        ([], 3, -1),
        ([3], 3, 0),
        ([1, 2, 3], 3, 2),
        ([8, 3, 5, 3], 3, 1),
        ([1, 1, 1], 1, 0),
        ([1, 2, 3], 9, -1),
    ],
)
def test_first_index_examples(solution, values, target, expected):
    before = copy.deepcopy(values)
    assert solution.first_index(values, target) == expected
    assert values == before


@given(st.lists(st.integers(-50, 50), max_size=50), st.integers(-50, 50))
def test_first_index_property(solution, values, target):
    expected = values.index(target) if target in values else -1
    assert solution.first_index(values, target) == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([7], (7, 7)),
        ([-7], (-7, -7)),
        ([3, 1, 7, 2], (1, 7)),
        ([-5, -10, -2], (-10, -2)),
        ([3, 3, 3], (3, 3)),
    ],
)
def test_min_max_examples(solution, values, expected):
    before = copy.deepcopy(values)
    assert solution.min_max(values) == expected
    assert values == before


def test_min_max_empty(solution):
    with pytest.raises(ValueError):
        solution.min_max([])


@given(st.lists(st.integers(-10_000, 10_000), min_size=1, max_size=100))
def test_min_max_property(solution, values):
    assert solution.min_max(values) == (min(values), max(values))


@pytest.mark.parametrize(
    "values",
    [[], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4, 5], [3, 3, 2, 1]],
)
def test_reverse_in_place(solution, values):
    original_object = values
    expected = list(reversed(values))
    result = solution.reverse_in_place(values)
    assert result is None
    assert values is original_object
    assert values == expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([], -1),
        ([-1, 100, 100], 0),
        ([1, 2, 3], -1),
        ([4, -1, -2, -5, 8], 3),
        ([0, 0, -1], 2),
    ],
)
def test_first_negative_running_sum(solution, values, expected):
    assert solution.first_negative_running_sum(values) == expected


def test_analyse_scores_examples(solution):
    scores = [50, 80, 20, 100]
    before = scores.copy()
    assert solution.analyse_scores(scores, 50) == (62.5, 20, 100, 3)
    assert scores == before


@pytest.mark.parametrize(
    ("scores", "passing"),
    [
        ([], 50),
        ([0, 101], 50),
        ([-1, 50], 50),
        ([50], -1),
        ([50], 101),
    ],
)
def test_analyse_scores_invalid(solution, scores, passing):
    with pytest.raises(ValueError):
        solution.analyse_scores(scores, passing)


@given(
    scores=st.lists(st.integers(0, 100), min_size=1, max_size=100),
    passing=st.integers(0, 100),
)
def test_analyse_scores_property(solution, scores, passing):
    result = solution.analyse_scores(scores, passing)
    expected = (
        sum(scores) / len(scores),
        min(scores),
        max(scores),
        sum(score >= passing for score in scores),
    )
    assert result == expected
