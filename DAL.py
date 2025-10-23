import os
import sqlite3
from typing import List, Optional, Tuple, Dict, Any


DB_FILENAME = 'projects.db'


def get_db_path() -> str:
    return os.path.join(os.path.dirname(__file__), DB_FILENAME)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create database and projects table if not exists."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                image_file_name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def list_projects() -> List[sqlite3.Row]:
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, title, description, image_file_name, created_at FROM projects ORDER BY created_at DESC"
        )
        return cur.fetchall()


def insert_project(title: str, description: str, image_file_name: str) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO projects (title, description, image_file_name) VALUES (?, ?, ?)",
            (title.strip(), description.strip(), image_file_name.strip()),
        )
        return cur.lastrowid


def delete_project(project_id: int) -> int:
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        return cur.rowcount


