from app.agent.ollama_client import OllamaClient


class PersonalAgent:
    """Core interface for the Personal AI Agent."""

    def __init__(self) -> None:
        self.llm = OllamaClient()

    def ask(self, prompt: str) -> str:
        """Process a user request and return an answer."""
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        return self.llm.chat(prompt)
