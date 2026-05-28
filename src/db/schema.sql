-- Esquema de la base de discursos del Congreso argentino.
-- Una fila = una intervención (discurso) de un orador en una sesión.

CREATE TABLE IF NOT EXISTS speeches (
    id          INTEGER PRIMARY KEY,
    chamber     TEXT NOT NULL,            -- 'diputados' | 'senado'
    session     TEXT,                     -- p.ej. "8ª Sesión Ordinaria"
    date        TEXT,                      -- ISO 8601: YYYY-MM-DD
    speaker     TEXT,                      -- nombre del/la orador/a
    party       TEXT,                      -- bloque / interbloque
    province    TEXT,                      -- distrito que representa
    text        TEXT NOT NULL,            -- texto de la intervención
    source_url  TEXT,                      -- URL de la versión taquigráfica
    source_id   TEXT,                      -- id estable de la fuente (dedup)
    created_at  TEXT DEFAULT (datetime('now'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_speeches_source
    ON speeches(source_id) WHERE source_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_speeches_chamber ON speeches(chamber);
CREATE INDEX IF NOT EXISTS idx_speeches_date    ON speeches(date);
CREATE INDEX IF NOT EXISTS idx_speeches_speaker ON speeches(speaker);

-- Índice full-text. remove_diacritics 2 => "obra publica" matchea "obra pública".
CREATE VIRTUAL TABLE IF NOT EXISTS speeches_fts USING fts5(
    text,
    speaker,
    content='speeches',
    content_rowid='id',
    tokenize="unicode61 remove_diacritics 2"
);

-- Triggers para mantener el índice FTS sincronizado con la tabla base.
CREATE TRIGGER IF NOT EXISTS speeches_ai AFTER INSERT ON speeches BEGIN
    INSERT INTO speeches_fts(rowid, text, speaker)
    VALUES (new.id, new.text, new.speaker);
END;

CREATE TRIGGER IF NOT EXISTS speeches_ad AFTER DELETE ON speeches BEGIN
    INSERT INTO speeches_fts(speeches_fts, rowid, text, speaker)
    VALUES ('delete', old.id, old.text, old.speaker);
END;

CREATE TRIGGER IF NOT EXISTS speeches_au AFTER UPDATE ON speeches BEGIN
    INSERT INTO speeches_fts(speeches_fts, rowid, text, speaker)
    VALUES ('delete', old.id, old.text, old.speaker);
    INSERT INTO speeches_fts(rowid, text, speaker)
    VALUES (new.id, new.text, new.speaker);
END;
