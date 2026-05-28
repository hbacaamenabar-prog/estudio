"""Scraper de versiones taquigráficas del H. Senado de la Nación.

Fuente (requiere acceso de red a los dominios .gob.ar):
  - Buscador de versiones taquigráficas y diarios de sesiones:
      https://www.senado.gob.ar/parlamentario/sesiones/busquedaTac
      Las versiones suelen publicarse en PDF por sesión.

NOTA: igual que en Diputados, el parseo concreto depende del PDF/HTML real,
que debe inspeccionarse con acceso de red.
"""
from __future__ import annotations

from .common import http_get, make_record  # noqa: F401

BUSQUEDA_TAQUIGRAFICA = (
    "https://www.senado.gob.ar/parlamentario/sesiones/busquedaTac"
)


def scrape(limit: int | None = None) -> list[dict]:
    """Devuelve intervenciones normalizadas (esquema de make_record).

    TODO (requiere acceso de red a senado.gob.ar):
      1. Listar las sesiones desde el buscador taquigráfico.
      2. Descargar el PDF de cada versión (http_get) y common.pdf_to_text.
      3. Segmentar por orador (encabezados tipo "Sr. APELLIDO.-") y emitir un
         make_record(chamber='senado', ...) por intervención.
    """
    raise NotImplementedError(
        "Parseo pendiente: requiere inspeccionar la estructura real de "
        "senado.gob.ar (bloqueada en este entorno por la allowlist de red)."
    )
