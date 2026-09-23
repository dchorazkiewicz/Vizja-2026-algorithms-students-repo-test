# Evidence snapshot — strong submission

Source profile: demo/list_01/sample_submissions/strong.py

## Summary

- functional checks: 23 / 23
- methodological findings: 0

## Selected runtime evidence

### first_index

- result: 1
- element reads: 2
- visited indices: [0, 1]
- early termination: yes
- writes: 0

### min_max

- result: (0, 99)
- element reads: 101
- comparisons: 198
- slices: 0
- writes: 0

### reverse_in_place

- final state correct: yes
- reads: 20
- writes: 20
- slice reads/writes: 0 / 0

### first_negative_running_sum

- result: 0
- reads before return: 1
- early termination: yes

### analyse_scores

- reads: 6
- writes: 0
- slices: 0

## Empirical growth

For the linear tasks, doubling input size approximately doubles measured element reads.

- first_index median exponent: 1.000
- min_max median exponent: 0.994
- first_negative_running_sum median exponent: 1.000
- analyse_scores median exponent: 1.000

Interpretation: the implementation is both functionally correct and consistent with the intended algorithmic structure.
