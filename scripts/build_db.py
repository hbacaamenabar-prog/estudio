#!/usr/bin/env python3
"""Construye/actualiza la base de discursos a partir de archivos JSON.

Uso:
    python scripts/build_db.py                  # carga data/sample en discursos.db
    python scripts/build_db.py --input ruta.json --db mi.db
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.db import database  # noqa: E402


def load_records(path: Path) -> list[dict]:
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    records: list[dict] = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        records.extend(data if isinstance(data, list) else [data])
    return records


def main() -> None:
    ap = argparse.ArgumentParser(description="Construye la base de discursos.")
    ap.add_argument("--db", default=str(ROOT / "discursos.db"))
    ap.add_argument("--input", default=str(ROOT / "data" / "sample"))
    args = ap.parse_args()

    records = load_records(Path(args.input))
    con = database.connect(args.db)
    database.init_db(con)
    inserted = database.insert_speeches(con, records)
    print(f"Leídos: {len(records)} | Insertados nuevos: {inserted} | "
          f"Total en base: {database.count(con)}")
    print(f"Base: {args.db}")


if __name__ == "__main__":
    main()
