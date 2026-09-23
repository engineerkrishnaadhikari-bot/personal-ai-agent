from app.database.audit_repository import AuditRepository
from app.verification.risk import RiskLevel


class AuditLogger:
    """Record tool and agent actions."""

    def __init__(
        self,
        repository: AuditRepository | None = None,
    ) -> None:
        self.repository = repository or AuditRepository()

    def record(
        self,
        *,
        event_type: str,
        action: str,
        risk_level: RiskLevel,
        allowed: bool,
        approved: bool,
        success: bool,
        details: str,
    ) -> int:
        return self.repository.record(
            event_type=event_type,
            action=action,
            risk_level=risk_level.value,
            allowed=allowed,
            approved=approved,
            success=success,
            details=details,
        )

    def recent(self, limit: int = 50) -> list[dict]:
        return self.repository.get_recent(limit)