from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationResult:
    passed: bool
    score: float
    reasons: tuple[str, ...]


class Verifier:
    """Perform deterministic checks on agent output."""

    def verify(
        self,
        prompt: str,
        response: str,
    ) -> VerificationResult:
        reasons: list[str] = []

        if not prompt.strip():
            return VerificationResult(
                passed=False,
                score=0.0,
                reasons=("Prompt is empty.",),
            )

        if not response.strip():
            return VerificationResult(
                passed=False,
                score=0.0,
                reasons=("Response is empty.",),
            )

        score = 1.0

        if len(response.strip()) < 5:
            score -= 0.4
            reasons.append("Response is unusually short.")

        if len(response) > 20_000:
            score -= 0.2
            reasons.append("Response is unusually long.")

        score = max(0.0, min(1.0, score))

        if not reasons:
            reasons.append("Basic response checks passed.")

        return VerificationResult(
            passed=score >= 0.8,
            score=score,
            reasons=tuple(reasons),
        )



