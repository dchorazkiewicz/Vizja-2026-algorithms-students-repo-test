# Private grader layer — List 03

This directory demonstrates tree-specific instructor-side analysis.

## Evidence sources

**Functional evidence**

- traversal order;
- BST search contract;
- duplicate handling;
- insertion result;
- height convention;
- global BST validation;
- rotation shape;
- AVL balance and stored heights.

**AST evidence**

- recursive traversal/height/validation;
- use of full in-order traversal inside path-search tasks;
- whole-tree sorting/rebuilding;
- presence or absence of AVL rotation calls.

**Runtime tree instrumentation**

The grader supplies transparent tree nodes whose properties record:

- key reads;
- key comparisons;
- left/right reads;
- left/right writes;
- height reads/writes;
- node allocations.

This lets the same student code run naturally while the grader observes how it interacts with the tree.

**Shape-sensitive complexity evidence**

BST operations are measured on both balanced and degenerate trees. The reports therefore show directly that the relevant parameter is tree height `h`, not simply node count `n`.

**AVL evidence**

The grader patches the provided `Node` constructor with an instrumented equivalent and wraps `rotate_left` / `rotate_right` to count real rotation calls.

This makes it possible to distinguish:

- local AVL repair;
- whole-tree rebuilding;
- plain unbalanced BST insertion.

The report keeps these facts separate and turns them into targeted revision feedback.
