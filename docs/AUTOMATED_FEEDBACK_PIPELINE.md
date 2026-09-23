# Automated student-work and feedback pipeline

## Scope

This document describes only the asynchronous technical workflow around programming assignments.

It does not define lecture delivery, classroom discussion, attendance, or general student management. Those belong to a separate operational layer.

## Design goals

The pipeline is designed around five properties:

- **reproducibility** — every report refers to a concrete code revision;
- **separation of concerns** — student material, mirrors, graders and educational state have different responsibilities;
- **actionable feedback** — reports explain observable implementation behaviour rather than returning only a score;
- **iteration** — a correction creates a new version and a new report without erasing earlier evidence;
- **automation of repeatable work** — deterministic technical checks are applied consistently.

## Production model

The intended system separates four responsibilities.

### 1. Student workbook

The public workbook contains only material the student should receive: assignment statements, required function signatures, starter code, explicit contracts and constraints, and optional design templates.

It does not contain the instructor's reference implementation or hidden tests.

### 2. Student fork

Each student works in their own fork. The fork is the student's versioned workspace and contains the sequence of commits that shows the evolution of their solution.

### 3. Private mirror

The instructor-side mirror records what was actually observed in the student's repository.

Each observation should be tied to a concrete commit SHA and preserve enough information to reproduce the technical assessment later.

The mirror can also preserve Issue and comment snapshots when GitHub communication is part of the workflow.

### 4. Private grader

The grader contains the material that must remain instructor-side: hidden unit tests, property-based tests, AST rules, runtime instrumentation, operation-count experiments, memory and side-effect checks, reference implementations, and report generation.

In production, untrusted student code should execute in an isolated environment with no repository write token or unrelated secrets, restricted network access where appropriate, and explicit CPU, memory and time limits. The public demonstrator shows the grading logic; sandbox hardening belongs to the deployment layer.

## End-to-end flow

~~~text
assignment published
      ↓
student forks workbook
      ↓
student commits a solution
      ↓
mirror observes commit SHA
      ↓
grader evaluates that exact version
      ↓
versioned technical report
      ↓
feedback is prepared
      ↓
Issue or comment is published to the student
      ↓
student revises the implementation
      ↓
new commit is mirrored and evaluated again
~~~

## Technical report

A report should record student/repository identity, commit SHA, observation time, grader version, test-suite version, missing files or functions, functional results, AST findings, runtime measurements, empirical complexity measurements, memory diagnostics, and any timeout or execution error.

The report is technical evidence, not the final educational decision.

## Versioning

Reports must not overwrite one another.

~~~text
commit A → report A
commit B → report B
commit C → report C
~~~

This makes improvement and regression visible over time and ensures that feedback always refers to a specific version of the student's work.

## Feedback through GitHub

A technical report can be condensed into student-facing feedback.

The intended interaction is not one-way. An Issue or comment can become a compact technical review thread: the report identifies an observation, the student can respond or revise the implementation, and a later report can show whether the relevant behaviour changed.

~~~text
Task 05

All functional checks pass.

The implementation recomputes each prefix sum and creates a new slice on every iteration.
Observed read growth is approximately quadratic.

Try maintaining one running-sum variable and processing each element at most once.

Analysed commit: abc123
~~~

The feedback can be posted as a GitHub Issue or comment. The student may reply or push a correction, producing the next iteration of the same loop.

## Periodic automation

A simple production scheduler can check active forks, mirror only changed HEADs, run the grader, store a report, compare it with the previous report, and prepare feedback or an attention item.

The same design can later be event-driven.

## Idempotence

A useful evaluation key is:

~~~text
repository
+ commit SHA
+ grader version
+ test-suite version
~~~

Re-running an identical key should reproduce the same logical result. A new evaluation is justified when the student code, grader, tests, or configuration changes.

## Technical evidence versus educational decision

The automated system may establish facts such as: all functional tests pass, early termination is missing, slicing was detected, observed cost is approximately quadratic, or a required file is missing.

Those are technical observations.

Whether they imply acceptance, revision, a warning, a discussion, or no action is a separate educational decision. This separation keeps the audit trail clear and prevents a change in the grader from silently rewriting past teaching decisions.

## Relation to Vizja_classes_databases

The technical pipeline can later publish semantic events to Vizja_classes_databases, for example: a new student version was observed, a grader run completed, a task passes functional checks, a complexity concern was detected, a required artifact is missing, feedback was published, the student replied, or a newer revision is available.

Full snapshots and raw grader logs can remain in the mirror/grader layer, while Vizja_classes_databases stores the educational meaning and current operational state.


## Production potential

The current repository proves the analytical core with simulated submissions and real CI execution.

A production deployment can extend the same model without changing the fundamental evidence format:

~~~text
real fork observation
→ mirror exact SHA
→ isolated grader run
→ versioned report
→ feedback publication
→ student response/revision
→ next observed SHA
~~~

Likely extensions include scheduled or event-driven mirror updates, automatic Issue/comment publication, longitudinal comparisons between revisions, and integration with the class database for current state and instructor attention queues.

These are deployment extensions rather than prerequisites for the current demonstrator to show the grading and feedback model.
