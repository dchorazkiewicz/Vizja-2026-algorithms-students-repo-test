# List 02 — automated technical feedback

Analysed revision: `344fb61b1657905e9ce346fb8e5df6b19195212e`
Demonstration profile: **weak**

## Summary

- functional checks: **25/31**
- methodological findings: **5**

## Correctness issues

- `binary_search`: 4/5 checks passed; failing cases: leftmost-duplicate.
- `insertion_sort_in_place`: 5/6 checks passed; failing cases: stable.
- `selection_sort_in_place`: 3/5 checks passed; failing cases: duplicates, reverse.
- `merge_sorted`: 3/5 checks passed; failing cases: duplicates, stable.

## Implementation observations

- `merge_sort`: banned shortcut calls: sorted; required recursive structure not detected.
- `quick_sort_in_place`: loop nesting too shallow for requested method: 0; banned shortcut calls: sort; required recursive structure not detected.

## Stability

The insertion-sort probe changes the relative order of equal keys.

Insertion sort in this task must be stable. Shift only elements that are strictly greater than the key.

---

This feedback is generated from versioned technical evidence. It is intended to support revision of the implementation and is not a standalone final grade.
