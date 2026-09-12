import sqlite3
from pathlib import Path


class MemoryRepository:
    """Local SQLite repository for agent memories."""

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
                (memory_type, content, importance, confidence, user_confirmed)
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
