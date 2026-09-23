"""Example student: weak implementation with correctness and method defects."""


def clamp(value: int, lower: int, upper: int) -> int:
    return abs(value)


def first_index(values, target) -> int:
    result = -1
    for index in range(len(values)):
        if values[index] == target:
            result = index
    return result


def min_max(values) -> tuple[int, int]:
    minimum = 0
    maximum = 0
    for value in values:
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
    return minimum, maximum


def reverse_in_place(values) -> None:
    copy = list(reversed(values))
    return copy


def first_negative_running_sum(values) -> int:
    for index in range(len(values)):
        if sum(values[: index + 1]) < 0:
            return index
    return -1


def analyse_scores(scores, passing_score: int):
    if not scores:
        return None
    return (
        sum(scores) / len(scores),
        min(scores),
        max(scores),
        len([score for score in scores if score >= passing_score]),
    )
