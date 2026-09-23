from app.verification.verifier import Verifier


def test_valid_response_passes() -> None:
    result = Verifier().verify(
        prompt="What is smoke testing?",
        response="Smoke testing checks the basic functionality of an application.",
    )

    assert result.passed is True
    assert result.score == 1.0


def test_empty_prompt_fails() -> None:
    result = Verifier().verify(
        prompt=" ",
        response="A valid response.",
    )

    assert result.passed is False
    assert result.score == 0.0


def test_empty_response_fails() -> None:
    result = Verifier().verify(
        prompt="Explain testing.",
        response=" ",
    )

    assert result.passed is False
    assert result.score == 0.0


def test_very_short_response_is_flagged() -> None:
    result = Verifier().verify(
        prompt="Explain testing.",
        response="Yes",
    )

    assert result.passed is False
    assert result.score == 0.6
