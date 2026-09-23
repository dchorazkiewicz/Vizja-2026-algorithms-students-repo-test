# Evidence snapshot — weak submission

Source profile: demo/list_01/sample_submissions/weak.py

## Summary

- functional checks: 9 / 23
- methodological findings: 7

## Functional problems

Examples include:

- clamp solves the wrong problem for most tested inputs;
- first_index returns the last occurrence instead of the first;
- min_max fails for important domains such as all-negative input and empty input;
- reverse_in_place returns a new list instead of mutating the supplied object;
- analyse_scores does not implement the required validation contract.

## Methodological findings

- reverse_in_place uses list/reversed instead of the required in-place algorithm;
- first_negative_running_sum uses sum and slicing;
- analyse_scores uses several built-in shortcuts and no explicit task-level loop structure.

## Quadratic behaviour detected despite correct outputs

The running-sum task passes all four functional checks, but repeatedly evaluates prefixes.

Measured element reads:

| n | reads |
|---:|---:|
| 64 | 2,080 |
| 128 | 8,256 |
| 256 | 32,896 |
| 512 | 131,328 |

Doubling exponents:

- 1.989
- 1.994
- 1.997

Median exponent: 1.994.

This is strong empirical evidence of approximately quadratic growth.

The same implementation also showed much higher peak allocation in the diagnostic memory probe because it repeatedly creates prefix slices.

Interpretation: the grader can identify a technically important algorithmic defect even when the returned answers are correct.
