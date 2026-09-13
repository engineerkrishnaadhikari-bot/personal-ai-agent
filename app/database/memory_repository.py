import sqlite3
from pathlib import Path


class MemoryRepository:
    """Local SQLite repository for memories and learning records."""

    def __init__(self, database_path: str = "data/memory.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance REAL NOT NULL DEFAULT 0.5,
                    confidence REAL NOT NULL DEFAULT 0.5,
                    user_confirmed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS mistakes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context TEXT NOT NULL,
                    agent_action TEXT NOT NULL,
                    expected_result TEXT NOT NULL,
                    actual_result TEXT NOT NULL,
                    user_correction TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS lessons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson TEXT NOT NULL,
                    category TEXT NOT NULL,
                    confidence REAL NOT NULL DEFAULT 0.5,
                    importance REAL NOT NULL DEFAULT 0.5,
                    source_mistake_id INTEGER,
                    times_applied INTEGER NOT NULL DEFAULT 0,
                    user_confirmed INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(source_mistake_id)
                        REFERENCES mistakes(id)
                )
                """
            )

    def add(
        self,
        memory_type: str,
        content: str,
        importance: float = 0.5,
        confidence: float = 0.5,
        user_confirmed: bool = False,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO memories
                (
                    memory_type,
                    content,
                    importance,
                    confidence,
                    user_confirmed
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    memory_type,
                    content,
                    importance,
                    confidence,
                    int(user_confirmed),
                ),
            )
            return int(cursor.lastrowid)

    def get_all(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    memory_type,
                    content,
                    importance,
                    confidence,
                    user_confirmed,
                    created_at,
                    updated_at
                FROM memories
                ORDER BY importance DESC, updated_at DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def add_mistake(
        self,
        context: str,
        agent_action: str,
        expected_result: str,
        actual_result: str,
        user_correction: str,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO mistakes
                (
                    context,
                    agent_action,
                    expected_result,
                    actual_result,
                    user_correction
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    context,
                    agent_action,
                    expected_result,
                    actual_result,
                    user_correction,
                ),
            )
            return int(cursor.lastrowid)

    def add_lesson(
        self,
        lesson: str,
        category: str,
        confidence: float,
        importance: float,
        source_mistake_id: int | None = None,
        user_confirmed: bool = False,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO lessons
                (
                    lesson,
                    category,
                    confidence,
                    importance,
                    source_mistake_id,
                    user_confirmed
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    lesson,
                    category,
                    confidence,
                    importance,
                    source_mistake_id,
                    int(user_confirmed),
                ),
            )
            return int(cursor.lastrowid)

    def get_lessons(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    lesson,
                    category,
                    confidence,
                    importance,
                    source_mistake_id,
                    times_applied,
                    user_confirmed,
                    created_at,
                    updated_at
                FROM lessons
                ORDER BY confidence DESC, importance DESC, updated_at DESC
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def search_lessons(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """Return lessons matching words from the query."""

        if not query.strip():
            return []

        words = [
            word.strip().lower()
            for word in query.split()
            if len(word.strip()) >= 3
        ]

        if not words:
            return []

        conditions = " OR ".join(
            "LOWER(lesson) LIKE ?" for _ in words
        )

        parameters = [f"%{word}%" for word in words]
        parameters.append(limit)

        with self._connect() as connection:
            rows = connection.execute(
                f"""
                SELECT
                    id,
                    lesson,
                    category,
                    confidence,
                    importance,
                    source_mistake_id,
                    times_applied,
                    user_confirmed,
                    created_at,
                    updated_at
                FROM lessons
                WHERE {conditions}
                ORDER BY confidence DESC, importance DESC, updated_at DESC
                LIMIT ?
                """,
                parameters,
            ).fetchall()

        return [dict(row) for row in rows]
