# List 01 — Contracts, State and Simple Algorithms

This is the student-facing assignment specification used by the demonstrator.

In production, students would receive material of this kind without the private grader, hidden tests, or reference implementation.

Implement the function bodies in starter.py and complete DESIGN_TEMPLATE.md for each task.

## Task 1 — clamp

Implement clamp(value, lower, upper).

Precondition: lower <= upper.

Return lower when value is below the interval, upper when it is above the interval, and value otherwise.

Algorithmic intent: explicit selection, O(1) time, O(1) auxiliary space, and no min/max shortcut.

## Task 2 — first_index

Return the smallest index containing target, or -1 when target is absent. Do not modify the input.

Algorithmic intent: explicit linear scan, immediate return after the first match, best case O(1), worst case O(n), and no index/next shortcut.

## Task 3 — min_max

Return (minimum, maximum) for a non-empty sequence. Raise ValueError for empty input.

Algorithmic intent: one pass, O(n) time, O(1) auxiliary space, no input mutation, and no min/max/sorted/sort or copying slice.

## Task 4 — reverse_in_place

Reverse the mutable sequence in place and return None.

Algorithmic intent: mutate the same object, O(n) time, O(1) auxiliary space, and no reversed or full-size copy.

## Task 5 — first_negative_running_sum

Return the first index where the running sum becomes strictly negative, or -1 if it never does.

~~~text
values:        4, -1, -2, -5, 8
running sums:  4,  3,  1, -4, 4
result: 3
~~~

Algorithmic intent: maintain one running-sum variable, stop as soon as the answer is known, O(n) worst-case time, and no repeated sum of prefixes.

## Task 6 — analyse_scores

Return (average, minimum, maximum, number_of_passing_scores).

Scores and passing_score must be in 0..100. Raise ValueError for invalid or empty input.

Algorithmic intent: validate and aggregate in one pass, O(n) time, O(1) auxiliary space, no input mutation, and no sum/min/max/sorted shortcut.

## Required design note

For each task, complete the design template with the contract, state meaning, termination argument, and complexity analysis.

Executable tests provide evidence about behaviour; the design note provides evidence that the algorithm is understood.
