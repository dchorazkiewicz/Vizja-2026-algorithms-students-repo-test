"""Student-facing starter for List 01.

This file intentionally contains function signatures and contracts only.
Students are expected to replace NotImplementedError with their algorithms.
"""


def clamp(value: int, lower: int, upper: int) -> int:
    """Clamp value to the inclusive interval [lower, upper].

    Precondition:
        lower <= upper
    """
    raise NotImplementedError


def first_index(values, target) -> int:
    """Return the first index containing target, or -1 if target is absent.

    Do not modify values.
    """
    raise NotImplementedError


def min_max(values) -> tuple[int, int]:
    """Return (minimum, maximum) for a non-empty finite sequence.

    Raise ValueError for an empty sequence.
    Do not modify values.
    Use O(1) auxiliary space.
    """
    raise NotImplementedError


def reverse_in_place(values) -> None:
    """Reverse the mutable sequence in place and return None.

    Use O(1) auxiliary space.
    """
    raise NotImplementedError


def first_negative_running_sum(values) -> int:
    """Return first index where the running sum becomes strictly negative.

    Return -1 when the running sum never becomes negative.
    """
    raise NotImplementedError


def analyse_scores(scores, passing_score: int) -> tuple[float, int, int, int]:
    """Return (average, minimum, maximum, count_at_or_above_passing_score).

    Valid scores and passing_score are in [0, 100].
    Raise ValueError for invalid or empty input.
    Process scores in one pass and do not modify the input.
    """
    raise NotImplementedError
