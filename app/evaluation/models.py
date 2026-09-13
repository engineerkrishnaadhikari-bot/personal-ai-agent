from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    """A deterministic test case for agent evaluation."""

    case_id: str
    prompt: str
    expected_keywords: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationResult:
    """Result of evaluating one test case."""

    case_id: str
    passed: bool
    score: float
    missing_keywords: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationSummary:
    """Aggregate evaluation statistics."""

    total: int
    passed: int
    failed: int
    accuracy: float
