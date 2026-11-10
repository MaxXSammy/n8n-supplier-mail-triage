-- Ausbau Einkaufssteuerung: Jahresbedarf und Konditionen je Artikel, Eskalationsstufen, AB-Status der Bestellungen
-- und ein Audit-Protokoll, das sich nur ergänzen, aber nicht ändern lässt.
-- Läuft bei einer neuen Datenbank automatisch nach 02_preiserhoehung.sql. Eine bestehende Datenbank aktualisieren:
--   docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER"' < db/03_einkaufssteuerung.sql
\connect triage

-- Eskalation nach Jahreswirkung statt nach Einzelbestellung. Gestuft, damit die Geschäftsleitung nur große Fälle sieht:
-- Ein fester Alarm schon ab 5.000 € würde bei jeder zweiten Erhöhung auf einen A-Artikel auslösen und bald ignoriert.
INSERT INTO einstellungen (schluessel, wert, beschreibung) VALUES
    ('eskalation_einkaufsleitung_euro',    5000,  'Ab diesen jährlichen Mehrkosten (Full-Year-Effekt) bekommt die Einkaufsleitung eine Aufgabe'),
    ('eskalation_geschaeftsleitung_euro',  50000, 'Ab diesen jährlichen Mehrkosten bekommt zusätzlich die Geschäftsleitung eine Aufgabe'),
    ('eskalation_liefertreue_prozent',     85,    'Liefertreue unter diesem Wert und eine Erhöhung über der nächsten Schwelle: Einkaufsleitung, Alternativlieferant prüfen'),
    ('eskalation_liefertreue_preis_prozent', 10,  'Preiserhöhung in %, ab der die schlechte Liefertreue zur Eskalation führt'),
    ('wechselkurs_chf_eur',                1.06,  'Fester Umrechnungskurs für Schwellen in Euro (im echten Einsatz tagesaktuell aus dem ERP)')
ON CONFLICT (schluessel) DO NOTHING;

-- Konditionen je Lieferant und Artikel, wie sie im Einkaufsinfosatz des ERP stünden.
-- jahresbedarf NULL = keine Historie (z. B. Neulieferant): Der Full-Year-Effekt wird dann als "fehlt" gemeldet, nicht als 0 €.
CREATE TABLE IF NOT EXISTS artikel_konditionen (
    lieferant_id    INTEGER NOT NULL REFERENCES lieferanten (id),
    artikelnr       TEXT NOT NULL,
    jahresbedarf    NUMERIC(12, 2),        -- Stück pro Jahr (Verbrauch der letzten zwölf Monate oder Planbedarf)
    vpe             INTEGER CHECK (vpe > 0),   -- Verpackungseinheit in Stück
    moq             INTEGER CHECK (moq > 0),   -- Mindestbestellmenge in Stück
    PRIMARY KEY (lieferant_id, artikelnr)
);

INSERT INTO artikel_konditionen (lieferant_id, artikelnr, jahresbedarf, vpe, moq) VALUES
    (1, 'AW-40', 24000,  500,  1000),
    (1, 'LB-20', 9600,   100,  500),
    (1, 'MS-6',  60000,  1000, 5000),
    (2, 'WE-12', 18000,  50,   500),
    (2, 'DS-08', 60000,  1000, 5000),
    (2, 'NK-16', 7200,   100,  300),
    (3, 'HS-12', 300000, 48,   480),
    (3, 'BU-22', 250000, 50,   500),
    (4, 'AW-40', 36000,  500,  1000),
    (4, 'SR-05', 24000,  500,  2000),
    (5, 'ZW-25', 24000,  100,  600),
    (6, 'PB-6',  6000,   100,  500),
    (6, 'GS-4',  36000,  500,  1000),
    (6, 'AS-3',  9600,   100,  400),
    (7, 'FL-80', 14000,  50,   600),
    (7, 'SP-10', 48000,  1000, 4000),
    (8, 'DR-30', 12000,  40,   400),   -- VPE 40 ist falsch gepflegt, der Lieferant liefert in 50er-Einheiten (Mail 24)
    (8, 'RI-14', 30000,  500,  2500),
    (9, 'KG-30', NULL,   50,   200)
ON CONFLICT (lieferant_id, artikelnr) DO NOTHING;

