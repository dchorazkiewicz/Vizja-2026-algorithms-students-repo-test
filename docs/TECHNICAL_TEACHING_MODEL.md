# Technical teaching model

## Purpose

The technical environment should help students learn algorithms while also giving them a disciplined way to build, revise and discuss working code.

The goal is not to add tooling for its own sake. Each part of the workflow exists because it makes either the student's work or the instructor's feedback more precise.

## 1. Work on real, versioned artifacts

A solution is not treated as a disposable upload.

The student works in a Git repository, commits changes, receives feedback against a concrete revision and can improve the same artifact.

~~~text
implementation
→ commit
→ technical evidence
→ feedback
→ revision
→ new commit
→ new evidence
~~~

## 2. Separate correctness from implementation quality

A program can return the right answer and still implement the wrong algorithm.

The grader therefore keeps several dimensions separate:

- functional correctness;
- contract compliance;
- algorithmic structure;
- runtime behaviour;
- complexity evidence;
- mutation and side effects;
- memory behaviour;
- structural invariants.

This is more informative than reducing everything to one score.

## 3. Make algorithmic ideas observable

Important theoretical properties are connected to concrete execution.

Examples:

- early termination becomes a measurable number of reads;
- binary search becomes an observable access path;
- stability becomes the preserved order of equal-key identities;
- O(n²) behaviour becomes measurable growth in comparisons or reads;
- BST search becomes a count of visited nodes;
- AVL balancing becomes observable rotations, heights and link updates.

The point is not to replace formal reasoning. It is to give students runtime evidence that can be connected to that reasoning.

## 4. Method-level checks must follow the learning objective

A methodological rule is justified only when it corresponds to the algorithmic concept being taught.

For example:

- banning linear scan in a binary-search task is part of the task itself;
- checking stability in insertion sort is part of the algorithm's required property;
- checking local rotations in AVL insertion distinguishes AVL maintenance from whole-tree reconstruction.

This prevents the grader from turning personal coding preferences into hidden assessment criteria.

The evidence should therefore be explainable in terms of the published task contract.

## 5. Feedback should say what happened and what to improve

A useful feedback item normally contains:

1. the observed fact;
2. the relevant evidence;
3. why it matters for the task;
4. a concrete direction for revision.

~~~text
All functional checks pass.

On 4,096 sorted elements, your search inspected 4,096 values.
The task requires binary search, so the expected access pattern is logarithmic.

Maintain low/high bounds and inspect only the midpoint of the active interval.
~~~

This is intentionally different from an unexplained FAIL.

## 6. Use software-development mechanics where they are educationally useful

The workflow uses:

- Git repositories and forks;
- commits and SHA-based provenance;
- CI;
- private/hidden tests;
- machine-readable reports;
- human-readable review output;
- GitHub Issues/comments for asynchronous feedback.

These are not decorative additions. They make the work reproducible, reviewable and iterative, while exposing students to habits that also make sense in larger software projects.

## 7. Keep automation and educational judgment separate

The automated layer should report facts:

~~~text
functional tests: pass
early termination: missing
observed growth: quadratic
AVL invariant: violated
~~~

It should not silently turn those observations into an irreversible educational decision.

The report is evidence. The decision about what that evidence means remains a separate layer.

## 8. Feedback is also a technical conversation

The generated Issue text is a starting point, not the end of the interaction.

A student can challenge an observation, explain an implementation choice, ask what a metric means, or push a revision. The instructor can respond against the same commit and evidence.

That gives the asynchronous part of the course a useful project-like rhythm:

~~~text
code
→ automated evidence
→ review comment
→ discussion
→ revision
→ new evidence
~~~

Automation improves the quality and consistency of the starting evidence; it does not remove the human review loop.

## 9. Increase depth as the algorithms become richer

- **List 01:** state, control flow, reads/writes, side effects and simple complexity;
- **List 02:** search paths, stability, adaptivity, comparisons, data movement and divide-and-conquer growth;
- **List 03:** tree shape, path length, allocation, link mutation, global invariants, stored metadata and AVL rotations.

The same model can later extend naturally to graphs, heaps, dynamic programming, backtracking or other syllabus areas.

## 10. Preserve reproducibility

A technical result should be identifiable by at least:

~~~text
student repository
+ student commit SHA
+ grader version
+ test-suite version
~~~

That makes later review possible and prevents feedback from becoming detached from the code version it describes.
