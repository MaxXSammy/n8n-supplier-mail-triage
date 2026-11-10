-- Vorgangshistorie und Vereinbarungen: Was mit einem Lieferanten abgesprochen ist, damit Vertretung und Neueinsteiger
-- eine Preiserhöhung richtig einordnen (z. B. "Festpreis bis Q1/2027"). Dazu Ziel und Regeln für die Kennzahlen oben.
-- Läuft bei einer neuen Datenbank automatisch nach 05_abteilungen.sql. Eine bestehende Datenbank aktualisieren:
--   docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER"' < db/06_vereinbarungen.sql
\connect triage

-- Absprachen je Lieferant, optional nur für einen Artikel. Im echten Einsatz Rahmenverträge und Konditionen aus dem ERP.
CREATE TABLE IF NOT EXISTS vereinbarungen (
    id              SERIAL PRIMARY KEY,
    lieferant_id    INTEGER NOT NULL REFERENCES lieferanten (id),
    artikelnr       TEXT,                     -- NULL = gilt für alle Artikel des Lieferanten
    art             TEXT NOT NULL CHECK (art IN ('festpreis', 'preisgleitklausel', 'sonstiges')),
    gueltig_bis     DATE,
    text            TEXT NOT NULL,
    UNIQUE (lieferant_id, art, text)
);

INSERT INTO vereinbarungen (lieferant_id, artikelnr, art, gueltig_bis, text) VALUES
    (7, 'FL-80', 'festpreis',         '2027-03-31', 'Festpreis bis Q1/2027 laut Rahmenvertrag RV-2025-014'),
    (1, NULL,    'preisgleitklausel', '2027-12-31', 'Preisgleitklausel Stahl: Anpassung nur mit Index-Nachweis und erst ab 5 % Indexänderung'),
    (8, NULL,    'sonstiges',         '2026-12-31', 'Lieferantenentwicklung: Liefertreue-Ziel 90 % bis Jahresende, Review im Januar'),
    (5, NULL,    'sonstiges',         NULL,         'Zweitlieferant für ZW-25 in Qualifizierung (Erstmuster bei Brenner Zerspanung)')
ON CONFLICT (lieferant_id, art, text) DO NOTHING;

INSERT INTO einstellungen (schluessel, wert, beschreibung) VALUES
    ('cost_avoidance_ziel_euro', 100000, 'Jahresziel für vermiedene Mehrkosten (Jahreswirkung abgelehnter Preiserhöhungen)'),
    ('rueckstau_tage',           2,      'Eine offene Aufgabe, die älter ist als so viele Tage, gilt als Rückstau (Streak "Tage ohne Rückstau")')
ON CONFLICT (schluessel) DO NOTHING;
