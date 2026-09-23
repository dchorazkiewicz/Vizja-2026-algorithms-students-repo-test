"""Simulated student submission: functionally correct but methodologically weak."""


def binary_search(values, target) -> int:
    for index in range(len(values)):
        if values[index] == target:
            return index
    return -1


def insertion_sort_in_place(values) -> None:
    values[:] = sorted(values)


def selection_sort_in_place(values) -> None:
    # Bubble sort returns the right result but is not selection sort and moves
    # substantially more data on reverse-ordered inputs.
    for end in range(len(values) - 1, 0, -1):
        for index in range(end):
            if values[index] > values[index + 1]:
                values[index], values[index + 1] = values[index + 1], values[index]


def merge_sorted(left, right) -> list:
    # Correct and stable, but deliberately quadratic.
    result = list(left) + list(right)

    for index in range(1, len(result)):
        key = result[index]
        position = index - 1
        while position >= 0 and result[position] > key:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = key

    return result


def merge_sort(values) -> list:
    # Correct stable result, but no divide and conquer.
    result = list(values)

    for index in range(1, len(result)):
        key = result[index]
        position = index - 1
        while position >= 0 and result[position] > key:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = key

    return result


def quick_sort_in_place(values) -> None:
    # Correct result, but insertion sort instead of quicksort.
    for index in range(1, len(values)):
        key = values[index]
        position = index - 1
        while position >= 0 and values[position] > key:
            values[position + 1] = values[position]
            position -= 1
        values[position + 1] = key
