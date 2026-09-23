"""Simulated student submission: strong algorithmic implementation."""


def binary_search(values, target) -> int:
    low = 0
    high = len(values) - 1
    result = -1

    while low <= high:
        middle = (low + high) // 2
        value = values[middle]

        if value < target:
            low = middle + 1
        else:
            if value == target:
                result = middle
            high = middle - 1

    return result


def insertion_sort_in_place(values) -> None:
    for index in range(1, len(values)):
        key = values[index]
        position = index - 1

        while position >= 0 and values[position] > key:
            values[position + 1] = values[position]
            position -= 1

        if position + 1 != index:
            values[position + 1] = key


def selection_sort_in_place(values) -> None:
    for start in range(len(values) - 1):
        minimum_index = start

        for index in range(start + 1, len(values)):
            if values[index] < values[minimum_index]:
                minimum_index = index

        if minimum_index != start:
            values[start], values[minimum_index] = values[minimum_index], values[start]


def merge_sorted(left, right) -> list:
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        left_value = left[left_index]
        right_value = right[right_index]

        if left_value <= right_value:
            result.append(left_value)
            left_index += 1
        else:
            result.append(right_value)
            right_index += 1

    while left_index < len(left):
        result.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        result.append(right[right_index])
        right_index += 1

    return result


def merge_sort(values) -> list:
    if len(values) <= 1:
        return list(values)

    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    return merge_sorted(left, right)


def quick_sort_in_place(values) -> None:
    def sort_range(low, high):
        i = low
        j = high
        pivot = values[(low + high) // 2]

        while i <= j:
            while values[i] < pivot:
                i += 1
            while values[j] > pivot:
                j -= 1

            if i <= j:
                if i != j:
                    values[i], values[j] = values[j], values[i]
                i += 1
                j -= 1

        if low < j:
            sort_range(low, j)
        if i < high:
            sort_range(i, high)

    if len(values) > 1:
        sort_range(0, len(values) - 1)
