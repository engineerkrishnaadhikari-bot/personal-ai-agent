import sqlite3
from pathlib import Path


class AuditRepository:
    """Store an immutable record of agent actions."""

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
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    action TEXT NOT NULL,
                    risk_level TEXT NOT NULL,
                    allowed INTEGER NOT NULL,
                    approved INTEGER NOT NULL,
                    success INTEGER NOT NULL,
                    details TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def record(
        self,
        event_type: str,
        action: str,
        risk_level: str,
        allowed: bool,
        approved: bool,
        success: bool,
        details: str,
    ) -> int:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO audit_events (
                    event_type,
                    action,
                    risk_level,
                    allowed,
                    approved,
                    success,
                    details
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_type,
                    action,
                    risk_level,
                    int(allowed),
                    int(approved),
                    int(success),
                    details,
                ),
            )

            return int(cursor.lastrowid)

    def get_recent(self, limit: int = 50) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    event_type,
                    action,
                    risk_level,
                    allowed,
                    approved,
                    success,
                    details,
                    created_at
                FROM audit_events
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        return [dict(row) for row in rows]