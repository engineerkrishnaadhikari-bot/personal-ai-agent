from app.tools.permissions import ToolPermissionManager


def test_low_risk_action_allowed() -> None:
    decision = ToolPermissionManager().evaluate(
        "list files"
    )

    assert decision.allowed is True
    assert decision.requires_approval is False


def test_medium_risk_requires_approval() -> None:
    decision = ToolPermissionManager().evaluate(
        "git commit changes"
    )

    assert decision.allowed is False
    assert decision.requires_approval is True


def test_medium_risk_can_be_approved() -> None:
    decision = ToolPermissionManager().evaluate(
        "git commit changes",
        approved=True,
    )

    assert decision.allowed is True


def test_high_risk_requires_approval() -> None:
    decision = ToolPermissionManager().evaluate(
        "push changes to remote",
    )

    assert decision.allowed is False
    assert decision.requires_approval is True


def test_critical_action_never_auto_executes() -> None:
    decision = ToolPermissionManager().evaluate(
        "force push",
    )

    assert decision.allowed is False
    assert decision.requires_approval is True


def test_critical_action_requires_explicit_approval() -> None:
    decision = ToolPermissionManager().evaluate(
        "force push",
        approved=True,
    )

    assert decision.allowed is False
