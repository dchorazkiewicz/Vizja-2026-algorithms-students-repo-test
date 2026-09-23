import pytest

from playground.list_01_foundations.grader.complexity import empirical_exponent
from playground.list_01_foundations.grader.tracked import TrackedSequence


def read_cost(function, values, *args):
    tracked = TrackedSequence(values)
    function(tracked, *args)
    return tracked.reads


@pytest.mark.parametrize("name,args", [
    ("first_index", (10**9,)),
    ("min_max", ()),
    ("first_negative_running_sum", ()),
])
def test_linear_read_growth(solution, name, args):
    function = getattr(solution, name)

    if name == "first_negative_running_sum":
        data_n = [1] * 256
        data_2n = [1] * 512
    elif name == "first_index":
        data_n = list(range(256))
        data_2n = list(range(512))
    else:
        data_n = list(range(256))
        data_2n = list(range(512))

    c1 = read_cost(function, data_n, *args)
    c2 = read_cost(function, data_2n, *args)
    p = empirical_exponent(c1, c2)

    assert 0.75 <= p <= 1.25


def test_analyse_scores_linear_read_growth(solution):
    c1 = read_cost(solution.analyse_scores, [50] * 256, 50)
    c2 = read_cost(solution.analyse_scores, [50] * 512, 50)
    p = empirical_exponent(c1, c2)
    assert 0.75 <= p <= 1.25
