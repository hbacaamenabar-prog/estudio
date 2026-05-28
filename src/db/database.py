"""Acceso a la base de discursos (SQLite + FTS5)."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Mapping

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

FIELDS = (
    "chamber", "session", "date", "speaker",
    "party", "province", "text", "source_url", "source_id",
)


def connect(db_path: str | Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_db(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    con.commit()


def insert_speeches(con: sqlite3.Connection, records: Iterable[Mapping]) -> int:
    """Inserta intervenciones. Dedup por source_id (INSERT OR IGNORE)."""
    rows = [tuple(r.get(f) for f in FIELDS) for r in records]
    placeholders = ", ".join("?" for _ in FIELDS)
    cur = con.executemany(
        f"INSERT OR IGNORE INTO speeches ({', '.join(FIELDS)}) "
        f"VALUES ({placeholders})",
        rows,
    )
    con.commit()
    return cur.rowcount


def count(con: sqlite3.Connection) -> int:
    return con.execute("SELECT COUNT(*) FROM speeches").fetchone()[0]
