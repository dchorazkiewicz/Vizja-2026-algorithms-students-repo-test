from pathlib import Path

from demo.list_01.private_grader.evaluate import evaluate


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "sample_submissions"


def test_strong_profile_is_clean():
    report = evaluate(SAMPLES / "strong.py")
    assert report["summary"]["functional_passed"] == report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] == 0
    assert report["runtime"]["first_index"]["early_exit"] is True
    assert report["runtime"]["first_negative_running_sum"]["early_exit"] is True


def test_functionally_correct_profile_exposes_method_issues():
    report = evaluate(SAMPLES / "functionally_correct_but_inefficient.py")
    assert report["summary"]["functional_passed"] == report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] >= 5
    assert report["runtime"]["first_index"]["early_exit"] is False
    assert report["runtime"]["min_max"]["iterations"] >= 2


def test_weak_profile_has_correctness_and_method_problems():
    report = evaluate(SAMPLES / "weak.py")
    assert report["summary"]["functional_passed"] < report["summary"]["functional_total"]
    assert report["summary"]["method_issue_count"] >= 5
    assert report["runtime"]["first_index"]["early_exit"] is False

    growth = report["complexity"]["first_negative_running_sum"]["median_exponent"]
    assert growth is not None
    assert growth > 1.7
