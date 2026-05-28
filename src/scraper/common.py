"""Plumbing común para los scrapers (HTTP con reintentos, PDF→texto, IO)."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Iterable, Mapping

import requests

USER_AGENT = (
    "Mozilla/5.0 (compatible; estudio-discursos/0.1; "
    "+investigacion academica)"
)


def http_get(url: str, *, retries: int = 4, timeout: int = 30,
             session: requests.Session | None = None) -> requests.Response:
    """GET con backoff exponencial (2s, 4s, 8s, 16s) ante errores de red."""
    sess = session or requests.Session()
    headers = {"User-Agent": USER_AGENT}
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            resp = sess.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:  # red o HTTP 5xx
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"Fallo GET {url} tras {retries} intentos: {last_exc}")


def pdf_to_text(content: bytes) -> str:
    """Extrae texto de un PDF (las versiones taquigráficas suelen ser PDF).

    Requiere `pdfmin.six` (ver requirements.txt). Se importa de forma diferida.
    """
    import io
    from pdfminer.high_level import extract_text  # type: ignore

    return extract_text(io.BytesIO(content))


def save_records_json(records: Iterable[Mapping], path: str | Path) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = list(records)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                    encoding="utf-8")
    return len(data)


def make_record(*, chamber: str, text: str, source_id: str,
                session: str | None = None, date: str | None = None,
                speaker: str | None = None, party: str | None = None,
                province: str | None = None,
                source_url: str | None = None) -> dict:
    """Normaliza una intervención al esquema que consume la base de datos."""
    return {
        "chamber": chamber, "session": session, "date": date,
        "speaker": speaker, "party": party, "province": province,
        "text": text.strip(), "source_url": source_url, "source_id": source_id,
    }
