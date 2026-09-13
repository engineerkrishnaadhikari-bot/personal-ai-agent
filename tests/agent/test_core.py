from unittest.mock import Mock

import pytest

from app.agent.core import PersonalAgent


def test_agent_passes_prompt_to_llm() -> None:
    agent = PersonalAgent()
    agent.llm = Mock()
    agent.context_builder = Mock()

    agent.context_builder.build.return_value = ""
    agent.llm.chat.return_value = "Test response"

    result = agent.ask("Hello")

    agent.context_builder.build.assert_called_once_with(
        "Hello"
    )
    agent.llm.chat.assert_called_once_with("Hello")

    assert result == "Test response"


def test_agent_uses_learned_context() -> None:
    agent = PersonalAgent()
    agent.llm = Mock()
    agent.context_builder = Mock()

    agent.context_builder.build.return_value = (
        "Relevant lesson: main is for stable releases."
    )
    agent.llm.chat.return_value = "Use development branch."

    result = agent.ask("How should I develop this feature?")

    sent_prompt = agent.llm.chat.call_args.args[0]

    assert (
        "Relevant lesson: main is for stable releases."
        in sent_prompt
    )
    assert "How should I develop this feature?" in sent_prompt
    assert result == "Use development branch."


def test_agent_rejects_empty_prompt() -> None:
    agent = PersonalAgent()

    with pytest.raises(
        ValueError,
        match="Prompt cannot be empty",
    ):
        agent.ask("   ")
