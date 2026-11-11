# Projektsteckbrief: Supplier Mail Triage

**Stand:** 11.11.2026 · **Art des Dokuments:** nachträglich zusammengefasst

> Das Projekt begann am 30.10.2026 ohne schriftlichen Plan. Dieser Steckbrief fasst Ziel, Umfang und Rahmen so zusammen, wie sie sich im Verlauf ergeben haben. Das Fachkonzept (`docs/fachkonzept.md`) entstand am Abend des Starttages. Was nicht bekannt ist, steht als „offen".

## Kurzbeschreibung

| | |
|---|---|
| **Projekt** | Supplier Mail Triage (Repository `n8n-supplier-mail-triage`) |
| **Art** | Eigenprojekt als Portfolio und Machbarkeitsstudie, mit fachlichem Input aus der Einkaufspraxis |
| **Projektleitung und Entwicklung** | Maximilian Schneider |
| **Auftraggeber** | keiner. Der Anwendungsfall ist fiktiv (Hagemann Antriebstechnik GmbH, gleicher Rahmen wie im Projekt `procurement-rag-agent`) |
| **Start** | 30.10.2026 |
| **Stand** | Prototyp, getestet mit synthetischen Mails, noch kein Einsatz im echten Postfach |
| **Quellcode** | https://github.com/MaxXSammy/n8n-supplier-mail-triage |

## Ausgangslage und Problem

Im Sammelpostfach eines Einkaufs landen täglich Angebote, Auftragsbestätigungen (AB), Reklamationen, Rechnungen, Versandmeldungen und Werbung. Jede Mail wird gelesen, einem Team zugeordnet, und Nummern und Beträge werden abgeschrieben. Am meisten Zeit kosten Auftragsbestätigungen, weil sie gegen die Bestellung geprüft werden müssen. Manche Lieferanten bestätigen blind „alles wie gewünscht". Hinzu kommt das Risiko durch Betrugsmails mit „neuer Bankverbindung".

## Ziel

1. Eingehende Lieferanten-Mails automatisch einer von elf Kategorien zuordnen und an das zuständige Team bringen.
2. Auftragsbestätigungen mit der Bestellung abgleichen und Abweichungen sichtbar machen.
3. Betrugsverdächtige, unsichere und fehlerhafte Fälle immer an einen Menschen geben.
4. Dem Einkäufer Entscheidungshilfen liefern (Zusammenfassung, Warnungen, Antwortentwurf, Anfrage-Entwurf).
5. Alles lokal verarbeiten, ohne Cloud-Dienst.

## Umfang

**Im Umfang**
- Annahme von Mails per Schnittstelle (Webhook), Prüfung, Einordnung, Auslesen von Nummern, Beträgen und Terminen
- Prüfung im Code (Belege, Pflichtfelder, Betrugsregeln, Manipulationsschutz)
- AB-Abgleich mit Bestellung, Liefertreue, Absender, Blindbestätigung, Währung
- Arbeitsliste für den Einkauf mit Zusammenfassung, Warnungen, Erledigt-Knopf, Entwürfen
- Prüfliste (Review) für unsichere Fälle, Fehlerbehandlung
- Messung der Qualität mit Testsätzen

**Nicht im Umfang (Nicht-Ziele)**
- Keine automatischen Entscheidungen, keine Zahlungen, keine Buchungen
- **Kein automatischer Versand von Mails.** Entwürfe öffnen sich im Mailprogramm, ein Mensch sendet.
- Kein Ersatz für das ERP
- Keine Freigabe- oder Genehmigungsabläufe. Sie wurden am 10.11.2026 entwickelt und bewusst wieder entfernt (siehe Lessons Learned).
- Keine Spielelemente (Ränge, Serien) in der Oberfläche
- Kein Betrieb für das Handy, die Oberfläche ist für den Browser am Rechner gestaltet

## Erwarteter Nutzen

Weniger Handarbeit bei Routine-Mails und weniger übersehene Fehler (abweichende ABs, Betrugsversuche). Beides ist **bisher nicht im echten Betrieb gemessen**. Eine vorsichtige Rechnung steht im Whitepaper (120 bis 400 Stunden pro Jahr bei 1.000 Mails im Monat, vier Personen und 3 bis 10 Minuten je Mail, 20 % der Mails ohne Handarbeit).

## Beteiligte und Rollen

| Rolle | Besetzung |
|---|---|
| Projektleitung, Entwicklung, Test, Dokumentation | Maximilian Schneider |
| Fachlicher Input (Regeln aus der Praxis) | Maximilian Schneider, Einkaufserfahrung (Fachkonzept) |
| Künftige Anwender (Einkauf) | **offen**, bisher nicht beteiligt |
| Betrieb und IT | **offen** |
| Datenschutz | **offen** |

## Meilensteine (aus der Versionsgeschichte)

| Datum | Meilenstein |
|---|---|
| 30.10.2026 | Erster Stand: Triage-Workflow, Review, Fehlerbehandlung. Am Abend: AB-Prüfung, Arbeitsliste, Antwortentwürfe, Fachkonzept |
| 31.10.2026 | Dokumentation, Bilder, Demo-Material |
| 10.11.2026 | Ausbau um Freigaben und Oberflächen-Themen, am selben Tag zurückgenommen. Rückbau auf den Stand vom 31.10. |
| 11.11.2026 | Duplikatschutz, 11 Kategorien, Prüfsätze, Arbeitsliste nach Team, Währungsprüfung, neue Oberfläche, Projektdokumentation |

## Erfolgskriterien

- **Prototyp (erreicht, mit Einschränkungen):** gemessene Qualität auf mehreren Testsätzen mit vorab festgelegten Lösungen, Betrugsfälle immer beim Menschen, Ergebnisse offen dokumentiert.
- **Pilot (offen):** siehe `08_pilotplan.md`. Zum Beispiel: keine Mail ohne Prüfung an die falsche Stelle, höchstens 30 % der Mails in der Prüfung, Zeit je Mail messbar niedriger.

## Annahmen und Abhängigkeiten

- Annahme: durchschnittlich 5 Minuten je Mail im Einkauf (nicht gemessen, je nach Arbeitsweise 3 bis 10).
- Ein Rechner mit Grafikkarte (8 GB) reicht für das lokale Modell (etwa 6 Sekunden je Mail).
- Für den Echtbetrieb nötig: Postfach-Anschluss, Bestelldaten aus dem ERP, PDF-Anhänge, persönliche Logins. Alles **noch nicht gebaut**.

## Aufwand und Kosten

Der Aufwand wurde nicht erfasst. Laufende Kosten im Betrieb: Strom und Hardware, keine Lizenzgebühren für das Modell. Die Lizenzbedingungen von n8n, Ollama und dem Modell sind vor einer kommerziellen Nutzung zu prüfen (**offen**).

## Risiken

Siehe `05_risiken_und_datenschutz.md`. Die drei wichtigsten: keine Tests mit echten Mails, fehlende Anbindung an Postfach und ERP, gemeinsamer Login ohne Nachvollziehbarkeit.

## Status

Prototyp mit belegten Zahlen und ehrlich dokumentierten Grenzen. Nächster Schritt: Pilot im Schattenbetrieb (`08_pilotplan.md`).
