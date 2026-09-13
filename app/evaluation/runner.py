from collections.abc import Callable

from app.evaluation.models import (
    EvaluationCase,
    EvaluationResult,
    EvaluationSummary,
)
from app.evaluation.scorer import EvaluationScorer


class EvaluationRunner:
    """Run deterministic agent evaluation cases."""

    def __init__(
        self,
        agent_callable: Callable[[str], str],
    ) -> None:
        self.agent_callable = agent_callable
        self.scorer = EvaluationScorer()

    def run(
        self,
        cases: list[EvaluationCase],
    ) -> tuple[list[EvaluationResult], EvaluationSummary]:
        results: list[EvaluationResult] = []

        for case in cases:
            response = self.agent_callable(case.prompt)

            result = self.scorer.score(
                case_id=case.case_id,
                response=response,
                expected_keywords=case.expected_keywords,
            )

            results.append(result)

        passed = sum(result.passed for result in results)
        total = len(results)
        failed = total - passed

        accuracy = (
            passed / total
            if total
            else 1.0
        )

        summary = EvaluationSummary(
            total=total,
            passed=passed,
            failed=failed,
            accuracy=round(accuracy, 4),
        )

        return results, summary
