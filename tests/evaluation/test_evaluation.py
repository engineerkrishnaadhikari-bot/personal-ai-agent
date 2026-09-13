from app.evaluation.models import EvaluationCase
from app.evaluation.runner import EvaluationRunner
from app.evaluation.scorer import EvaluationScorer


def test_scorer_passes_when_all_keywords_match() -> None:
    result = EvaluationScorer().score(
        case_id="TEST-001",
        response=(
            "Smoke testing checks the basic functionality "
            "of the application."
        ),
        expected_keywords=("smoke", "basic functionality"),
    )

    assert result.passed is True
    assert result.score == 1.0
    assert result.missing_keywords == ()


def test_scorer_fails_when_keyword_is_missing() -> None:
    result = EvaluationScorer().score(
        case_id="TEST-002",
        response="This checks the application.",
        expected_keywords=("smoke", "basic functionality"),
    )

    assert result.passed is False
    assert result.score == 0.0
    assert "smoke" in result.missing_keywords
    assert "basic functionality" in result.missing_keywords


def test_runner_calculates_accuracy() -> None:
    responses = {
        "What is smoke testing?": (
            "Smoke testing checks basic functionality."
        ),
        "What is regression testing?": (
            "Regression testing checks changes and "
            "existing functionality."
        ),
    }

    def fake_agent(prompt: str) -> str:
        return responses[prompt]

    cases = [
        EvaluationCase(
            case_id="TEST-001",
            prompt="What is smoke testing?",
            expected_keywords=("smoke", "basic functionality"),
        ),
        EvaluationCase(
            case_id="TEST-002",
            prompt="What is regression testing?",
            expected_keywords=("regression", "existing functionality"),
        ),
    ]

    results, summary = EvaluationRunner(fake_agent).run(cases)

    assert len(results) == 2
    assert summary.total == 2
    assert summary.passed == 2
    assert summary.failed == 0
    assert summary.accuracy == 1.0
