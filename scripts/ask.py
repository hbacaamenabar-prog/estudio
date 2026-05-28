#!/usr/bin/env python3
"""Consulta el agente RAG sobre los discursos.

Uso:
    python scripts/ask.py "¿Qué se dijo sobre educación?"
    python scripts/ask.py "energía" --chamber senado --limit 5
    python scripts/ask.py "salud" --retrieve-only      # sin llamar a Claude

Si no hay ANTHROPIC_API_KEY, cae automáticamente a modo retrieve-only.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.db import database  # noqa: E402
from src.agent import agent, retriever  # noqa: E402


def print_sources(results: list[dict]) -> None:
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r.get('speaker')} ({r.get('party')}, "
              f"{r.get('province')}) — {r.get('chamber')}, "
              f"{r.get('date')}  score={r['score']:.2f}")
        print(f"    {r['snippet']}")
        if r.get("source_url"):
            print(f"    fuente: {r['source_url']}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Agente RAG de discursos.")
    ap.add_argument("question")
    ap.add_argument("--db", default=str(ROOT / "discursos.db"))
    ap.add_argument("--chamber", choices=["diputados", "senado"])
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--retrieve-only", action="store_true",
                    help="Solo muestra los pasajes recuperados, sin llamar a Claude.")
    args = ap.parse_args()

    con = database.connect(args.db)

    if args.retrieve_only or not os.environ.get("ANTHROPIC_API_KEY"):
        if not args.retrieve_only:
            print("(ANTHROPIC_API_KEY no definida → modo solo-recuperación)\n")
        results = retriever.search(con, args.question,
                                   limit=args.limit, chamber=args.chamber)
        if not results:
            print("Sin resultados.")
            return
        print(f"Pasajes recuperados para: {args.question!r}")
        print_sources(results)
        return

    res = agent.answer(con, args.question, limit=args.limit, chamber=args.chamber)
    print("RESPUESTA\n")
    print(res["answer"])
    print("\n\nFUENTES")
    print_sources(res["sources"])


if __name__ == "__main__":
    main()
