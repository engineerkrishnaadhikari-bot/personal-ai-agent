from app.database.memory_repository import MemoryRepository


class LearningManager:
    """Converts user corrections into reusable lessons."""

    def __init__(
        self,
        repository: MemoryRepository | None = None,
    ) -> None:
        self.repository = repository or MemoryRepository()

    def learn_from_correction(
        self,
        context: str,
        agent_action: str,
        expected_result: str,
        actual_result: str,
        user_correction: str,
        category: str = "general",
        importance: float = 0.8,
        user_confirmed: bool = True,
    ) -> int:
        self._validate_score(importance, "Importance")

        if not context.strip():
            raise ValueError("Context cannot be empty.")

        if not agent_action.strip():
            raise ValueError("Agent action cannot be empty.")

        if not expected_result.strip():
            raise ValueError("Expected result cannot be empty.")

        if not actual_result.strip():
            raise ValueError("Actual result cannot be empty.")

        if not user_correction.strip():
            raise ValueError("User correction cannot be empty.")

        if not category.strip():
            raise ValueError("Category cannot be empty.")

        mistake_id = self.repository.add_mistake(
            context=context.strip(),
            agent_action=agent_action.strip(),
            expected_result=expected_result.strip(),
            actual_result=actual_result.strip(),
            user_correction=user_correction.strip(),
        )

        confidence = 1.0 if user_confirmed else 0.6

        lesson = self._build_lesson(
            expected_result=expected_result.strip(),
            user_correction=user_correction.strip(),
        )

        return self.repository.add_lesson(
            lesson=lesson,
            category=category.strip(),
            confidence=confidence,
            importance=importance,
            source_mistake_id=mistake_id,
            user_confirmed=user_confirmed,
        )

    def recall_lessons(self) -> list[dict]:
        return self.repository.get_lessons()

    @staticmethod
    def _build_lesson(
        expected_result: str,
        user_correction: str,
    ) -> str:
        return (
            f"Expected: {expected_result} "
            f"User correction: {user_correction}"
        )

    @staticmethod
    def _validate_score(value: float, field_name: str) -> None:
        if not 0.0 <= value <= 1.0:
            raise ValueError(
                f"{field_name} must be between 0 and 1."
            )
