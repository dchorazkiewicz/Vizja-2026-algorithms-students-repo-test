from demo.list_03.private_grader.evaluate import methodological_findings, static_observations


def test_reference_has_no_methodological_findings(source_path):
    findings = methodological_findings(static_observations(source_path))
    assert all(not issues for issues in findings.values())
