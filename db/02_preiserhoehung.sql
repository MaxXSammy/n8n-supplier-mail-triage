-- Ausbau Preiserhöhung: eigene Kategorie, Preishistorie, Schwellen und Aufgaben je Team.
-- Läuft bei einer neuen Datenbank automatisch nach init.sql. Eine bestehende Datenbank aktualisieren:
--   docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER"' < db/02_preiserhoehung.sql
-- Das Skript ist wiederholbar: Bereits vorhandene Tabellen und Zeilen bleiben unverändert.
\connect triage

INSERT INTO team_routing (kategorie, team, postfach) VALUES
    ('preiserhoehung', 'Einkauf', 'einkauf@hagemann-antriebstechnik.example')
ON CONFLICT (kategorie) DO NOTHING;

-- Wann die Disposition eine Preiserhöhung in einer AB selbst freigeben darf und ab wann der strategische Einkauf informiert wird
INSERT INTO einstellungen (schluessel, wert, beschreibung) VALUES
    ('preis_toleranz_dispo_prozent',       5,   'Bis zu dieser Preiserhöhung in % darf die Disposition eine AB selbst freigeben'),
    ('preis_toleranz_dispo_euro',          500, 'und nur, wenn die Mehrkosten auf die Bestellung höchstens so viele Euro betragen'),
    ('preis_eskalation_strategie_prozent', 10,  'Ab dieser Preiserhöhung in % bekommt der strategische Einkauf eine Info')
ON CONFLICT (schluessel) DO NOTHING;

-- Preise je Lieferant und Artikel, wie sie im ERP als Konditionshistorie stünden.
-- aenderung_prozent NULL = Erstlistung ohne Vorgängerpreis.
CREATE TABLE IF NOT EXISTS preis_historie (
    id                  SERIAL PRIMARY KEY,
    lieferant_id        INTEGER NOT NULL REFERENCES lieferanten (id),
    artikelnr           TEXT NOT NULL,
    preis               NUMERIC(12, 4) NOT NULL,
    waehrung            TEXT NOT NULL,
    gueltig_ab          DATE NOT NULL,
    aenderung_prozent   NUMERIC(6, 2),
    anlass              TEXT,
    UNIQUE (lieferant_id, artikelnr, gueltig_ab)
);

INSERT INTO preis_historie (lieferant_id, artikelnr, preis, waehrung, gueltig_ab, aenderung_prozent, anlass) VALUES
    (1, 'AW-40', 3.06,  'EUR', '2024-07-01', NULL, 'Erstlistung'),
    (1, 'AW-40', 3.12,  'EUR', '2025-07-01', 2.0,  'Lohnkosten'),
    (1, 'LB-20', 2.45,  'EUR', '2025-01-01', NULL, 'Erstlistung'),
    (1, 'MS-6',  0.09,  'EUR', '2024-01-01', NULL, 'Erstlistung'),
    (5, 'ZW-25', 6.10,  'EUR', '2025-01-01', NULL, 'Erstlistung'),
    (5, 'ZW-25', 6.40,  'EUR', '2026-01-15', 4.9,  'Energiekosten'),
    (6, 'PB-6',  1.85,  'CHF', '2025-03-01', NULL, 'Erstlistung'),
    (7, 'FL-80', 4.85,  'EUR', '2024-01-01', NULL, 'Erstlistung'),
    (7, 'FL-80', 5.10,  'EUR', '2026-04-01', 5.2,  'Stahlpreise'),
    (7, 'SP-10', 0.30,  'EUR', '2025-02-01', NULL, 'Erstlistung'),
    (7, 'SP-10', 0.31,  'EUR', '2026-04-01', 3.3,  'Stahlpreise'),
    (8, 'DR-30', 0.44,  'EUR', '2025-01-01', NULL, 'Erstlistung'),
    (8, 'DR-30', 0.48,  'EUR', '2026-06-01', 9.1,  'Rohstoffzuschlag'),
    (8, 'RI-14', 0.19,  'EUR', '2025-01-01', NULL, 'Erstlistung')
ON CONFLICT (lieferant_id, artikelnr, gueltig_ab) DO NOTHING;

-- Aus einer Mail entsteht ein Ticket (der Vorgang), aus dem Ticket eine oder mehrere Aufgaben für verschiedene Teams.
-- Beispiel: AB mit 8 % Preiserhöhung = Disposition prüft den Termin, der Einkäufer prüft den Preis.
CREATE TABLE IF NOT EXISTS aufgaben (
    id              SERIAL PRIMARY KEY,
    ticket_id       INTEGER NOT NULL REFERENCES tickets (id),
    team            TEXT NOT NULL,
    zustaendig      TEXT,
    art             TEXT NOT NULL,       -- z. B. liefertermin_pruefen, preis_freigeben, preiserhoehung_pruefen, preis_info
    prioritaet      TEXT NOT NULL DEFAULT 'normal' CHECK (prioritaet IN ('normal', 'hoch')),
    status          TEXT NOT NULL DEFAULT 'offen' CHECK (status IN ('offen', 'erledigt', 'info')),
    details         JSONB NOT NULL DEFAULT '{}',
    erstellt_am     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Tickets aus der Zeit vor den Aufgaben bekommen je eine Aufgabe für ihr Team, damit die Arbeitsliste sie weiter zeigt
INSERT INTO aufgaben (ticket_id, team, zustaendig, art, status)
SELECT t.id, t.team, t.zustaendig, 'bearbeiten', CASE WHEN t.status = 'offen' THEN 'offen' ELSE 'erledigt' END
FROM tickets t
WHERE NOT EXISTS (SELECT 1 FROM aufgaben a WHERE a.ticket_id = t.id);
