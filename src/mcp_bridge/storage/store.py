from __future__ import annotations

import os
import sqlite3
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Any, Optional


@dataclass
class InMemoryStore:
    todos: Dict[int, Dict[str, Any]]
    next_id: int = 1

    def __init__(self) -> None:
        self.todos = {}
        self.next_id = 1

    def create(self, title: str) -> int:
        cleaned = title.strip()
        if not cleaned:
            raise ValueError("title cannot be empty")
        tid = self.next_id
        self.todos[tid] = {"title": cleaned, "completed": False}
        self.next_id += 1
        return tid

    def list_all(self) -> Dict[int, Dict[str, Any]]:
        return dict(self.todos)

    def get(self, tid: int) -> Optional[Dict[str, Any]]:
        return self.todos.get(tid)

    def update(
        self, tid: int, title: Optional[str] = None, completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        item = self.todos.get(tid)
        if item is None:
            raise ValueError(f"todo {tid} not found")
        if title is not None:
            cleaned = title.strip()
            if not cleaned:
                raise ValueError("title cannot be empty")
            item["title"] = cleaned
        if completed is not None:
            if not isinstance(completed, bool):
                raise ValueError("completed must be a boolean")
            item["completed"] = completed
        return item

    def delete(self, tid: int) -> Dict[str, Any]:
        if tid not in self.todos:
            raise ValueError(f"todo {tid} not found")
        return self.todos.pop(tid)


class SQLiteStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=NORMAL;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create(self, title: str) -> int:
        cleaned = title.strip()
        if not cleaned:
            raise ValueError("title cannot be empty")
        now = self._now()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO todos (title, completed, created_at, updated_at) VALUES (?, 0, ?, ?)",
            (cleaned, now, now),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def list_all(self) -> Dict[int, Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, completed FROM todos ORDER BY id")
        result: Dict[int, Dict[str, Any]] = {}
        for row in cur.fetchall():
            result[int(row["id"])] = {
                "title": row["title"],
                "completed": bool(row["completed"]),
            }
        return result

    def get(self, tid: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, completed FROM todos WHERE id = ?", (tid,))
        row = cur.fetchone()
        if not row:
            return None
        return {"title": row["title"], "completed": bool(row["completed"])}

    def update(
        self, tid: int, title: Optional[str] = None, completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        if title is None and completed is None:
            raise ValueError("provide at least one field to update: title or completed")
        cur = self.conn.cursor()
        if title is not None and completed is not None:
            cleaned = title.strip()
            if not cleaned:
                raise ValueError("title cannot be empty")
            cur.execute(
                "UPDATE todos SET title = ?, completed = ?, updated_at = ? WHERE id = ?",
                (cleaned, 1 if completed else 0, self._now(), tid),
            )
        elif title is not None:
            cleaned = title.strip()
            if not cleaned:
                raise ValueError("title cannot be empty")
            cur.execute(
                "UPDATE todos SET title = ?, updated_at = ? WHERE id = ?",
                (cleaned, self._now(), tid),
            )
        else:
            if not isinstance(completed, bool):
                raise ValueError("completed must be a boolean")
            cur.execute(
                "UPDATE todos SET completed = ?, updated_at = ? WHERE id = ?",
                (1 if completed else 0, self._now(), tid),
            )
        if cur.rowcount == 0:
            raise ValueError(f"todo {tid} not found")
        self.conn.commit()
        item = self.get(tid)
        assert item is not None
        return item

    def delete(self, tid: int) -> Dict[str, Any]:
        item = self.get(tid)
        if item is None:
            raise ValueError(f"todo {tid} not found")
        cur = self.conn.cursor()
        cur.execute("DELETE FROM todos WHERE id = ?", (tid,))
        self.conn.commit()
        return item


def get_store() -> InMemoryStore | SQLiteStore:
    db_path = os.getenv("MCP_TODO_DB")
    if db_path:
        return SQLiteStore(db_path)
    return InMemoryStore()
