from demo.list_02.private_grader.ast_checks import function_metrics, function_node, parse_file


def metrics(source_path, name):
    return function_metrics(function_node(parse_file(source_path), name))


def test_binary_search_structure(source_path):
    item = metrics(source_path, "binary_search")
    assert item["max_loop_depth"] >= 1
    assert set(item["calls"]).isdisjoint({"index", "bisect", "bisect_left", "bisect_right"})
    assert item["slice"] is False
    assert item["membership"] is False


def test_insertion_sort_structure(source_path):
    item = metrics(source_path, "insertion_sort_in_place")
    assert item["max_loop_depth"] >= 2
    assert set(item["calls"]).isdisjoint({"sorted", "sort"})
    assert item["slice"] is False


def test_selection_sort_structure(source_path):
    item = metrics(source_path, "selection_sort_in_place")
    assert item["max_loop_depth"] >= 2
    assert set(item["calls"]).isdisjoint({"sorted", "sort"})
    assert item["slice"] is False


def test_merge_sorted_structure(source_path):
    item = metrics(source_path, "merge_sorted")
    assert item["max_loop_depth"] >= 1
    assert set(item["calls"]).isdisjoint({"sorted", "sort"})


def test_merge_sort_structure(source_path):
    item = metrics(source_path, "merge_sort")
    assert "merge_sort" in item["recursive_functions"]
    assert set(item["calls"]).isdisjoint({"sorted", "sort"})


def test_quick_sort_structure(source_path):
    item = metrics(source_path, "quick_sort_in_place")
    assert item["max_loop_depth"] >= 1
    assert item["recursive_functions"]
    assert set(item["calls"]).isdisjoint({"sorted", "sort"})
    assert item["slice"] is False
