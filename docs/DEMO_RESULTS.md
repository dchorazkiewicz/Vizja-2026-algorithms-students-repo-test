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


---

# List 03 — Binary Trees, BST and AVL Trees

The third demonstrator was executed successfully in GitHub Actions after the feedback rules were reviewed and refined.

- workflow: [List 03 automated assessment demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/runs/35821582928)
- run number: 2
- source commit: 901128068b6a6a58b95eb8eec03eebff2d1b1adf
- result: **success**
- pytest suite: **18 passed**
- pytest stage: **2.39 s**
- evaluator functional checks per profile: **34**
- generated-evidence commit: `4381debe9bb5c0422a77d4d15086fe29b7ce9b47`
- generated-evidence author: **github-actions[bot]**

## List 03 simulated submissions

| Profile | Functional checks | Methodological findings | Key evidence |
|---|---:|---:|---|
| Strong | 34 / 34 | 0 | path-limited BST search, local insertion, global validation, correct rotations, AVL height 7 after 64 ascending inserts |
| Functionally correct but inefficient | 34 / 34 | 6 | full traversal for search, materialised inorder validation, whole-tree AVL rebuild with 2,080 allocations |
| Weak | 14 / 34 | 2 | wrong traversal order, incorrect search branches, duplicates inserted, height off-by-one, local-only validator, missing height maintenance, unbalanced AVL |

## Balanced versus degenerate BST search

For a search miss:

~~~text
balanced tree with 4,095 nodes:
strong implementation → 24 key reads

degenerate right-chain with 512 nodes:
strong implementation → 1,024 key reads
~~~

The repeated key reads come from separate equality/order comparisons, but the structural point is visible: search cost follows tree height `h`.

The functionally correct but inefficient profile materialises a complete in-order traversal:

~~~text
balanced tree with 4,095 nodes:
4,095 key reads
~~~

## Local AVL repair versus rebuilding

For 64 ascending insertions:

~~~text
strong AVL:
64 nodes created
57 rotations
final height 7
valid AVL: yes

functionally correct rebuild:
2,080 nodes created
0 rotations
final height 7
valid AVL: yes
~~~

Both final trees are correct, but the implementation strategy and update cost are fundamentally different.

The cumulative node-allocation experiment makes that difference measurable:

~~~text
strong allocation-growth exponent: 1.000
rebuild allocation-growth exponent: 1.978
~~~

## Structural defects in the weak profile

The weak profile gives useful examples where the final failure is not merely "wrong output":

- in-order traversal is actually pre-order;
- BST search follows the wrong branch direction;
- duplicate insertion changes the tree;
- the height convention is off by one;
- the validator checks only local parent/child order and misses a deeper ancestor-bound violation;
- rotations rewire links but do not update stored heights;
- ascending AVL insertion produces height 64 instead of a logarithmic-height balanced tree.

Checked-in evidence:

- [Strong List 03 submission](../demo/list_03/evidence/strong.md)
- [Functionally correct but inefficient List 03 submission](../demo/list_03/evidence/functionally_correct_but_inefficient.md)
- [Weak List 03 submission](../demo/list_03/evidence/weak.md)
