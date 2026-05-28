# Estudio de discursos del Congreso argentino

Base de datos y agente conversacional (RAG) sobre discursos de la H. Cámara de
Diputados y el H. Senado de la Nación Argentina.

Prototipo end-to-end: **scraping → base SQLite con búsqueda full-text → agente
que responde con Claude citando las fuentes**.

## Estado actual

- ✅ Base de datos (SQLite + FTS5) e ingesta de discursos — funcionando.
- ✅ Recuperación full-text en español (stopwords + matching por prefijo).
- ✅ Agente RAG sobre la API de Claude (requiere `ANTHROPIC_API_KEY`).
- ✅ Muestra de datos **sintéticos** para probar todo sin acceso a la red
  (`data/sample/`).
- 🚧 Scraper de las versiones taquigráficas: el *plumbing* (HTTP con reintentos,
  PDF→texto, normalización) está listo; falta el parseo concreto, que requiere
  inspeccionar el HTML/PDF real de los sitios `.gob.ar`.

> **Datos de muestra**: los discursos en `data/sample/` son **ficticios**
> (oradores y frases inventados), pensados solo para validar el pipeline.
> No representan intervenciones reales.

## Instalación

```bash
pip install -r requirements.txt        # requests, pdfminer.six, anthropic
cp .env.example .env                   # completá ANTHROPIC_API_KEY para el agente
```

## Uso rápido (con la muestra)

```bash
# 1) Construir la base con los discursos de muestra
python scripts/build_db.py

# 2) Buscar pasajes (no requiere API key)
python scripts/ask.py "presupuesto para educación" --retrieve-only

# 3) Preguntarle al agente (requiere ANTHROPIC_API_KEY)
python scripts/ask.py "¿Qué posturas hay sobre la obra pública?"
python scripts/ask.py "energía" --chamber senado --limit 5
```

Si no hay `ANTHROPIC_API_KEY`, `ask.py` cae automáticamente a modo
solo-recuperación.

## Scraping de datos reales

Los sitios oficiales (`datos.hcdn.gob.ar`, `diputados.gov.ar`,
`senado.gob.ar`) **no son accesibles desde el entorno de Claude Code en la web**
por la *allowlist* de red. Para poblar la base con datos reales, corré el
scraper en un entorno con acceso a esos dominios (tu máquina), o ampliá la
política de red del entorno web.

```bash
python scripts/run_scraper.py --chamber diputados --out data/diputados.json
python scripts/build_db.py --input data/diputados.json
```

El parseo (segmentación por orador de cada versión taquigráfica) está marcado
como `TODO` en `src/scraper/diputados.py` y `src/scraper/senado.py`: requiere
ver la estructura real de las páginas/PDF para completarse.

## Estructura

```
src/
  db/        schema.sql, database.py     # SQLite + FTS5
  agent/     retriever.py, agent.py      # búsqueda + RAG con Claude
  scraper/   common.py, diputados.py, senado.py
scripts/
  build_db.py     # JSON -> base de datos
  ask.py          # consultar al agente
  run_scraper.py  # scraping -> JSON
data/sample/      # discursos de muestra (sintéticos)
```

## Esquema de un discurso

Cada fila de la tabla `speeches` es una intervención:

| campo | descripción |
|-------|-------------|
| `chamber` | `diputados` o `senado` |
| `session` | sesión (p.ej. "8ª Sesión Ordinaria") |
| `date` | fecha ISO `YYYY-MM-DD` |
| `speaker` | orador/a |
| `party` | bloque / interbloque |
| `province` | distrito |
| `text` | texto de la intervención |
| `source_url` / `source_id` | trazabilidad y deduplicación |
