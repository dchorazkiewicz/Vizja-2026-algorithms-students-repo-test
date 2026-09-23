from pathlib import Path

from demo.list_02.private_grader.evaluate import evaluate


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "sample_submissions"


def test_strong_profile_is_clean():
    report = evaluate(SAMPLES / "strong.py")
    assert report["summary"]["functional_passed"] == report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] == 0
    assert report["runtime"]["binary_search"]["logarithmic_probe"] is True
    assert report["runtime"]["insertion_sort_in_place"]["stable"] is True
    assert report["runtime"]["selection_sort_in_place"]["limited_data_movement"] is True


def test_functionally_correct_but_inefficient_profile_is_detected():
    report = evaluate(SAMPLES / "functionally_correct_but_inefficient.py")
    assert report["summary"]["functional_passed"] == report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] >= 5
    assert report["runtime"]["binary_search"]["logarithmic_probe"] is False
    assert report["runtime"]["selection_sort_in_place"]["limited_data_movement"] is False

    merge_exp = report["complexity"]["merge_sort"]["median_exponent"]
    quick_exp = report["complexity"]["quick_sort"]["median_exponent"]
    assert merge_exp is not None and merge_exp > 1.6
    assert quick_exp is not None and quick_exp > 1.6


def test_weak_profile_has_correctness_and_method_defects():
    report = evaluate(SAMPLES / "weak.py")
    assert report["summary"]["functional_passed"] < report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] >= 3
    assert report["runtime"]["insertion_sort_in_place"]["stable"] is False
