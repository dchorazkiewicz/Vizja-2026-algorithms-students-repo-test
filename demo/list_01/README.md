# List 01 — Contracts, State and Simple Algorithms

This directory is the first complete demonstration of the exercise workflow.

The tasks are intentionally simple. The point is to show how much useful information can be extracted automatically from small Python implementations.

## Directory structure

~~~text
student_package/
    README.md
    starter.py
    DESIGN_TEMPLATE.md

private_grader/
    README.md
    reference_solution.py
    evaluate.py
    instrumentation.py
    ast_checks.py
    complexity.py

sample_submissions/
    strong.py
    functionally_correct_but_inefficient.py
    weak.py

tests/
    functional, AST, runtime and complexity checks

evidence/
    curated verified snapshots

generated/
    CI-generated reports, logs and Issue feedback drafts
~~~

In production, student_package would live in the public workbook. private_grader and tests would live in a private instructor-controlled repository. They are colocated here only so this repository can demonstrate the complete system.

## What the grader observes

For these small tasks the demonstrator already inspects functional correctness, generated cases, AST structure, forbidden shortcuts, loop count and nesting, slicing, input reads and writes, visited indices, early termination, comparison counts, repeated passes, empirical growth, mutation, stdout/stderr, line-level execution traces, and diagnostic memory allocation.

The tests also validate the grader itself against three deliberately different sample submissions.

## Sample profiles

**Strong** is functionally correct and follows the intended algorithmic method.

**Functionally correct but inefficient** produces correct outputs while intentionally using shortcuts, unnecessary passes, or avoidable copying.

**Weak** contains both correctness defects and algorithmic defects. One task deliberately returns correct answers with a quadratic implementation so that the complexity instrumentation can expose the problem.

## Running locally

~~~bash
python -m pip install -r demo/list_01/requirements-dev.txt
pytest demo/list_01/tests -vv
~~~

Generate one technical report:

~~~bash
python -m demo.list_01.private_grader.evaluate \
  --solution demo/list_01/sample_submissions/functionally_correct_but_inefficient.py \
  --markdown report.md \
  --json report.json
~~~

## Continuous integration

GitHub Actions runs the complete laboratory on every relevant change. It executes the tests, verifies that the grader distinguishes all three sample profiles, generates Markdown and JSON reports, renders GitHub Issue feedback drafts, publishes the reports in the Actions summary, uploads the raw evidence as an artifact, and commits the latest generated evidence to `generated/`.

The workflow is part of the demonstration: it proves that the inspection described here is executable rather than only conceptual.


## Captured evidence

A successful CI run is preserved in [evidence/](evidence/) as concise curated snapshots. The latest machine-generated evidence is committed by GitHub Actions to [generated/](generated/), including the raw pytest log, JUnit XML, Markdown/JSON reports, run metadata, and ready-to-post GitHub Issue feedback drafts.
