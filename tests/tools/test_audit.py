from pathlib import Path

from app.database.audit_repository import AuditRepository
from app.tools.audit import AuditLogger
from app.verification.risk import RiskLevel


def test_audit_event_is_recorded(tmp_path: Path) -> None:
    repository = AuditRepository(
        str(tmp_path / "audit.db")
    )
    audit = AuditLogger(repository)

    event_id = audit.record(
        event_type="tool_execution",
        action="git_status",
        risk_level=RiskLevel.LOW,
        allowed=True,
        approved=False,
        success=True,
        details="Git status completed.",
    )

    events = audit.recent()

    assert event_id == 1
    assert len(events) == 1
    assert events[0]["event_type"] == "tool_execution"
    assert events[0]["action"] == "git_status"
    assert events[0]["risk_level"] == "low"
    assert events[0]["allowed"] == 1
    assert events[0]["success"] == 1


def test_denied_action_is_recorded(tmp_path: Path) -> None:
    repository = AuditRepository(
        str(tmp_path / "audit.db")
    )
    audit = AuditLogger(repository)

    audit.record(
        event_type="tool_denied",
        action="force push",
        risk_level=RiskLevel.CRITICAL,
        allowed=False,
        approved=False,
        success=False,
        details="Critical action denied.",
    )

    event = audit.recent()[0]

    assert event["allowed"] == 0
    assert event["success"] == 0
    assert event["risk_level"] == "critical"