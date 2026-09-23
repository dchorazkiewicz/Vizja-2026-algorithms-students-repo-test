# Evidence snapshot — weak submission

## Summary

- functional checks: 25 / 31
- methodological findings: 5

## Correctness defects

Detected failures include:

- binary search returns an occurrence but not the required leftmost duplicate;
- insertion sort breaks stability;
- selection sort has an off-by-one error and misses valid minimum candidates;
- merge drops one of two equal items;
- merge stability therefore also fails.

## Binary search

The implementation still uses logarithmic interval reduction:

- reads for n = 4,096: 26
- logarithmic runtime probe: yes

The technical problem is not the complexity class. It is the leftmost-occurrence contract.

## Insertion sort stability

The tagged result for equal keys is reordered:

~~~text
[(1, 3), (1, 1), (2, 4), (2, 2), (2, 0)]
~~~

The output keys are sorted, but equal-key identities are reversed. This makes the stability defect directly observable.

## Selection sort

For 64 elements:

- observed comparisons: 1,953
- canonical expected comparisons: 2,016

The lower count is not an optimisation: it is evidence that the final candidate range is not fully inspected, consistent with the off-by-one defect.

## Library shortcuts

AST identifies:

- merge_sort implemented with sorted;
- quick_sort_in_place implemented with .sort();
- no requested recursive structure for either task.

The functions return correct sorted outputs for the tested numeric cases, but they do not implement the requested algorithms.
