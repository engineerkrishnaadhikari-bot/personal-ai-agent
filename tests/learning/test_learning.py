from pathlib import Path

import pytest

from app.database.memory_repository import MemoryRepository
from app.learning.manager import LearningManager


@pytest.fixture
def learning_manager(tmp_path: Path) -> LearningManager:
    repository = MemoryRepository(str(tmp_path / "learning.db"))
    return LearningManager(repository)


def test_learn_from_user_correction(
    learning_manager: LearningManager,
) -> None:
    lesson_id = learning_manager.learn_from_correction(
        context="Git release workflow",
        agent_action="Recommended development on main",
        expected_result="Development uses development branch",
        actual_result="Agent recommended main",
        user_correction=(
            "Main is only for stable releases."
        ),
        category="git",
        importance=0.9,
        user_confirmed=True,
    )

    lessons = learning_manager.recall_lessons()

    assert lesson_id == 1
    assert len(lessons) == 1
    assert lessons[0]["category"] == "git"
    assert lessons[0]["confidence"] == 1.0
    assert lessons[0]["importance"] == 0.9
    assert lessons[0]["user_confirmed"] == 1


def test_unconfirmed_lesson_gets_lower_confidence(
    learning_manager: LearningManager,
) -> None:
    learning_manager.learn_from_correction(
        context="Testing",
        agent_action="Wrong recommendation",
        expected_result="Use regression testing",
        actual_result="Suggested smoke testing",
        user_correction="Use regression testing here.",
        user_confirmed=False,
    )

    lessons = learning_manager.recall_lessons()

    assert lessons[0]["confidence"] == 0.6
    assert lessons[0]["user_confirmed"] == 0


def test_empty_correction_rejected(
    learning_manager: LearningManager,
) -> None:
    with pytest.raises(
        ValueError,
        match="User correction cannot be empty",
    ):
        learning_manager.learn_from_correction(
            context="Testing",
            agent_action="Wrong answer",
            expected_result="Correct answer",
            actual_result="Wrong answer",
            user_correction="   ",
        )


def test_invalid_importance_rejected(
    learning_manager: LearningManager,
) -> None:
    with pytest.raises(
        ValueError,
        match="Importance must be between 0 and 1",
    ):
        learning_manager.learn_from_correction(
            context="Testing",
            agent_action="Wrong answer",
            expected_result="Correct answer",
            actual_result="Wrong answer",
            user_correction="Fix this",
            importance=1.5,
        )
