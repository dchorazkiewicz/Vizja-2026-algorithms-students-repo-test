# Why Python is the primary teaching language

## Principle

The course is about **algorithms**, not about mastering one programming language.

The implementation language should make the algorithm easy to express, execute, inspect, and test while adding as little language-specific ceremony as possible.

Python is the default language for the exercise infrastructure because it supports that goal exceptionally well.

## Low syntactic overhead

For introductory and intermediate algorithm work, Python lets students focus on state, control flow, invariants, correctness, termination, data-access patterns, and computational cost instead of spending disproportionate effort on type declarations, templates, memory-management syntax, or project scaffolding.

This does not make Python the only valid language. The same algorithms can be implemented in C++ or Java. Python is chosen because it keeps the representation close to the algorithmic idea.

## Natural runtime instrumentation

Python's dynamic object model allows the grader to supply controlled objects that behave like normal sequences or values.

A student can write natural code such as:

~~~python
for index in range(len(values)):
    if values[index] == target:
        return index
~~~

while the grader can transparently record which indices were read, how many reads occurred, whether the input was written to, how many iterations were started, whether slicing occurred, and how many comparisons were executed.

The instrumentation remains on the instructor side. The student does not need to write logging code just to make the algorithm observable.

## Native AST support

Python's standard ast module exposes the parsed structure of a submission without executing it.

This makes it straightforward to inspect explicit iteration, nested loops, recursion, slicing, list comprehensions, built-in shortcuts, unexpected imports, print calls, and global state.

AST analysis does not prove algorithmic complexity by itself. It is one independent source of evidence that can be combined with runtime measurements.

## Multiple independent forms of evidence

The grader combines functional unit tests, property-based tests, AST structure, instrumented execution, operation counts, empirical growth experiments, side-effect checks, memory diagnostics, and termination limits.

A correct result is therefore separated from the question of whether the intended algorithmic method was used.

## Complexity as an observable property

For many exercises we can measure operations that are closer to the algorithm than wall-clock time: element reads, writes, comparisons, swaps, recursive calls, visited vertices, or inspected edges.

By running the same implementation for increasing input sizes, we can observe whether the measured cost behaves approximately like constant, linear, linearithmic, quadratic, or another growth class.

This remains empirical evidence rather than a formal proof of Big O complexity, but it is highly useful for automated feedback.

## Design rule

**Instrument as deeply as useful, but do not distort the student's programming interface merely to make grading easier.**

The assignment should present a natural function contract. The complexity of observation belongs to the grader.

Python makes that separation unusually easy, which is why it is the primary teaching language for this system.
