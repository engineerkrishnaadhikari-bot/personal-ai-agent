from unittest.mock import Mock

from app.agent.core import PersonalAgent


def test_agent_passes_prompt_to_llm() -> None:
    agent = PersonalAgent()
    agent.llm = Mock()

    agent.llm.chat.return_value = "Test response"

    result = agent.ask("Hello")

    agent.llm.chat.assert_called_once_with("Hello")
    assert result == "Test response"


def test_agent_rejects_empty_prompt() -> None:
    agent = PersonalAgent()

    try:
        agent.ask("   ")
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert str(exc) == "Prompt cannot be empty."
