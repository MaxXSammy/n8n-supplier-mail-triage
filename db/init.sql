-- Läuft beim ersten Start des Postgres-Containers. Die Datenbank n8n legt der Container selbst an.
CREATE DATABASE triage;
\connect triage

-- Routing-Tabelle: Welche Kategorie landet bei welchem Team.
-- Liegt in der Datenbank statt im Workflow, damit der Fachbereich sie ohne Workflow-Änderung pflegen kann.
CREATE TABLE team_routing (
    kategorie   TEXT PRIMARY KEY,
    team        TEXT NOT NULL,
    postfach    TEXT NOT NULL
);

INSERT INTO team_routing (kategorie, team, postfach) VALUES
    ('angebot',      'Strategischer Einkauf',   'einkauf-strategie@hagemann-antriebstechnik.example'),
    ('reklamation',  'Qualitätsmanagement',     'qm@hagemann-antriebstechnik.example'),
    ('lieferverzug', 'Disposition',             'dispo@hagemann-antriebstechnik.example'),
    ('rechnung',     'Kreditorenbuchhaltung',   'kreditoren@hagemann-antriebstechnik.example'),
    ('sonstiges',    'Einkauf Sammelpostfach',  'einkauf@hagemann-antriebstechnik.example');

CREATE TABLE tickets (
    id                  SERIAL PRIMARY KEY,
    mail_id             TEXT NOT NULL UNIQUE,        -- Message-ID der Mail: verhindert doppelte Tickets
    kategorie           TEXT NOT NULL REFERENCES team_routing (kategorie),
    team                TEXT NOT NULL,
    absender            TEXT,
    betreff             TEXT,
    lieferant           TEXT,
    bestellnummer       TEXT,
    rechnungsnummer     TEXT,
    angebotsnummer      TEXT,
    artikel             TEXT,
    betrag              NUMERIC(14, 2),
    waehrung            TEXT,
    neuer_liefertermin  DATE,
    dringlichkeit       TEXT,
    zusammenfassung     TEXT,
    konfidenz           NUMERIC(3, 2),
    quelle              TEXT NOT NULL CHECK (quelle IN ('automatisch', 'review')),
    warnungen           JSONB NOT NULL DEFAULT '[]',
    status              TEXT NOT NULL DEFAULT 'offen',
    erstellt_am         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Human-in-the-loop: Mails, die das System nicht sicher selbst zuordnen darf
CREATE TABLE review_queue (
    id                      SERIAL PRIMARY KEY,
    mail_id                 TEXT NOT NULL UNIQUE,
    gruende                 JSONB NOT NULL,          -- z. B. ["konfidenz_niedrig", "bankdatenaenderung"]
    mail                    JSONB NOT NULL,
    llm_ausgabe             JSONB,                   -- NULL, wenn das LLM nicht erreichbar war
    status                  TEXT NOT NULL DEFAULT 'offen' CHECK (status IN ('offen', 'erledigt', 'verworfen')),
    korrigierte_kategorie   TEXT REFERENCES team_routing (kategorie),
    bearbeitet_von          TEXT,
    notiz                   TEXT,
    ticket_id               INTEGER REFERENCES tickets (id),
    erstellt_am             TIMESTAMPTZ NOT NULL DEFAULT now(),
    erledigt_am             TIMESTAMPTZ
);

-- Unerwartete Fehler aus dem Error-Workflow
CREATE TABLE fehler_log (
    id              SERIAL PRIMARY KEY,
    workflow        TEXT,
    node            TEXT,
    fehlermeldung   TEXT,
    execution_id    TEXT,
    execution_url   TEXT,
    erstellt_am     TIMESTAMPTZ NOT NULL DEFAULT now()
);