-- Wann der Lieferant die Bestellung bestätigt hat. Für bestätigte Bestellungen gilt der vereinbarte Preis,
-- eine später angekündigte Erhöhung gilt dafür nur mit unserer Zustimmung.
ALTER TABLE bestellungen ADD COLUMN IF NOT EXISTS bestaetigt_am TIMESTAMPTZ;
UPDATE bestellungen SET bestaetigt_am = v.am::timestamptz
FROM (VALUES ('4500018401', '2026-10-26 15:00+01'), ('4500018418', '2026-10-30 09:00+01'),
             ('4500018405', '2026-10-27 16:00+01'), ('4500018416', '2026-10-30 10:00+01'),
             ('4500018414', '2026-10-29 14:00+01')) AS v (nr, am)
WHERE bestellnummer = v.nr AND bestaetigt_am IS NULL;

-- Audit-Protokoll für menschliche Entscheidungen. Einträge lassen sich nur anhängen: Ein Trigger verbietet
-- UPDATE, DELETE und TRUNCATE, jede Zeile trägt den Hash ihrer Vorgängerin (Hash-Kette).
-- Das ist manipulationserschwert, aber nicht revisionssicher im Sinne der GoBD: Ein Datenbank-Administrator kann
-- die Trigger abschalten. "Wer" ist der Name aus dem Formular, alle Bearbeiter teilen sich ein Login.
CREATE TABLE IF NOT EXISTS audit_log (
    id          BIGSERIAL PRIMARY KEY,
    zeit        TIMESTAMPTZ NOT NULL DEFAULT clock_timestamp(),
    akteur      TEXT NOT NULL,
    aktion      TEXT NOT NULL,          -- z. B. review_freigegeben, review_verworfen
    objekt      TEXT NOT NULL,          -- z. B. review_queue
    objekt_id   TEXT NOT NULL,
    details     JSONB NOT NULL DEFAULT '{}',
    vorher_hash TEXT,
    hash        TEXT NOT NULL
);

CREATE OR REPLACE FUNCTION audit_hash(z audit_log) RETURNS TEXT LANGUAGE sql IMMUTABLE AS $$
    -- Zeit in UTC mit festem Format, damit der Hash nicht von Sitzungseinstellungen abhängt
    SELECT encode(sha256(convert_to(concat_ws('|', COALESCE(z.vorher_hash, ''),
        to_char(z.zeit AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US'), z.akteur, z.aktion, z.objekt, z.objekt_id,
        z.details::text), 'UTF8')), 'hex');
$$;

CREATE OR REPLACE FUNCTION audit_verketten() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    -- Sperre, damit zwei gleichzeitige Einträge nicht denselben Vorgänger bekommen
    PERFORM pg_advisory_xact_lock(hashtext('audit_log'));
    SELECT hash INTO NEW.vorher_hash FROM audit_log ORDER BY id DESC LIMIT 1;
    NEW.zeit := clock_timestamp();
    NEW.hash := audit_hash(NEW);
    RETURN NEW;
END $$;

CREATE OR REPLACE FUNCTION audit_unveraenderlich() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'audit_log ist unveränderlich: % ist nicht erlaubt', TG_OP;
END $$;

DROP TRIGGER IF EXISTS audit_verketten ON audit_log;
CREATE TRIGGER audit_verketten BEFORE INSERT ON audit_log FOR EACH ROW EXECUTE FUNCTION audit_verketten();
DROP TRIGGER IF EXISTS audit_kein_update ON audit_log;
CREATE TRIGGER audit_kein_update BEFORE UPDATE OR DELETE ON audit_log FOR EACH ROW EXECUTE FUNCTION audit_unveraenderlich();
DROP TRIGGER IF EXISTS audit_kein_truncate ON audit_log;
CREATE TRIGGER audit_kein_truncate BEFORE TRUNCATE ON audit_log FOR EACH STATEMENT EXECUTE FUNCTION audit_unveraenderlich();

-- Prüft die ganze Kette: Gibt die erste Zeile zurück, deren Hash nicht stimmt, oder NULL, wenn alles intakt ist
CREATE OR REPLACE FUNCTION audit_pruefen() RETURNS BIGINT LANGUAGE plpgsql STABLE AS $$
DECLARE
    z audit_log;
    vorher TEXT := NULL;
BEGIN
    FOR z IN SELECT * FROM audit_log ORDER BY id LOOP
        IF z.vorher_hash IS DISTINCT FROM vorher OR z.hash <> audit_hash(z) THEN
            RETURN z.id;
        END IF;
        vorher := z.hash;
    END LOOP;
    RETURN NULL;
END $$;
