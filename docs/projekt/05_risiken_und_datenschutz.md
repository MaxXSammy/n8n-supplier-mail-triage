# Risiken und Datenschutz

**Stand:** 11.11.2026 · **Art des Dokuments:** nachträglich erstellt. Es ist **keine Rechtsberatung**. Vor einem Einsatz mit echten Mails müssen Datenschutz, Betriebsrat (falls vorhanden) und Recht einbezogen werden.

## Risikoregister

Bewertung: W = Wahrscheinlichkeit, A = Auswirkung (niedrig, mittel, hoch).

| ID | Risiko | W | A | Maßnahme | Status |
|---|---|---|---|---|---|
| R-01 | Das Modell ordnet eine Mail falsch ein, sie landet beim falschen Team | mittel | mittel | Pflichtfelder und Plausibilitätsprüfungen, Prüfliste, Messung, Pilot im Schattenbetrieb | offen: 4 von 99 Mails gingen im Test ohne Prüfung an die falsche Stelle |
| R-02 | Eine Betrugsmail (Bankdaten, Adresse, USt-ID) wird nicht erkannt | niedrig | hoch | Feste Regel, Stammdatenänderung immer zum Menschen. In den Tests 14 von 14 | teilweise: Regel ist umgehbar (Umschreibung, andere Sprache) |
| R-03 | Eine Mail schleust Anweisungen an das Modell ein | mittel | mittel | Mailtext als Daten behandelt, Erkennungsregel, Modell löst keine Aktion aus, Werte werden gegen den Mailtext geprüft, Ticket löst keine Zahlung aus | teilweise |
| R-04 | Eine AB mit Abweichung wird automatisch bestätigt | niedrig | hoch | Abgleich mit der Bestellung (Preis, Menge, Termin, Währung), Liefertreue, Blindbestätigung. Im Test 0 durchgewunkene ABs, die Währungslücke wurde am 11.11.2026 geschlossen | teilweise, solange Bestelldaten nicht aus dem ERP kommen |
| R-05 | Ausfall von Modell, Datenbank oder n8n | mittel | mittel | Wiederholungen, Fehlerausgang in die Prüfliste, Fehler-Workflow, Protokoll | teilweise: kein Alarm an Menschen |
| R-06 | Datenverlust | niedrig | mittel | Sicherung von Hand beschrieben (`07_betriebshandbuch.md`) | offen: keine automatische Sicherung |
| R-07 | Personenbezogene Daten werden ohne Löschfrist gespeichert | hoch | mittel | – | **offen**, siehe Datenschutz |
| R-08 | Gemeinsamer Login: kein Nachweis, wer was entschieden hat, kein Rollenkonzept | hoch | mittel | Persönliche Konten im Pilot | **offen** |
| R-09 | Die Genauigkeit wird überschätzt (Testmails sind synthetisch, Overfitting) | mittel | hoch | Prüfsätze mit vorab festgelegten Lösungen, Zahlen auf fremden Mails nennen, Pilot mit echten Mails | teilweise |
| R-10 | Das Team nimmt das Tool nicht an oder verlässt sich blind darauf | mittel | mittel | Mensch entscheidet, Entwürfe werden nie gesendet, Pilot im Schattenbetrieb, Erfolgskriterien vorab | offen |
| R-11 | Bestelldaten und Liefertreue sind veraltet, weil sie nicht aus dem ERP kommen | hoch | hoch | ERP-Anbindung oder regelmäßiger Export | **offen** |
| R-12 | Einzelne Person betreut alles, Wissen geht verloren | mittel | mittel | Dokumentation (dieser Ordner), Betriebshandbuch | teilweise |
| R-13 | Lizenzfragen bei kommerzieller Nutzung (n8n, Ollama, Modell) | unklar | mittel | Lizenzbedingungen prüfen | **offen** |

## Datenschutz

### Welche Daten werden verarbeitet

Lieferanten-Mails enthalten Namen und Mailadressen von Ansprechpartnern, Telefonnummern, Bestell-, Rechnungs- und Angebotsdaten, Preise und gelegentlich Bankdaten. Im Betrieb mit echten Mails kommen Daten der Mitarbeitenden hinzu (Bearbeiter, Zuständige).

### Was positiv ist

- **Lokale Verarbeitung:** Mails gehen nicht an einen Cloud-Dienst, es gibt keinen externen Auftragsverarbeiter für das Modell.
- Das Tool sendet keine Mails und bucht nichts.
- Der Zugriff auf die Arbeitsliste und die Formulare ist durch einen Login geschützt.

### Was offen ist

| Punkt | Stand |
|---|---|
| Rechtsgrundlage und Zweckbindung der Verarbeitung | nicht geklärt, mit Datenschutz zu klären |
| Verzeichnis der Verarbeitungstätigkeiten | nicht erstellt |
| **Löschfristen** | nicht definiert. Tickets, Prüffälle und Entwürfe bleiben unbegrenzt in der Datenbank |
| **Mailtexte in n8n:** Die Workflows speichern Ausführungen vollständig (`saveDataSuccessExecution: all`). Damit stehen Mailinhalte auch im Ausführungsprotokoll von n8n | zu ändern oder mit Löschfrist zu versehen |
| Mailtext in der Prüfliste (`review_queue`) | bleibt gespeichert, kein Löschlauf |
| Zugriff und Rollen | ein gemeinsamer Login, keine Protokollierung nach Person |
| Auskunft und Löschung auf Anfrage von Betroffenen | nicht vorgesehen |
| Mitbestimmung: Auswertung von Mails der Mitarbeitenden kann mitbestimmungspflichtig sein | zu prüfen |
| Sicherung (Backups) enthält dieselben Daten | Aufbewahrung festlegen |

### Vor einem Pilot mit echten Mails

1. Datenschutzbeauftragte und, falls vorhanden, den Betriebsrat einbeziehen.
2. Zweck, Rechtsgrundlage und Löschfristen schriftlich festlegen.
3. Ausführungsprotokoll in n8n und die Prüfliste mit Löschfrist versehen.
4. Persönliche Zugänge einführen.
5. Nur anonymisierte oder freigegebene Mails für Tests verwenden. Testsätze, die ins öffentliche Repository kommen, enthalten keine echten Daten.
