"""Example student: strong implementation."""


def clamp(value: int, lower: int, upper: int) -> int:
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value


def first_index(values, target) -> int:
    for index in range(len(values)):
        if values[index] == target:
            return index
    return -1


def min_max(values) -> tuple[int, int]:
    if len(values) == 0:
        raise ValueError("values must not be empty")
    minimum = values[0]
    maximum = values[0]
    for index in range(1, len(values)):
        value = values[index]
        if value < minimum:
            minimum = value
        if value > maximum:
            maximum = value
    return minimum, maximum


def reverse_in_place(values) -> None:
    left = 0
    right = len(values) - 1
    while left < right:
        values[left], values[right] = values[right], values[left]
        left += 1
        right -= 1


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

    first = scores[0]
    if not 0 <= first <= 100:
        raise ValueError("score must be in [0, 100]")

    total = first
    minimum = first
    maximum = first
    passing = 1 if first >= passing_score else 0

    for index in range(1, len(scores)):
        score = scores[index]
        if not 0 <= score <= 100:
            raise ValueError("score must be in [0, 100]")
        total += score
        if score < minimum:
            minimum = score
        if score > maximum:
            maximum = score
        if score >= passing_score:
            passing += 1

    return total / len(scores), minimum, maximum, passing
