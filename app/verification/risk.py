from enum import StrEnum


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskEngine:
    """Classify potentially dangerous actions."""

    def classify(self, action: str) -> RiskLevel:
        normalized = action.lower()

        critical_terms = (
            "delete everything",
            "format disk",
            "rm -rf /",
            "drop database",
            "force push",
        )

        high_terms = (
            "delete",
            "remove",
            "send email",
            "push",
            "deploy",
            "execute",
        )

        medium_terms = (
            "write file",
            "modify file",
            "git commit",
        )

        if any(term in normalized for term in critical_terms):
            return RiskLevel.CRITICAL

        if any(term in normalized for term in high_terms):
            return RiskLevel.HIGH

        if any(term in normalized for term in medium_terms):
            return RiskLevel.MEDIUM

        return RiskLevel.LOW
