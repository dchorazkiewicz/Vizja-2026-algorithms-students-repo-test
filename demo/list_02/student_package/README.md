# List 02 — Searching, Sorting and Divide & Conquer

Implement the functions in `starter.py`.

The emphasis is on implementing the requested algorithm, not only reproducing the final output.

## Task 1 — binary_search

~~~python
def binary_search(values, target) -> int:
    ...
~~~

Precondition: `values` is sorted in nondecreasing order.

Return the **leftmost** index containing `target`, or `-1` if the target is absent.

Requirements:

- use binary search;
- do not modify the input;
- worst-case time `O(log n)`;
- auxiliary space `O(1)`;
- do not use `.index()`, `bisect`, membership search, or linear scanning.

## Task 2 — insertion_sort_in_place

~~~python
def insertion_sort_in_place(values) -> None:
    ...
~~~

Sort the mutable sequence in nondecreasing order.

Requirements:

- insertion sort;
- stable;
- modify the same object;
- return `None`;
- `O(1)` auxiliary space;
- quadratic worst case;
- adaptive behaviour on already-sorted data;
- no `sorted()`, `.sort()`, or full-size copying.

## Task 3 — selection_sort_in_place

~~~python
def selection_sort_in_place(values) -> None:
    ...
~~~

Sort the mutable sequence in nondecreasing order.

Requirements:

- canonical selection sort;
- modify the same object;
- return `None`;
- `O(1)` auxiliary space;
- `O(n²)` comparisons;
- at most one swap per outer iteration;
- no `sorted()`, `.sort()`, or full-size copying.

Stability is not required.

## Task 4 — merge_sorted

~~~python
def merge_sorted(left, right) -> list:
    ...
~~~

Precondition: both inputs are sorted.

Return one sorted list containing all elements from both inputs.

Requirements:

- stable;
- do not modify either input;
- `O(n + m)` time;
- result storage `O(n + m)`;
- no `sorted()` or `.sort()`.

When equal keys are encountered, the element from `left` must be emitted first.

## Task 5 — merge_sort

~~~python
def merge_sort(values) -> list:
    ...
~~~

Return a new sorted list and leave the input unchanged.

Requirements:

- recursive divide and conquer;
- stable;
- use a merge step;
- `O(n log n)` time;
- `O(n)` auxiliary storage;
- no `sorted()` or `.sort()`.

## Task 6 — quick_sort_in_place

~~~python
def quick_sort_in_place(values) -> None:
    ...
~~~

Sort the mutable sequence in place.

Requirements:

- quicksort-style partitioning;
- return `None`;
- modify the same object;
- no `sorted()`, `.sort()`, or full-size slice copy;
- expected/average `O(n log n)` behaviour on non-adversarial input.

Stability is not required.

## Design note

Complete `DESIGN_TEMPLATE.md` for each task. In this list, explicitly discuss:

- the key comparison operation;
- expected data movement;
- stability where applicable;
- best/worst/average behaviour where relevant;
- why the implementation uses the requested algorithm rather than only producing a sorted result.
