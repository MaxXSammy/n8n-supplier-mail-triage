# Anforderungen und Umsetzungsstand

**Stand:** 11.11.2026 · **Art des Dokuments:** nachträglich zusammengefasst aus Fachkonzept (`docs/fachkonzept.md`), README und Code

Priorität: **M** = muss, **S** = soll, **K** = kann. Status: erfüllt, teilweise, offen. Der Nachweis nennt, wo man es prüfen kann.

## Funktionale Anforderungen

| ID | Anforderung | Prio | Status | Nachweis |
|---|---|---|---|---|
| F-01 | Mails per Schnittstelle (Webhook) annehmen, Pflichtfelder und Größe prüfen, HTML bereinigen | M | erfüllt | Workflow 01, `scripts/robustheit.py` |
| F-02 | Mail einer von elf Kategorien zuordnen | M | erfüllt, mit Einschränkungen | Prüfsatz 4: 78 % richtig, 86 % bei Lieferanten-Mails |
| F-03 | Nummern, Beträge, Termine auslesen, jeder Wert muss im Mailtext stehen (Belegprüfung) | M | erfüllt | `eval/ergebnisse*.md`, Extraktion 96 bis 100 % je Satz |
| F-04 | Zuständigkeit über eine Tabelle festlegen, ohne Workflow-Änderung pflegbar | M | erfüllt | Tabelle `team_routing` |
| F-05 | Doppelte Mails erkennen (gleiche Nachricht und gleicher Inhalt unter neuer ID) | M | erfüllt | Workflow 01, Test vom 11.11.2026 |
| F-06 | AB mit Bestellung abgleichen: Preis, Menge, Termin, Währung | M | erfüllt | Prüfsatz 4: AB-Entscheidung 12 von 13 |
| F-07 | AB-Regeln: Liefertreue-Schwellen (90 % und 80 %), neuer Lieferant, Blindbestätigung unter 30 Minuten, abweichende Absender-Domain | M | erfüllt | `docs/fachkonzept.md`, Tabelle `einstellungen` |
| F-08 | Änderung von Bankdaten, Adresse oder USt-ID immer an einen Menschen | M | erfüllt | 14 von 14 in allen Prüfsätzen |
| F-09 | Eingeschleuste Anweisungen („Ignoriere alle Anweisungen") erkennen und prüfen lassen | M | teilweise | Regelbasiert, umgehbar (Grenzen siehe Risiken) |
| F-10 | Unsichere und fehlerhafte Fälle in eine Prüfliste, Abschluss per Formular | M | erfüllt | Workflow 02, im Review nur die Kategorie korrigierbar |
| F-11 | Antwortentwurf bei AB-Abweichung aus Vorlagen, Ton wählbar | S | erfüllt | Workflow 04 |
| F-12 | Anfrage-Entwurf (RFQ) im Format für den Procurement-RAG-Agent | K | erfüllt | Arbeitsliste, Angebot und Preisänderung |
| F-13 | Arbeitsliste nach Team mit Zusammenfassung, Warnungen, Suche, Filter, Erledigt | M | erfüllt | Workflow 02, Screenshot in `docs/arbeitsliste.png` |
| F-14 | Fehlerbehandlung: Modell nicht erreichbar führt in die Prüfliste, unerwartete Fehler in ein Protokoll | M | erfüllt | Error-Workflow, Tabelle `fehler_log` |
| F-15 | Anschluss an ein echtes Postfach (IMAP, nur lesen) | M (Pilot) | **offen** | – |
| F-16 | PDF-Anhänge lesen | S | **offen** | – |
| F-17 | Bestell- und Lieferantendaten aus dem ERP statt aus einer eigenen Tabelle | M (Pilot) | **offen** | – |
| F-18 | Persönliche Benutzer, Nachweis, wer was entschieden hat | M (Pilot) | **offen** | – |
| F-19 | Interne Mails und Systemmeldungen sicher erkennen und weiterleiten | S | teilweise | nur 13 von 25 richtig (Prüfsatz 4) |
| F-20 | Weitere Mailtypen aus dem Fachkonzept (Projektstatus-Anfrage, Terminanfrage, AGB-Änderung) | K | **offen** | `docs/fachkonzept.md` |

## Nicht-funktionale Anforderungen

| ID | Anforderung | Prio | Status | Nachweis |
|---|---|---|---|---|
| N-01 | Verarbeitung lokal, keine Mails an Cloud-Dienste | M | erfüllt | Architektur, `docker-compose.yml` |
| N-02 | Antwortzeit je Mail im Bereich weniger Sekunden | S | erfüllt | etwa 6 Sekunden auf einer Grafikkarte mit 8 GB |
| N-03 | Nachvollziehbar: Grund für eine Prüfung steht sichtbar am Fall | M | erfüllt | Warnungen und Chips in der Arbeitsliste |
| N-04 | Kein automatischer Versand von Mails, keine Buchungen | M | erfüllt | Architektur, Entwürfe öffnen sich im Mailprogramm |
| N-05 | Reproduzierbare Installation mit einem Befehl | S | erfüllt | `docker compose up -d`, CI prüft die Konfiguration |
| N-06 | Geheimnisse nicht im Klartext und nicht in der Umgebung der Container | M | erfüllt | Docker-Secrets |
| N-07 | Eingaben abgesichert (SQL-Injection, Skript in Betreff, Größenlimit) | M | erfüllt | `scripts/robustheit.py`, zwölf Fälle |
| N-08 | Löschkonzept für gespeicherte Mails und Tickets | M (Pilot) | **offen** | siehe `05_risiken_und_datenschutz.md` |
| N-09 | Sicherung und Wiederherstellung der Datenbank | S | teilweise | manuell beschrieben im Betriebshandbuch |
| N-10 | Bedienbar im Browser am Rechner | S | erfüllt | mobil ausdrücklich kein Ziel |

## Offene Punkte für den Pilot

F-15, F-17, F-18, N-08. Ohne diese vier ist ein Betrieb mit echten Mails nicht sinnvoll.
