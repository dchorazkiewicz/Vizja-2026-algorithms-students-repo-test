# Algorithms and Complexity — Automated Exercise & Feedback Demonstrator

[![List 01 demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-01-demo.yml/badge.svg)](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-01-demo.yml)
[![List 02 demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-02-demo.yml/badge.svg)](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-02-demo.yml)
[![List 03 demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-03-demo.yml/badge.svg)](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-03-demo.yml)

This repository is a working proof of concept for the **technical side of programming exercises and feedback** in Algorithms and Complexity.

It shows the complete path from a student-facing assignment to versioned technical evidence and actionable feedback:

~~~text
assignment
   ↓
student fork and commits
   ↓
private mirror of a concrete SHA
   ↓
hidden grader and instrumentation
   ↓
technical report
   ↓
GitHub Issue / comment feedback
   ↓
student revision
   ↓
next version, next report
~~~

The important point is not only automation. It is **what the automation observes and how that evidence is used**.

## What this approach is designed to achieve

- **Students work with real versioned artifacts.** Solutions live in Git repositories and evolve through commits rather than one-off uploads.
- **Correct output is necessary, but not always sufficient.** The grader can also inspect implementation structure, data access, operation counts, side effects, memory behaviour, recursion, invariants and empirical complexity.
- **Feedback is specific and actionable.** A student can be told that a result is correct but a scan is linear instead of logarithmic, a sort is unstable, a tree is being rebuilt instead of locally rebalanced, or an invariant is violated.
- **Every observation is tied to a concrete revision.** Reports are bound to commit SHA, grader version and test-suite version, which makes the process reproducible and auditable.
- **The workflow uses familiar software-development mechanics.** Forks, commits, CI, hidden tests, machine-readable reports and Issue-based review support both learning and disciplined project work.
- **Automation produces technical evidence, not an opaque final grade.** Educational decisions remain separate from the raw measurements.

See [Technical teaching model](docs/TECHNICAL_TEACHING_MODEL.md).

## Three working demonstrations

| Demonstration | Student topic | What the grader can observe |
|---|---|---|
| [List 01 — Contracts, State and Simple Algorithms](demo/list_01/README.md) | simple imperative algorithms | correctness, early exit, repeated passes, reads/writes, slicing, side effects, memory, empirical growth |
| [List 02 — Searching, Sorting and Divide & Conquer](demo/list_02/README.md) | binary search and sorting | comparisons, writes, stability, adaptivity, data movement, recursion, linear vs quadratic vs n log n behaviour |
| [List 03 — Binary Trees, BST and AVL Trees](demo/list_03/README.md) | trees, BST, AVL | visited nodes, path length, link changes, node allocation, global invariants, heights, balance, rotations, local repair vs rebuilding |

Each demonstration contains:

- the material a student could receive;
- a private-grader layer;
- three simulated submissions: **strong**, **functionally correct but inefficient**, and **weak**;
- tests of both the assignment and the grader;
- generated technical reports;
- ready-to-post GitHub Issue feedback drafts;
- raw pytest/JUnit evidence;
- CI-generated evidence committed by `github-actions[bot]`.

## Why the three student profiles matter

The middle profile is deliberately important.

It often passes **all functional checks** while violating the intended algorithmic method.

~~~text
Binary search task, 4,096 elements

strong implementation:
13 reads

functionally correct linear scan:
4,096 reads
~~~

~~~text
Selection-sort task, 64 elements

canonical selection sort:
2,016 comparisons
64 writes

functionally correct bubble-sort substitute:
2,016 comparisons
4,032 writes
~~~

~~~text
AVL insertion, 64 ascending keys

local AVL repair:
64 node allocations
57 rotations
final height 7

functionally correct whole-tree rebuild:
2,080 node allocations
0 rotations
final height 7
~~~

The output can be identical while the algorithmic behaviour is fundamentally different.

## Five-minute tour

1. Open [List 02 student package](demo/list_02/student_package/README.md) to see what a student would receive.
2. Compare the [strong](demo/list_02/sample_submissions/strong.py) and [functionally correct but inefficient](demo/list_02/sample_submissions/functionally_correct_but_inefficient.py) submissions.
3. Read the generated [List 02 feedback for the functionally correct submission](demo/list_02/generated/feedback/functionally-correct-but-inefficient-issue.md).
4. Read the generated [List 03 weak-submission feedback](demo/list_03/generated/feedback/weak-issue.md) to see structural BST/AVL feedback.
5. Open [Verified demonstration evidence](docs/DEMO_RESULTS.md) or the GitHub Actions badges above to confirm that the pipelines actually run and commit their outputs.

## Repository architecture

~~~text
demo/list_xx/
├── student_package/       # material that could be public
├── private_grader/        # instructor-side analysis
├── sample_submissions/    # simulated student work
├── tests/                 # hidden-test equivalent in the demo
├── evidence/              # concise verified snapshots
└── generated/             # latest CI-generated reports and feedback
~~~

In an actual deployment, the student-facing workbook would be separated from the private mirror, grader and hidden tests.

## Design principles

The grader combines independent forms of evidence rather than relying on one signal:

- unit and property-based tests;
- AST analysis;
- runtime instrumentation;
- operation counting;
- early-termination and access-pattern checks;
- empirical complexity experiments;
- side-effect and mutation checks;
- memory diagnostics;
- recursion and structural-invariant checks.

Python is used deliberately because its low syntactic overhead and dynamic runtime make deep instrumentation possible without forcing unnatural APIs on students. See [Why Python](docs/PYTHON_RATIONALE.md).

## Documentation

- [Technical teaching model](docs/TECHNICAL_TEACHING_MODEL.md)
- [Automated feedback pipeline](docs/AUTOMATED_FEEDBACK_PIPELINE.md)
- [Verified demonstration evidence](docs/DEMO_RESULTS.md)
- [Why Python is the primary teaching language](docs/PYTHON_RATIONALE.md)
- [Task-design topic map](docs/TOPIC_AREAS.md)
- [Scope and provenance](docs/SCOPE_AND_PROVENANCE.md)
- [Source syllabus reference](docs/COURSE_SYLLABUS.md)

## Scope

This is a demonstrator of how I would structure this part of the course if responsible for it. It is not an official university repository, an official grading policy, or a claim that I teach the lecture component.

The separate \`Algorithms_and_Complexity\` repository is a syllabus-to-learning-material proof of concept. The only shared foundation between the two projects is the source syllabus.
