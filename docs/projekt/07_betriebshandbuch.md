# Betriebshandbuch

**Stand:** 11.11.2026 · **Art des Dokuments:** nachträglich erstellt aus der Praxis der Entwicklung. Gilt für den Prototyp auf einem einzelnen Rechner.

## Voraussetzungen

- Windows, macOS oder Linux mit Docker (Compose)
- Ollama mit dem Modell `qwen2.5:7b`. Eine Grafikkarte mit 8 GB reicht für etwa 6 Sekunden je Mail, auf der CPU wird es deutlich langsamer.
- Die Datei `.env` mit Zugangsdaten (Vorlage `.env.example`). Die Geheimnisse liegen als Docker-Secrets in Dateien, nicht in der Umgebung der Container.

## Start und Stopp

```bash
docker compose up -d          # alles starten, beim ersten Start entstehen Datenbank und Workflows
docker compose ps             # Zustand ansehen
docker compose stop           # anhalten, Daten bleiben erhalten
docker compose down -v        # ACHTUNG: löscht alle Daten (Datenbank und n8n)
```

Nach einem Neustart von n8n dauert es 10 bis 30 Sekunden, bis die Seiten antworten. Vorher kommt kurz „404".

Ollama muss laufen (`ollama serve`, Adresse in `.env` bei `OLLAMA_BASE_URL`). Ohne Ollama landen alle Mails nach drei Versuchen mit dem Grund „Modell nicht erreichbar" in der Prüfliste.

## Adressen

| Adresse | Zweck |
|---|---|
| `http://localhost:5678` | n8n-Oberfläche (beim ersten Aufruf Konto anlegen) |
| `http://localhost:5678/webhook/arbeitsliste` | Arbeitsliste (Login aus `.env`: `REVIEW_USER`, `REVIEW_PASSWORD`) |
| `POST /webhook/lieferanten-mail` | Eingang für Mails (Header `X-Webhook-Token`) |
| `/form/entwurf`, `/form/review` | Formulare |

## Änderungen einspielen

Die Workflows liegen im Repository und werden beim Start eingespielt. Nach einer Änderung an den Dateien in `workflows/`:

```bash
docker compose up n8n-import      # Workflows und Zugangsdaten neu einspielen
docker compose restart n8n        # n8n lädt die neue Fassung
```

Änderungen, die jemand in der n8n-Oberfläche gemacht hat, holt `python scripts/export_workflows.py` zurück ins Repository.

## Datenbank

Zugriff zum Nachsehen:

```bash
docker compose exec postgres psql -U n8n -d triage -c "SELECT id, kategorie, team, status FROM tickets ORDER BY id DESC LIMIT 20;"
```

**Neue Spalten und Tabellen bei bestehenden Installationen:** `db/init.sql` läuft nur beim allerersten Start. Spätere Ergänzungen müssen von Hand eingespielt werden. Bisher betroffen:

- Spalte `inhalts_hash` in `tickets` und `review_queue` (Duplikaterkennung über den Inhalt)
- Tabelle `app_geheimnis` (Token des Erledigt-Knopfs)
- Zeilen für die fünf neuen Kategorien in `team_routing`

Die genauen Anweisungen stehen in der Beschreibung der Pull Requests 9, 10 und 14 sowie in `db/init.sql`.

## Sichern und Wiederherstellen

Sichern (Ordner `backups/` ist von Git ausgeschlossen):

```bash
docker compose exec -T postgres pg_dump -U n8n -d triage > backups/triage_sicherung.sql
```

Wiederherstellen (ersetzt die Datenbank vollständig):

```bash
docker compose stop n8n
docker compose exec -T postgres psql -U n8n -d n8n -c "DROP DATABASE triage"
docker compose exec -T postgres psql -U n8n -d n8n -c "CREATE DATABASE triage OWNER n8n"
docker compose exec -T postgres psql -U n8n -d triage < backups/triage_sicherung.sql
docker compose start n8n
```

Das Verfahren wurde am 10.11.2026 einmal erfolgreich angewendet. Eine automatische Sicherung gibt es nicht.

## Beispieldaten und Auswertung

```bash
python scripts/demo_laden.py              # Beispielmails für eine Vorführung laden
python scripts/demo_laden.py --loeschen   # wieder entfernen
python scripts/evaluate.py --set pruefset4
```

`evaluate.py` schreibt Test-Tickets in die echte Datenbank und löscht sie nach dem Lauf wieder. **Nicht im Echtbetrieb ausführen.**

## Störungen

| Symptom | Ursache | Abhilfe |
|---|---|---|
| Alle Mails landen in der Prüfliste mit „Modell nicht erreichbar" | Ollama läuft nicht oder falsche Adresse | Ollama starten, `OLLAMA_BASE_URL` prüfen |
| Arbeitsliste zeigt „404" | n8n startet noch oder Workflow nicht veröffentlicht | 30 Sekunden warten, sonst `docker compose up n8n-import` und Neustart |
| Arbeitsliste verlangt immer wieder die Anmeldung | falscher Zugang | Wert in `.env` prüfen |
| „Erledigt" tut nichts, Fehler 400 | Token passt nicht (Seite veraltet, Geheimnis geändert) | Seite neu laden |
| Weiterleitung nach dem Formular führt ins Leere | läuft nicht unter `localhost:5678` | Adresse in den Formular-Knoten (Workflows 02 und 04) anpassen |
| Neue Mail wird als Duplikat abgewiesen | gleicher Inhalt innerhalb von 30 Tagen | gewollt, sonst Ticket in der Datenbank prüfen |
| Unerwartete Fehler | – | Tabelle `fehler_log` und das Ausführungsprotokoll in n8n ansehen |

## Pflege

- Schwellen der AB-Prüfung: Tabelle `einstellungen`. Zuständigkeiten: Tabelle `team_routing`. Beides ohne Änderung am Workflow.
- Qualität nach jeder Änderung neu messen (`04_testkonzept_und_testbericht.md`).
- Lizenzbedingungen von n8n, Ollama und dem Modell vor einem kommerziellen Einsatz prüfen.
