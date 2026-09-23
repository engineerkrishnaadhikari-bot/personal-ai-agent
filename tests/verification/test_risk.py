from app.verification.risk import RiskEngine, RiskLevel


def test_normal_question_is_low_risk() -> None:
    assert (
        RiskEngine().classify("explain regression testing")
        == RiskLevel.LOW
    )


def test_git_commit_is_medium_risk() -> None:
    assert (
        RiskEngine().classify("git commit changes")
        == RiskLevel.MEDIUM
    )


def test_delete_file_is_high_risk() -> None:
    assert (
        RiskEngine().classify("delete this file")
        == RiskLevel.HIGH
    )


def test_force_push_is_critical() -> None:
    assert (
        RiskEngine().classify("git force push")
        == RiskLevel.CRITICAL
    )
