from pathlib import Path

from demo.list_03.private_grader.evaluate import evaluate


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "sample_submissions"


def test_strong_profile_is_clean():
    report = evaluate(SAMPLES / "strong.py")
    assert report["summary"]["functional_passed"] == report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] == 0
    assert report["runtime"]["bst_contains"]["balanced_key_reads"] <= 32
    assert report["runtime"]["avl_insert"]["valid_avl"] is True
    assert report["runtime"]["avl_insert"]["nodes_created_across_64_insertions"] == 64


def test_functionally_correct_but_inefficient_profile_is_detected():
    report = evaluate(SAMPLES / "functionally_correct_but_inefficient.py")
    assert report["summary"]["functional_passed"] == report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] >= 3
    assert report["runtime"]["bst_contains"]["balanced_key_reads"] > 1000
    assert report["runtime"]["avl_insert"]["valid_avl"] is True
    assert report["runtime"]["avl_insert"]["nodes_created_across_64_insertions"] > 1000

    exponent = report["complexity"]["avl_cumulative_node_allocations"]["median_exponent"]
    assert exponent is not None and exponent > 1.5


def test_weak_profile_has_structural_and_correctness_defects():
    report = evaluate(SAMPLES / "weak.py")
    assert report["summary"]["functional_passed"] < report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] >= 2
    assert report["runtime"]["is_valid_bst"]["deep_invalid_result"] is True
    assert report["runtime"]["avl_insert"]["valid_avl"] is False
