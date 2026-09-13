from app.verification.confidence import ConfidenceEngine


def test_basic_confidence() -> None:
    score = ConfidenceEngine().calculate(0.9)

    assert score == 0.9


def test_memory_confidence_is_combined() -> None:
    score = ConfidenceEngine().calculate(
        verification_score=0.8,
        memory_confidence=1.0,
    )

    assert score == 0.9


def test_tool_verification_improves_confidence() -> None:
    score = ConfidenceEngine().calculate(
        verification_score=0.8,
        tool_verified=True,
    )

    assert score == 0.9


def test_confidence_is_bounded() -> None:
    score = ConfidenceEngine().calculate(
        verification_score=2.0,
        memory_confidence=-1.0,
    )

    assert 0.0 <= score <= 1.0
