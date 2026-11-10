-- Aufgaben in der Arbeitsliste entscheiden: Freigeben, Ablehnen, Erledigt. Dazu der Mailtext am Ticket für "Mail anzeigen".
-- Läuft bei einer neuen Datenbank automatisch nach 03_einkaufssteuerung.sql. Eine bestehende Datenbank aktualisieren:
--   docker compose exec -T postgres sh -c 'psql -U "$POSTGRES_USER"' < db/04_aufgaben_entscheiden.sql
\connect triage

ALTER TABLE aufgaben ADD COLUMN IF NOT EXISTS entscheidung TEXT CHECK (entscheidung IN ('freigegeben', 'abgelehnt', 'erledigt'));
ALTER TABLE aufgaben ADD COLUMN IF NOT EXISTS erledigt_von TEXT;
ALTER TABLE aufgaben ADD COLUMN IF NOT EXISTS erledigt_am TIMESTAMPTZ;
ALTER TABLE aufgaben ADD COLUMN IF NOT EXISTS notiz TEXT;

-- Bereinigter Mailtext (ohne HTML, gekürzt wie für das LLM), damit der Bearbeiter die Mail in der Arbeitsliste lesen kann
ALTER TABLE tickets ADD COLUMN IF NOT EXISTS mailtext TEXT;
