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
    ('angebot',              'Strategischer Einkauf',   'einkauf-strategie@hagemann-antriebstechnik.example'),
    ('auftragsbestaetigung', 'Disposition',             'dispo@hagemann-antriebstechnik.example'),
    ('reklamation',          'Qualitätsmanagement',     'qm@hagemann-antriebstechnik.example'),
    ('lieferverzug',         'Disposition',             'dispo@hagemann-antriebstechnik.example'),
    ('rechnung',             'Kreditorenbuchhaltung',   'kreditoren@hagemann-antriebstechnik.example'),
    ('sonstiges',            'Einkauf Sammelpostfach',  'einkauf@hagemann-antriebstechnik.example');

-- Einstellungen für die AB-Prüfung, vom Einkauf ohne Workflow-Änderung anpassbar
CREATE TABLE einstellungen (
    schluessel      TEXT PRIMARY KEY,
    wert            NUMERIC NOT NULL,
    beschreibung    TEXT NOT NULL
);

INSERT INTO einstellungen (schluessel, wert, beschreibung) VALUES
    ('liefertreue_schwelle_kritisch', 90, 'Mindest-Liefertreue in % für automatische AB-Bestätigung bei AX-, AY-, BX- und CX-Artikeln'),
    ('liefertreue_schwelle_standard', 80, 'Mindest-Liefertreue in % für alle übrigen Artikel (Slow Mover, geringwertig, hoher Puffer)'),
    ('blindbestaetigung_minuten',     30, 'Kommt die AB schneller als so viele Minuten nach dem Bestellversand, gilt sie als ungeprüft bestätigt');

-- Stammdaten, wie sie im ERP stünden. Liefertreue NULL = noch keine Historie.
CREATE TABLE lieferanten (
    id                  SERIAL PRIMARY KEY,
    name                TEXT NOT NULL,
    mail_domain         TEXT NOT NULL UNIQUE,
    ansprechpartner     TEXT NOT NULL,
    anrede              TEXT NOT NULL CHECK (anrede IN ('Frau', 'Herr')),
    liefertreue_prozent NUMERIC(5, 1),
    neu                 BOOLEAN NOT NULL DEFAULT false,   -- neu gelistet, z. B. nach Trial Order
    einkaeufer          TEXT NOT NULL,
    einkaeufer_mail     TEXT NOT NULL
);

INSERT INTO lieferanten (name, mail_domain, ansprechpartner, anrede, liefertreue_prozent, neu, einkaeufer, einkaeufer_mail) VALUES
    ('Alpen Drehtechnik GmbH',          'alpen-drehtechnik.example',          'Katharina Gruber', 'Frau', 96.0, false, 'Maximilian Schneider', 'm.schneider@hagemann-antriebstechnik.example'),
    ('Brenner Zerspanung GmbH',         'brenner-zerspanung.example',         'Stefan Huber',     'Herr', 88.0, false, 'Maximilian Schneider', 'm.schneider@hagemann-antriebstechnik.example'),
    ('Feldmann Präzisionsteile GmbH',   'feldmann-praezisionsteile.example',  'Anja Feldmann',    'Frau', 93.0, false, 'Julia Weber',          'j.weber@hagemann-antriebstechnik.example'),
    ('Officina Meccanica Rossi S.r.l.', 'officina-rossi.example',             'Marco Bellini',    'Herr', 83.0, false, 'Julia Weber',          'j.weber@hagemann-antriebstechnik.example'),
    ('Rheinwerk Komponenten GmbH',      'rheinwerk-komponenten.example',      'Jens Albrecht',    'Herr', 72.0, false, 'Maximilian Schneider', 'm.schneider@hagemann-antriebstechnik.example'),
    ('Swiss Turning AG',                'swissturning.example',               'Reto Meier',       'Herr', 98.0, false, 'Julia Weber',          'j.weber@hagemann-antriebstechnik.example'),
    ('Kovotech s.r.o.',                 'kovotech.example',                   'Petr Novák',       'Herr', 91.0, false, 'Maximilian Schneider', 'm.schneider@hagemann-antriebstechnik.example'),
    ('Precimet Sp. z o.o.',             'precimet.example',                   'Agnieszka Wójcik', 'Frau', 79.0, false, 'Julia Weber',          'j.weber@hagemann-antriebstechnik.example'),
    ('Nordform Kunststofftechnik GmbH', 'nordform.example',                   'Lisa Brandt',      'Frau', NULL, true,  'Maximilian Schneider', 'm.schneider@hagemann-antriebstechnik.example');

-- Offene Bestellungen (eine Position je Bestellung, zur Vereinfachung)
CREATE TABLE bestellungen (
    bestellnummer   TEXT PRIMARY KEY,
    lieferant_id    INTEGER NOT NULL REFERENCES lieferanten (id),
    artikelnr       TEXT NOT NULL,
    artikel         TEXT NOT NULL,
    abc_xyz         TEXT NOT NULL CHECK (abc_xyz ~ '^[ABC][XYZ]$'),
    menge           NUMERIC(12, 2) NOT NULL,
    einheit         TEXT NOT NULL DEFAULT 'Stk',
    einzelpreis     NUMERIC(12, 4) NOT NULL,
    waehrung        TEXT NOT NULL,
    wunschtermin    DATE NOT NULL,
    versendet_am    TIMESTAMPTZ NOT NULL
);

