"""Simulated student submission: mixed correctness and algorithmic defects."""


def binary_search(values, target) -> int:
    # Finds an occurrence, but not necessarily the leftmost one.
    low = 0
    high = len(values) - 1

    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1

    return -1


def insertion_sort_in_place(values) -> None:
    # Numerically sorted, but >= moves equal keys and destroys stability.
    for index in range(1, len(values)):
        key = values[index]
        position = index - 1

        while position >= 0 and values[position] >= key:
            values[position + 1] = values[position]
            position -= 1

        values[position + 1] = key


def selection_sort_in_place(values) -> None:
    # Off-by-one: the last element is never considered as a minimum candidate.
    for start in range(max(0, len(values) - 1)):
        minimum_index = start
        for index in range(start + 1, len(values) - 1):
            if values[index] < values[minimum_index]:
                minimum_index = index
        if minimum_index != start:
            values[start], values[minimum_index] = values[minimum_index], values[start]


def merge_sorted(left, right) -> list:
    # Common merge bug: one of two equal items is lost.
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        elif right[j] < left[i]:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(values) -> list:
    # Functionally correct, but bypasses the requested algorithm.
    return sorted(values)


def quick_sort_in_place(values) -> None:
    # Functionally correct, but bypasses the requested algorithm.
    values.sort()
