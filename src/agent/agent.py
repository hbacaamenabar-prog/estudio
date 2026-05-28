"""Agente RAG sobre los discursos: recupera con FTS5 y responde con Claude."""
from __future__ import annotations

import os
import sqlite3
from typing import Optional

from .retriever import search

DEFAULT_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = (
    "Sos un asistente que responde preguntas sobre discursos del Congreso "
    "de la Nación Argentina (Cámara de Diputados y Senado).\n"
    "Reglas:\n"
    "- Respondé ÚNICAMENTE con base en los fragmentos de discursos provistos.\n"
    "- Si los fragmentos no alcanzan para responder, decílo explícitamente.\n"
    "- Citá las fuentes usando los números entre corchetes, p.ej. [2].\n"
    "- No inventes citas textuales ni atribuyas frases que no figuren.\n"
    "- Sé conciso y neutral; no opines políticamente."
)


def format_context(results: list[dict]) -> str:
    bloques = []
    for i, r in enumerate(results, 1):
        encabezado = (
            f"[{i}] {r.get('speaker') or 'Orador/a s/d'} "
            f"({r.get('party') or 's/d'}, {r.get('province') or 's/d'}) — "
            f"{r.get('chamber')}, {r.get('session') or 's/d'}, "
            f"{r.get('date') or 's/d'}"
        )
        bloques.append(f"{encabezado}\n{r['text']}")
    return "\n\n---\n\n".join(bloques)


def answer(
    con: sqlite3.Connection,
    question: str,
    limit: int = 8,
    chamber: Optional[str] = None,
    model: str = DEFAULT_MODEL,
) -> dict:
    """Devuelve {'answer', 'sources'}. Requiere ANTHROPIC_API_KEY."""
    import anthropic  # import diferido: el modo retrieve-only no lo necesita

    results = search(con, question, limit=limit, chamber=chamber)
    if not results:
        return {"answer": "No se encontraron discursos relacionados.", "sources": []}

    client = anthropic.Anthropic()
    user_content = (
        f"Pregunta: {question}\n\n"
        f"Fragmentos de discursos:\n\n{format_context(results)}"
    )
    msg = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return {"answer": text, "sources": results}
