#!/usr/bin/env python3
"""Orquesta el scraping de las cámaras y guarda los discursos en JSON.

Uso (requiere acceso de red a los sitios .gob.ar):
    python scripts/run_scraper.py --chamber diputados --out data/diputados.json
    python scripts/run_scraper.py --chamber senado    --out data/senado.json

Luego cargá el JSON en la base con:
    python scripts/build_db.py --input data/diputados.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scraper import diputados, senado, common  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description="Scraper de discursos del Congreso.")
    ap.add_argument("--chamber", required=True, choices=["diputados", "senado"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    mod = diputados if args.chamber == "diputados" else senado
    records = mod.scrape(limit=args.limit)
    n = common.save_records_json(records, args.out)
    print(f"Guardadas {n} intervenciones en {args.out}")


if __name__ == "__main__":
    main()
