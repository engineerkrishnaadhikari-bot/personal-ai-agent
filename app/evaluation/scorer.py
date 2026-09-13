from app.evaluation.models import EvaluationResult


class EvaluationScorer:
    """Score responses against deterministic expectations."""

    def score(
        self,
        case_id: str,
        response: str,
        expected_keywords: tuple[str, ...],
    ) -> EvaluationResult:
        normalized_response = response.lower()

        if not expected_keywords:
            return EvaluationResult(
                case_id=case_id,
                passed=True,
                score=1.0,
                missing_keywords=(),
            )

        missing = tuple(
            keyword
            for keyword in expected_keywords
            if keyword.lower() not in normalized_response
        )

        score = (
            1.0
            - len(missing) / len(expected_keywords)
        )

        return EvaluationResult(
            case_id=case_id,
            passed=not missing,
            score=round(max(0.0, score), 4),
            missing_keywords=missing,
        )
