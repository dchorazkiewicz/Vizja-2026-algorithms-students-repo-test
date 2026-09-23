from demo.list_03.private_grader.evaluate import complexity_observations


def test_balanced_search_stays_logarithmic_scale(solution):
    report = complexity_observations(solution)
    assert report["bst_contains_balanced"]["max_key_reads"] <= 32


def test_skewed_search_is_linear_in_height(solution):
    report = complexity_observations(solution)
    exponent = report["bst_contains_skewed"]["median_exponent"]
    assert exponent is not None
    assert 0.75 <= exponent <= 1.25


def test_avl_allocations_are_linear_across_insert_sequence(solution):
    report = complexity_observations(solution)
    exponent = report["avl_cumulative_node_allocations"]["median_exponent"]
    assert exponent is not None
    assert 0.75 <= exponent <= 1.25

    heights = report["avl_final_height"]["measurements"]
    assert heights[-1][1] <= 9
