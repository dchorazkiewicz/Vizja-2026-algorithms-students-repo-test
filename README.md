# Algorithms and Complexity — Automated Exercise & Feedback Demonstrator

[![List 01 demo](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-01-demo.yml/badge.svg)](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/workflows/list-01-demo.yml)

This repository is a working demonstrator of the technical exercise workflow planned for **Algorithms and Complexity**.

Its scope is deliberately narrow: it shows how programming assignments can be distributed through GitHub, observed from student forks, evaluated with a private automated grader, and turned into versioned technical feedback. Lecture delivery and in-class student management are outside the scope of this repository.

## What this repository demonstrates

The intended production flow is:

~~~text
student assignment
      ↓
official workbook repository
      ↓ fork
student repository
      ↓ commit / push
private versioned mirror
      ↓
private grader
      ↓
technical evidence bound to a commit SHA
      ↓
feedback in GitHub Issue / comment
      ↓
student revision
      ↓
next mirrored version and next report
~~~

The demonstrator keeps the normally separate layers in one public repository so that the complete mechanism can be inspected. In production, the student package would be public while the grader, reference solutions, and hidden tests would remain private.

## Documentation

- [Course syllabus](docs/COURSE_SYLLABUS.md)
- [Task-design topic map](docs/TOPIC_AREAS.md)
- [Why Python is the primary teaching language](docs/PYTHON_RATIONALE.md)
- [Automated feedback pipeline](docs/AUTOMATED_FEEDBACK_PIPELINE.md)
- [What the current demonstration detects](docs/DEMO_RESULTS.md)

The complete lecture notes remain in [Algorithms_and_Complexity](https://github.com/dchorazkiewicz/Algorithms_and_Complexity). This repository is about the exercise and feedback infrastructure.

## Working demonstration: List 01

[List 01 — Contracts, State and Simple Algorithms](demo/list_01/README.md) is the first end-to-end example.

It contains four clearly separated parts:

- **student_package/** — exactly the kind of material that could be published to students;
- **private_grader/** — the instructor-side grader, reference implementation and instrumentation;
- **sample_submissions/** — three simulated student solutions with different quality profiles;
- **tests/** — tests of both the assignment and the grader itself.

GitHub Actions executes the complete laboratory and generates technical reports for all three sample submissions.

## Design principle

A correct output is necessary, but it is not always sufficient evidence that the intended algorithm was implemented.

The grader therefore combines:

- unit tests;
- property-based tests;
- AST analysis;
- runtime instrumentation;
- operation counting;
- early-termination checks;
- empirical complexity experiments;
- side-effect checks;
- memory diagnostics;
- execution tracing.

The purpose is not to reward clever test-specific code. The purpose is to make algorithmic behaviour observable and to give the student precise technical feedback tied to a specific version of their work.
