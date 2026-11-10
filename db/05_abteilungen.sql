-- Abteilungsübergreifende Vorgänge: Materialänderung, Werkstoffwechsel, Abkündigung brauchen Technik, QM und Disposition.
-- Läuft bei einer neuen Datenbank automatisch nach 04_aufgaben_entscheiden.sql. Eine bestehende Datenbank aktualisieren:
--   docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER"' < db/05_abteilungen.sql
\connect triage

-- Postfächer der Abteilungen für interne Entwürfe (team_routing ordnet Kategorien zu, hier geht es um Empfänger)
CREATE TABLE IF NOT EXISTS abteilungen (
    team        TEXT PRIMARY KEY,
    postfach    TEXT NOT NULL
);
INSERT INTO abteilungen (team, postfach) VALUES
    ('Technik',                 'technik@hagemann-antriebstechnik.example'),
    ('Qualitätsmanagement',     'qm@hagemann-antriebstechnik.example'),
    ('Disposition',             'dispo@hagemann-antriebstechnik.example'),
    ('Einkaufsleitung',         'einkaufsleitung@hagemann-antriebstechnik.example'),
    ('Geschäftsleitung',        'gl@hagemann-antriebstechnik.example'),
    ('Strategischer Einkauf',   'einkauf-strategie@hagemann-antriebstechnik.example')
ON CONFLICT (team) DO NOTHING;

-- Was die Mail über andere Abteilungen sagt: Merker von Modell und Regel, alter und neuer Werkstoff, Empfehlung des Modells
ALTER TABLE tickets ADD COLUMN IF NOT EXISTS abteilungen JSONB;

-- Entwürfe sind entweder an den Lieferanten oder intern an Abteilungen gerichtet, intern oft mit mehreren Empfängern
ALTER TABLE entwuerfe ADD COLUMN IF NOT EXISTS art TEXT NOT NULL DEFAULT 'lieferant' CHECK (art IN ('lieferant', 'intern'));
ALTER TABLE entwuerfe ADD COLUMN IF NOT EXISTS cc TEXT;
-- Wozu der Entwurf dient (z. B. preis_akzeptiert, unterlagen_anfordern), damit derselbe Entwurf nicht doppelt entsteht
ALTER TABLE entwuerfe ADD COLUMN IF NOT EXISTS zweck TEXT;
