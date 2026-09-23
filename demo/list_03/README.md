# List 03 — Binary Trees, BST and AVL Trees

List 03 is the third end-to-end demonstration of the automated exercise and feedback workflow.

The student-facing tasks are canonical tree algorithms. The private grader goes much deeper: it observes how the tree is traversed and modified, checks structural invariants, counts allocations and pointer changes, measures recursion, and verifies AVL rotations.

## Student tasks

1. `inorder_keys` — recursive in-order traversal.
2. `bst_contains` — search along one BST path.
3. `bst_insert` — insert one key without rebuilding the tree.
4. `bst_height` — recursive tree height.
5. `is_valid_bst` — global BST invariant validation.
6. `rotate_left` — canonical AVL left rotation.
7. `rotate_right` — canonical AVL right rotation.
8. `avl_insert` — recursive AVL insertion with height maintenance and rotations.

## Why trees are a useful demonstration

For arrays and sorting, the grader can count reads, writes and comparisons. Trees add a richer structural dimension.

The grader can observe:

- which node keys are visited;
- how often `left` and `right` are followed;
- how many child links are changed;
- how many new nodes are allocated;
- actual tree height;
- recursion depth;
- whether the global BST ordering invariant holds;
- whether stored AVL heights are correct;
- whether every balance factor is in `[-1, 1]`;
- how many left and right rotations are executed;
- whether an implementation rebuilds the entire tree instead of performing local rotations.

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
    functional, property, AST, structural, runtime and complexity checks

evidence/
    curated verified snapshots

generated/
    latest CI-generated reports, Issue drafts, pytest log and JUnit XML
~~~

In production, only the student package would be public. The grader, reference implementation and hidden tests would remain private.

## Three simulated students

**Strong** implements the requested tree algorithms directly.

**Functionally correct but inefficient** returns correct answers but deliberately uses expensive alternatives: full in-order traversal for BST search, materialising all keys to validate the tree, and rebuilding a balanced tree after every AVL insertion instead of performing local rotations.

**Weak** contains realistic structural defects: pre-order instead of in-order traversal, incorrect BST branch selection, duplicate insertion, an off-by-one height convention, a local-only BST validator, and AVL insertion without balancing.

## Engineering characteristics

The tree demonstrator keeps the same production-oriented properties as Lists 01 and 02:

- deterministic probes;
- tests of the grader itself;
- explicit public/private boundaries;
- JSON and Markdown evidence;
- JUnit and raw pytest logs;
- source commit provenance;
- student-facing GitHub Issue drafts;
- GitHub Actions artifacts;
- CI-generated evidence committed by `github-actions[bot]`.

The technical report keeps observations separate instead of collapsing them into one opaque score.

## Local execution

~~~bash
python -m pip install -r demo/list_03/requirements-dev.txt
pytest demo/list_03/tests -vv
~~~

Generate a report:

~~~bash
python -m demo.list_03.private_grader.evaluate \
  --solution demo/list_03/sample_submissions/functionally_correct_but_inefficient.py \
  --markdown report.md \
  --json report.json
~~~


## Verified GitHub Actions execution

The reviewed final run is [List 03 automated assessment demo — run #2](https://github.com/dchorazkiewicz/Vizja-2026-algorithms-students-repo-test/actions/runs/35821582928).

The pytest stage completed with **18 passed in 2.39 s**. The embedded evaluator also ran **34 functional checks per simulated submission**.

GitHub Actions generated the reports and Issue feedback drafts, uploaded the raw evidence, and committed the latest output back to the repository as:

\`4381debe9bb5c0422a77d4d15086fe29b7ce9b47 — Update generated List 03 evidence [skip ci]\`

The commit author is \`github-actions[bot]\`.

See:

- [curated evidence](evidence/)
- [latest CI-generated evidence](generated/)
