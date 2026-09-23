from app.agent.context import AgentContextBuilder
from app.agent.ollama_client import OllamaClient


class PersonalAgent:
    """Core interface for the Personal AI Agent."""

    def __init__(
        self,
        llm: OllamaClient | None = None,
        context_builder: AgentContextBuilder | None = None,
    ) -> None:
        self.llm = llm or OllamaClient()
        self.context_builder = (
            context_builder or AgentContextBuilder()
        )

    def ask(self, prompt: str) -> str:
        """Process a request using relevant learned context."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        learned_context = self.context_builder.build(prompt)

        if learned_context:
            enhanced_prompt = (
                f"{learned_context}\n\n"
                f"User request:\n{prompt}"
            )
        else:
            enhanced_prompt = prompt

        return self.llm.chat(enhanced_prompt)
