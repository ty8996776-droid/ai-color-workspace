import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from ai.common import WORKSPACE_ROOT, log_event, utc_now


class MemoryStore:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or (WORKSPACE_ROOT / "ai" / "memory" / "workspace_memory.sqlite3")
        self._memory_conn = sqlite3.connect(":memory:") if self.db_path == Path(":memory:") else None

    def _connect(self):
        if self._memory_conn is not None:
            return self._memory_conn
        if self.db_path != Path(":memory:"):
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(self.db_path))

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS color_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_file TEXT NOT NULL,
                    analyzer_result TEXT NOT NULL,
                    planner_result TEXT NOT NULL,
                    dctl_params TEXT NOT NULL,
                    score_result TEXT NOT NULL,
                    user_feedback TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
        log_event("memory", "init_db", {"db_path": str(self.db_path)})

    def save_record(
        self,
        input_file: str,
        analyzer_result: Dict[str, Any],
        planner_result: Dict[str, Any],
        dctl_params: Dict[str, Any],
        score_result: Dict[str, Any],
        user_feedback: str = "",
    ) -> int:
        created_at = utc_now()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO color_records (
                    input_file,
                    analyzer_result,
                    planner_result,
                    dctl_params,
                    score_result,
                    user_feedback,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    input_file,
                    json.dumps(analyzer_result, ensure_ascii=False, sort_keys=True),
                    json.dumps(planner_result, ensure_ascii=False, sort_keys=True),
                    json.dumps(dctl_params, ensure_ascii=False, sort_keys=True),
                    json.dumps(score_result, ensure_ascii=False, sort_keys=True),
                    user_feedback,
                    created_at,
                ),
            )
            record_id = int(cursor.lastrowid)
        log_event("memory", "save_record", {"id": record_id, "input_file": input_file})
        return record_id

    def list_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, input_file, analyzer_result, planner_result, dctl_params, score_result, user_feedback, created_at
                FROM color_records
                ORDER BY id DESC
                LIMIT ?
                """,
                (int(limit),),
            ).fetchall()
        history = [
            {
                "id": row[0],
                "input_file": row[1],
                "analyzer_result": json.loads(row[2]),
                "planner_result": json.loads(row[3]),
                "dctl_params": json.loads(row[4]),
                "score_result": json.loads(row[5]),
                "user_feedback": row[6],
                "created_at": row[7],
            }
            for row in rows
        ]
        log_event("memory", "list_history", {"count": len(history)})
        return history
