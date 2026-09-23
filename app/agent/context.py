from app.learning.manager import LearningManager


class AgentContextBuilder:
    """Build relevant context for an agent request."""

    def __init__(
        self,
        learning_manager: LearningManager | None = None,
    ) -> None:
        self.learning_manager = (
            learning_manager or LearningManager()
        )

    def build(self, prompt: str) -> str:
        lessons = self.learning_manager.recall_relevant_lessons(
            prompt,
            limit=5,
        )

        if not lessons:
            return ""

        lines = [
            "Relevant lessons learned from previous interactions:"
        ]

        for lesson in lessons:
            lines.append(
                f"- {lesson['lesson']} "
                f"(confidence={lesson['confidence']:.2f})"
            )

        return "\n".join(lines)