INSERT INTO bestellungen (bestellnummer, lieferant_id, artikelnr, artikel, abc_xyz, menge, einzelpreis, waehrung, wunschtermin, versendet_am) VALUES
    ('4500018401', 1, 'AW-40', 'Antriebswelle AW-40',          'AX', 2000, 3.12,   'EUR', '2026-11-20', '2026-10-26 09:00+01'),
    ('4500018402', 2, 'WE-12', 'Welle Ø12 x 85',               'AX', 1500, 3.80,   'EUR', '2026-11-27', '2026-10-26 10:00+01'),
    ('4500018403', 2, 'DS-08', 'Distanzscheibe 8 mm',          'CZ', 5000, 0.042,  'EUR', '2026-12-04', '2026-10-26 10:05+01'),
    ('4500018404', 5, 'ZW-25', 'Zahnradwelle ZW-25',           'AY', 2400, 6.40,   'EUR', '2026-11-25', '2026-10-27 08:00+01'),
    ('4500018405', 6, 'PB-6',  'Präzisionsbolzen PB-6',        'BX',  500, 1.85,   'CHF', '2026-11-18', '2026-10-27 13:00+01'),
    ('4500018406', 9, 'KG-30', 'Kunststoffgehäuse KG-30',      'BY',  800, 2.95,   'EUR', '2026-12-01', '2026-10-27 14:00+01'),
    ('4500018407', 7, 'FL-80', 'Flansch FL-80',                'AX', 1800, 5.10,   'EUR', '2026-12-11', '2026-10-28 08:30+01'),
    ('4500018408', 3, 'HS-12', 'Hülse HS-12',                  'BX', 1000, 0.86,   'EUR', '2026-11-30', '2026-10-28 09:00+01'),
    ('4500018409', 8, 'DR-30', 'Distanzring DR-30',            'CY', 1040, 0.48,   'EUR', '2026-12-02', '2026-10-28 10:00+01'),
    ('4500018410', 4, 'AW-40', 'Antriebswelle AW-40',          'BZ', 3000, 2.98,   'EUR', '2026-12-07', '2026-10-28 11:00+01'),
    ('4500018411', 1, 'LB-20', 'Lagerbolzen LB-20',            'AY', 1200, 2.45,   'EUR', '2026-11-14', '2026-10-28 12:00+01'),
    ('4500018412', 6, 'GS-4',  'Gewindestift GS-4',            'CX', 3000, 0.92,   'CHF', '2026-11-21', '2026-10-28 13:00+01'),
    ('4500018413', 7, 'SP-10', 'Spannstift SP-10',             'AX', 4000, 0.31,   'EUR', '2026-12-09', '2026-10-29 09:00+01'),
    ('4500018414', 3, 'BU-22', 'Buchse BU-22',                 'BX', 1500, 1.14,   'EUR', '2026-12-02', '2026-10-29 10:00+01'),
    ('4500018415', 4, 'SR-05', 'Scheibe SR-05',                'BY', 2000, 0.27,   'EUR', '2026-12-10', '2026-10-29 11:00+01'),
    ('4500018416', 8, 'RI-14', 'Ring RI-14',                   'CZ', 2500, 0.19,   'EUR', '2026-12-15', '2026-10-29 12:00+01'),
    ('4500018417', 6, 'AS-3',  'Achsstift AS-3',               'AX',  800, 2.10,   'CHF', '2026-11-26', '2026-10-29 14:00+01'),
    ('4500018418', 1, 'MS-6',  'Madenschraube MS-6',           'AX', 5000, 0.09,   'EUR', '2026-12-03', '2026-10-29 15:00+01'),
    ('4500018525', 2, 'NK-16', 'Nutenkeil NK-16',              'BY',  600, 1.20,   'EUR', '2026-12-03', '2026-10-29 08:00+01');

CREATE TABLE tickets (
    id                  SERIAL PRIMARY KEY,
    mail_id             TEXT NOT NULL UNIQUE,        -- Message-ID der Mail: verhindert doppelte Tickets
    kategorie           TEXT NOT NULL REFERENCES team_routing (kategorie),
    team                TEXT NOT NULL,
    zustaendig          TEXT,                        -- bei AB-Prüfung: zuständiger Einkäufer
    absender            TEXT,
    betreff             TEXT,
    lieferant           TEXT,
    bestellnummer       TEXT,
    rechnungsnummer     TEXT,
    angebotsnummer      TEXT,
    artikel             TEXT,
    einzelpreis         NUMERIC(12, 4),
    menge               NUMERIC(12, 2),
    betrag              NUMERIC(14, 2),
    waehrung            TEXT,
    liefertermin        DATE,
    dringlichkeit       TEXT,
    zusammenfassung     TEXT,
    konfidenz           NUMERIC(3, 2),
    quelle              TEXT NOT NULL CHECK (quelle IN ('automatisch', 'review')),
    warnungen           JSONB NOT NULL DEFAULT '[]',
    ab_pruefung         JSONB,                       -- Ergebnis des Abgleichs mit der Bestellung
    status              TEXT NOT NULL DEFAULT 'offen',
    erstellt_am         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Antwortentwürfe an Lieferanten. Der zuständige Mitarbeiter prüft und sendet selbst.
CREATE TABLE entwuerfe (
    id              SERIAL PRIMARY KEY,
    ticket_id       INTEGER NOT NULL REFERENCES tickets (id),
    empfaenger      TEXT NOT NULL,
    betreff         TEXT NOT NULL,
    text            TEXT NOT NULL,
    foermlichkeit   TEXT NOT NULL CHECK (foermlichkeit IN ('förmlich', 'locker')),
    nachdruck       TEXT NOT NULL CHECK (nachdruck IN ('mit Nachdruck', 'gelassen')),
    erstellt_von    TEXT NOT NULL,
    warnungen       JSONB NOT NULL DEFAULT '[]',
    erstellt_am     TIMESTAMPTZ NOT NULL DEFAULT now()
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
