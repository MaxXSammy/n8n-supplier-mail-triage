# Projektdokumentation

Diese Papiere gehören zu einem Software-Projekt, auch zu einem kleinen. Sie zeigen, wie das Projekt gedacht, entschieden, getestet und betrieben wird.

> **Ehrlicher Hinweis zur Entstehung:** Das Projekt begann am 30.10.2026 ohne schriftlichen Plan. Die Dokumente 01 bis 09 wurden **am 11.11.2026 nachträglich** aus Fachkonzept, Code, Messläufen und Versionsgeschichte zusammengestellt. Sie sind als „nachträglich" gekennzeichnet. Was nicht bekannt ist, steht als „offen".

## Dokumentenübersicht

| Nr. | Dokument | Zweck | Leser | Stand |
|---|---|---|---|---|
| – | [Fachkonzept](../fachkonzept.md) | fachliche Regeln aus der Einkaufspraxis | Entwicklung, Fachbereich | 30.10.2026 |
| – | [README](../../README.md) | Überblick, Installation, Messergebnisse, Grenzen | alle | laufend |
| 01 | [Projektsteckbrief](01_projektsteckbrief.md) | Ziel, Umfang, Nicht-Ziele, Rollen, Meilensteine | Auftraggeber, Team | 11.11.2026, nachträglich |
| 02 | [Anforderungen](02_anforderungen.md) | was das Tool können soll und was davon erfüllt ist | Entwicklung, Fachbereich | 11.11.2026, nachträglich |
| 03 | [Architektur und Entscheidungen](03_architektur_und_entscheidungen.md) | Aufbau, Daten, Schnittstellen, begründete Entscheidungen | Entwicklung, IT | 11.11.2026, nachträglich |
| 04 | [Testkonzept und Testbericht](04_testkonzept_und_testbericht.md) | wie gemessen wird, Ergebnisse, Grenzen | Entwicklung, Fachbereich | 11.11.2026 |
| 05 | [Risiken und Datenschutz](05_risiken_und_datenschutz.md) | Risikoregister, Datenschutz, offene Punkte vor dem Pilot | Projektleitung, Datenschutz | 11.11.2026, nachträglich |
| 06 | [Benutzerhandbuch](06_benutzerhandbuch.md) | Bedienung der Arbeitsliste | Einkauf | 11.11.2026 |
| 07 | [Betriebshandbuch](07_betriebshandbuch.md) | Installation, Betrieb, Sicherung, Störungen | IT, Betrieb | 11.11.2026 |
| 08 | [Pilotplan](08_pilotplan.md) | Vorschlag für den Schattenbetrieb mit echten Mails | Einkaufsleitung, Projektleitung | 11.11.2026, Vorschlag |
| 09 | [Lessons Learned](09_lessons_learned.md) | was gut lief, was schiefging, was ich ändere | Projektleitung | 11.11.2026 |
| – | [Änderungsprotokoll](../../CHANGELOG.md) | Änderungen nach Datum | alle | laufend |

Das **Whitepaper** (Zusammenfassung für Einkaufsleitung und Interessierte) liegt als eigenes Dokument vor und gehört nicht in dieses Repository.

## Was in einem echten Unternehmen zusätzlich dazugehören würde

Für diesen Prototyp bewusst nicht erstellt, weil es ohne Auftraggeber und ohne Pilot nichts zu füllen gäbe:

| Dokument | Warum später |
|---|---|
| Wirtschaftlichkeitsrechnung (Business Case) | braucht gemessene Zeiten und Kosten aus dem Pilot |
| Berechtigungs- und Rollenkonzept | braucht persönliche Konten (Anforderung F-18) |
| Verzeichnis der Verarbeitungstätigkeiten, Datenschutzfolgenabschätzung | braucht Rechtsgrundlage und Löschfristen, mit dem Datenschutz zu erarbeiten |
| Betriebs- und Notfallkonzept (Monitoring, Rufbereitschaft, Wiederanlauf) | braucht einen Betrieb mit echten Mails |
| Schulungsunterlage und Abnahmeprotokoll | braucht Anwender und einen abgeschlossenen Pilot |
| Vertragliche Regelungen (Lizenz, Support) | braucht einen Auftraggeber |

## Pflege

Jedes Dokument nennt seinen Stand. Nach einer größeren Änderung werden Anforderungen (02), Entscheidungen (03) und das Änderungsprotokoll angepasst. Messergebnisse (04) werden nach jedem Lauf aktualisiert. Weitere Papiere entstehen erst, wenn es etwas Echtes zu dokumentieren gibt.
