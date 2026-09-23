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
