"""Scraper de versiones taquigráficas de la H. Cámara de Diputados.

Fuentes (requieren acceso de red a los dominios .gob.ar):
  - Datos Abiertos (portal CKAN): https://datos.hcdn.gob.ar
      API estándar CKAN: /api/3/action/package_list y package_show.
      Útil para metadatos (legisladores, bloques, votaciones, sesiones).
  - Dirección de Taquígrafos: https://www.diputados.gov.ar/secparl/dtaqui/
      Publica las versiones taquigráficas de las sesiones (HTML/PDF).

NOTA: el parseo concreto (selección de bloques de discurso por orador dentro
de cada versión taquigráfica) depende del HTML/PDF real, que debe inspeccionarse
con acceso de red. La función `scrape()` deja marcado ese punto.
"""
from __future__ import annotations

from .common import http_get, make_record  # noqa: F401

DATOS_ABIERTOS = "https://datos.hcdn.gob.ar"
TAQUIGRAFOS = "https://www.diputados.gov.ar/secparl/dtaqui/"


def list_ckan_datasets() -> list[str]:
    """Lista los datasets del portal CKAN de Diputados."""
    resp = http_get(f"{DATOS_ABIERTOS}/api/3/action/package_list")
    return resp.json().get("result", [])


def scrape(limit: int | None = None) -> list[dict]:
    """Devuelve intervenciones normalizadas (esquema de make_record).

    TODO (requiere acceso de red a diputados.gov.ar para inspeccionar el HTML):
      1. Listar las versiones taquigráficas disponibles desde TAQUIGRAFOS.
      2. Descargar cada versión (http_get) y, si es PDF, common.pdf_to_text.
      3. Segmentar el texto por orador (regex sobre los encabezados tipo
         "Sr./Sra. APELLIDO.-") y construir un make_record(...) por intervención.
    """
    raise NotImplementedError(
        "Parseo pendiente: requiere inspeccionar la estructura real de "
        "diputados.gov.ar (bloqueada en este entorno por la allowlist de red)."
    )
