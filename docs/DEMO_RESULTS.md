# Demonstration results

The polished List 01 demonstrator has been executed successfully in GitHub Actions.

- workflow: [List 01 automated assessment demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/runs/35817893090)
- run number: 1
- commit: d1e8c1d6fb6cc3e5f791b24b9204c35d36ae7d17
- result: **success**
- test suite: **58 passed**
- pytest stage: **2.30 s**

## Three simulated submissions

| Profile | Functional checks | Methodological findings | Interpretation |
|---|---:|---:|---|
| Strong | 23 / 23 | 0 | Correct results and intended algorithmic method |
| Functionally correct but inefficient | 23 / 23 | 7 | Correct outputs, but several method and efficiency issues are observable |
| Weak | 9 / 23 | 7 | Both correctness and algorithmic problems are present |

Checked-in evidence snapshots:

- [Strong submission](../demo/list_01/evidence/strong.md)
- [Functionally correct but inefficient](../demo/list_01/evidence/functionally_correct_but_inefficient.md)
- [Weak submission](../demo/list_01/evidence/weak.md)

## Why the middle profile matters

The middle submission passes **all 23 functional checks**.

A conventional output-only test suite could therefore report success.

The deeper grader still detects:

- missing early termination in first_index;
- two complete passes in min_max;
- slicing in reverse_in_place;
- repeated traversals in analyse_scores;
- built-in shortcuts that bypass the intended exercise.

This is the central point of the demonstrator: correctness and algorithmic method are separate dimensions.

## Quadratic behaviour detected automatically

The weak running-sum implementation repeatedly evaluates sum over a growing slice.

Its functional checks for that task pass, but the measured reads are:

~~~text
64   →   2,080
128  →   8,256
256  →  32,896
512  → 131,328
~~~

The measured doubling exponent converges to approximately 2.0, exposing the quadratic implementation.

## Evidence retention

Each workflow run publishes:

- Markdown reports;
- JSON reports;
- JUnit XML;
- pytest log.

Those remain available as GitHub Actions artifacts for the configured retention period. The concise evidence snapshots committed to this repository preserve the key demonstration even after transient CI artifacts expire.


---

# List 02 — Searching, Sorting and Divide & Conquer

The second demonstrator has also been executed successfully in GitHub Actions.

- workflow: [List 02 automated assessment demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/runs/35820072440)
- run number: 4
- source commit: 9e0b0f7a95deaeb7cc845fe8cd653ecd516efdf7
- result: **success**
- test suite: **31 passed**
- pytest stage: **2.70 s**
- generated-evidence commit: `1ed9cce2104d8f5f365254ad8ee8ac1b01bb835b`
- generated-evidence author: **github-actions[bot]**

## List 02 simulated submissions

| Profile | Functional checks | Methodological findings | Key evidence |
|---|---:|---:|---|
| Strong | 31 / 31 | 0 | logarithmic binary search, stable/adaptive insertion sort, canonical selection-sort counts, linear merge, n log n divide-and-conquer growth |
| Functionally correct but inefficient | 31 / 31 | 5 | linear search, library sorting, excessive writes, quadratic merge, quadratic substitutes for merge sort and quicksort |
| Weak | 25 / 31 | 5 | leftmost-search contract defect, unstable insertion sort, selection off-by-one, duplicate loss in merge, library shortcuts |

Checked-in evidence:

- [Strong List 02 submission](../demo/list_02/evidence/strong.md)
- [Functionally correct but inefficient List 02 submission](../demo/list_02/evidence/functionally_correct_but_inefficient.md)
- [Weak List 02 submission](../demo/list_02/evidence/weak.md)

## A useful contrast

For binary search on 4,096 elements:

~~~text
strong implementation: 13 reads
functionally correct linear scan: 4,096 reads
~~~

For the selection-sort task on 64 reverse-ordered elements:

~~~text
canonical selection sort: 2,016 comparisons, 64 writes
bubble-sort substitute:   2,016 comparisons, 4,032 writes
~~~

For the linear merge task:

~~~text
strong merge exponent: 1.003
quadratic substitute:  1.984
~~~

The second list therefore demonstrates why the grader records multiple dimensions rather than reducing technical behaviour to a single pass/fail result.
