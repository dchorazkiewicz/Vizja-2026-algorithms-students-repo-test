from demo.list_03.private_grader.evaluate import runtime_observations


def test_balanced_bst_search_is_path_limited(solution):
    report = runtime_observations(solution)
    assert report["bst_contains"]["balanced_key_reads"] <= 32


def test_degenerate_bst_search_exposes_height_dependency(solution):
    report = runtime_observations(solution)
    assert report["bst_contains"]["skewed_key_reads"] >= 500


def test_bst_insert_is_local(solution):
    report = runtime_observations(solution)
    insert = report["bst_insert"]
    assert insert["node_created_for_new_key"] == 1
    assert insert["link_writes_for_new_key"] == 1
    assert insert["node_created_for_duplicate"] == 0


def test_global_validator_rejects_deep_violation(solution):
    report = runtime_observations(solution)
    assert report["is_valid_bst"]["deep_invalid_result"] is False


def test_avl_insert_uses_local_updates(solution):
    report = runtime_observations(solution)
    avl = report["avl_insert"]
    assert avl["valid_avl"] is True
    assert avl["actual_height"] <= 8
    assert avl["nodes_created_across_64_insertions"] == 64
    assert avl["total_rotations"] > 0
