"""Recuperación full-text sobre la base de discursos (SQLite FTS5)."""
from __future__ import annotations

import re
import sqlite3
from typing import Optional

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)

# Stopwords frecuentes del español: no aportan a la búsqueda y ensucian el ranking.
_STOPWORDS = {
    "a", "al", "ante", "con", "como", "de", "del", "desde", "el", "ella",
    "ellos", "en", "entre", "es", "esa", "ese", "esta", "este", "esto", "fue",
    "ha", "han", "hay", "la", "las", "le", "les", "lo", "los", "mas", "me",
    "mi", "no", "nos", "o", "para", "pero", "por", "que", "se", "si", "sin",
    "sobre", "su", "sus", "te", "un", "una", "uno", "unos", "unas", "y", "ya",
}


def build_match(query: str) -> str:
    """Convierte texto libre en una consulta FTS5 segura.

    - Quita stopwords del español.
    - Usa matching por prefijo (token*) para tolerar plurales y flexiones
      (p.ej. "universidad" matchea "universidades"). FTS5 no hace stemming.
    - Une con OR para maximizar el recall; bm25 ordena los resultados.
    Los tokens son \\w+ (alfanuméricos), seguros de usar sin entrecomillar.
    """
    tokens = [t for t in _TOKEN_RE.findall(query.lower()) if t not in _STOPWORDS]
    if not tokens:
        raise ValueError("La consulta no contiene términos buscables.")
    terms = [f"{t}*" if len(t) >= 4 else t for t in tokens]
    return " OR ".join(terms)


def search(
    con: sqlite3.Connection,
    query: str,
    limit: int = 8,
    chamber: Optional[str] = None,
) -> list[dict]:
    match = build_match(query)
    sql = """
        SELECT s.id, s.chamber, s.session, s.date, s.speaker, s.party,
               s.province, s.text, s.source_url,
               bm25(speeches_fts) AS score,
               snippet(speeches_fts, 0, '«', '»', ' … ', 18) AS snippet
        FROM speeches_fts
        JOIN speeches s ON s.id = speeches_fts.rowid
        WHERE speeches_fts MATCH ?
    """
    params: list = [match]
    if chamber:
        sql += " AND s.chamber = ?"
        params.append(chamber)
    sql += " ORDER BY score LIMIT ?"
    params.append(limit)
    return [dict(row) for row in con.execute(sql, params).fetchall()]
