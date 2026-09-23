"""Example student: functionally good, algorithmically mediocre.

The code deliberately uses convenient Python shortcuts and extra passes.
"""


def clamp(value: int, lower: int, upper: int) -> int:
    return min(max(value, lower), upper)


def first_index(values, target) -> int:
    result = -1
    for index in range(len(values)):
        if values[index] == target and result == -1:
            result = index
    return result


def min_max(values) -> tuple[int, int]:
    if len(values) == 0:
        raise ValueError("values must not be empty")
    return min(values), max(values)


def reverse_in_place(values) -> None:
    values[:] = values[::-1]


def first_negative_running_sum(values) -> int:
    running_sum = 0
    for index in range(len(values)):
        running_sum += values[index]
        if running_sum < 0:
            return index
    return -1


def analyse_scores(scores, passing_score: int) -> tuple[float, int, int, int]:
    if not 0 <= passing_score <= 100:
        raise ValueError("passing_score must be in [0, 100]")
    if len(scores) == 0:
        raise ValueError("scores must not be empty")
    for score in scores:
        if not 0 <= score <= 100:
            raise ValueError("score must be in [0, 100]")
    return (
        sum(scores) / len(scores),
        min(scores),
        max(scores),
        sum(score >= passing_score for score in scores),
    )
