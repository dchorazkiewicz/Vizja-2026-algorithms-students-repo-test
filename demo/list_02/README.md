# List 02 — Searching, Sorting and Divide & Conquer

List 02 is the second end-to-end demonstration of the automated exercise and feedback workflow.

The student tasks are canonical. The depth is on the instructor side: the grader observes correctness, structure, data access, comparisons, writes, stability, adaptivity, recursion and empirical complexity.

## Student tasks

1. `binary_search` — leftmost binary search on a sorted sequence.
2. `insertion_sort_in_place` — stable, adaptive insertion sort.
3. `selection_sort_in_place` — canonical selection sort with limited data movement.
4. `merge_sorted` — stable linear merge of two sorted sequences.
5. `merge_sort` — stable recursive divide-and-conquer sort.
6. `quick_sort_in_place` — in-place quicksort without library sorting.

## Demonstrator structure

~~~text
student_package/
    README.md
    starter.py
    DESIGN_TEMPLATE.md

private_grader/
    README.md
    reference_solution.py
    instrumentation.py
    ast_checks.py
    complexity.py
    evaluate.py
    feedback.py

sample_submissions/
    strong.py
    functionally_correct_but_inefficient.py
    weak.py

tests/
    functional, property, AST, behaviour and complexity checks

evidence/
    curated verified snapshots

generated/
    latest CI-generated reports, feedback drafts and raw test output
~~~

In production, `student_package/` would be published separately. The grader, reference solution and hidden tests would remain private.

## What is measured

### Binary search

The grader records:

- returned index;
- whether the **leftmost** duplicate is returned;
- indices actually visited;
- number of element reads;
- input mutation;
- growth of reads as `n` increases;
- use of linear-search shortcuts or membership checks.

### Insertion sort

The grader records:

- sortedness and permutation preservation;
- in-place behaviour;
- stability for equal keys;
- comparisons and writes;
- behaviour on already-sorted input;
- behaviour on reverse input;
- the contrast between approximately linear best-case comparisons and quadratic worst-case work.

### Selection sort

The grader records:

- sortedness and in-place behaviour;
- comparison count;
- write count;
- nested-loop structure;
- the characteristic `n(n-1)/2` comparison pattern;
- whether an implementation performs far more data movement than canonical selection sort.

### Merge

For `merge_sorted` the grader checks:

- correctness;
- input preservation;
- stability;
- comparison count;
- linear growth.

### Merge sort

The grader checks:

- correctness and permutation preservation;
- stability;
- recursion;
- input preservation;
- comparison growth consistent with `n log n`;
- recursion depth;
- diagnostic memory allocation.

### Quicksort

The grader checks:

- in-place correctness;
- lack of library sorting;
- absence of full-size slice copying;
- recursive structure;
- comparisons, reads and writes;
- recursion depth;
- empirical average-case behaviour on deterministic shuffled inputs.

## Three simulated students

**Strong** follows the intended methods.

**Functionally correct but inefficient** passes the functional requirements while deliberately using the wrong techniques: linear search instead of binary search, built-in sorting, repeated quadratic work, or another algorithm in place of the requested one.

**Weak** contains both correctness defects and method defects, including an unstable insertion sort and a merge implementation that loses duplicates.

This three-profile setup tests the grader itself. The CI run must prove that the grader distinguishes all three cases.

## Engineering characteristics

The demonstration is deliberately built like a small production-quality technical pipeline:

- deterministic inputs for repeatable measurements;
- tests of the grader itself;
- explicit public/private boundaries;
- JSON for machine consumption;
- Markdown for human review;
- JUnit and raw pytest logs;
- commit-SHA provenance;
- generated student-facing feedback;
- GitHub Actions artifacts;
- a bot commit containing the latest generated evidence.

The goal is useful, inspectable behaviour rather than scoring for its own sake.

## Local execution

~~~bash
python -m pip install -r demo/list_02/requirements-dev.txt
pytest demo/list_02/tests -vv
~~~

Generate one report:

~~~bash
python -m demo.list_02.private_grader.evaluate \
  --solution demo/list_02/sample_submissions/functionally_correct_but_inefficient.py \
  --markdown report.md \
  --json report.json
~~~

Generate the corresponding GitHub Issue draft:

~~~bash
python -m demo.list_02.private_grader.feedback \
  --report-json report.json \
  --profile "functionally correct but inefficient" \
  --source-sha example-sha \
  --output issue.md
~~~
