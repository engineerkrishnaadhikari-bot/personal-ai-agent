from dataclasses import dataclass

from app.verification.risk import RiskEngine, RiskLevel


@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    requires_approval: bool
    reason: str


class ToolPermissionManager:
    """Determine whether a tool action may execute."""

    def __init__(
        self,
        risk_engine: RiskEngine | None = None,
    ) -> None:
        self.risk_engine = risk_engine or RiskEngine()

    def evaluate(
        self,
        action: str,
        approved: bool = False,
    ) -> PermissionDecision:
        risk = self.risk_engine.classify(action)

        if risk == RiskLevel.LOW:
            return PermissionDecision(
                allowed=True,
                requires_approval=False,
                reason="Low-risk action.",
            )

        if risk == RiskLevel.MEDIUM:
            if approved:
                return PermissionDecision(
                    allowed=True,
                    requires_approval=False,
                    reason="Medium-risk action approved.",
                )

            return PermissionDecision(
                allowed=False,
                requires_approval=True,
                reason="User approval required.",
            )

        if risk == RiskLevel.HIGH:
            if approved:
                return PermissionDecision(
                    allowed=True,
                    requires_approval=False,
                    reason="High-risk action approved.",
                )

            return PermissionDecision(
                allowed=False,
                requires_approval=True,
                reason="Explicit user approval required.",
            )

        return PermissionDecision(
            allowed=False,
            requires_approval=True,
            reason="Critical actions require explicit approval.",
        )
