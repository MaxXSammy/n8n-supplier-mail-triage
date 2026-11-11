# Pilotplan (Vorschlag)

**Stand:** 11.11.2026 · **Art des Dokuments:** Vorschlag. Der Pilot hat noch nicht begonnen, alle Zahlen und Zusagen sind offen und mit dem Einkauf abzustimmen.

## Ziel

Vier bis sechs Wochen im **Schattenbetrieb** zeigen, ob das Tool im echten Postfach des Einkaufs trägt, ohne dass sich für das Team etwas ändert. Das Team arbeitet wie bisher. Das Tool läuft mit, seine Einordnung wird mit der echten verglichen.

## Zeitplan

| Woche | Inhalt |
|---|---|
| 1 | Aufbau: Lesezugriff auf das Sammelpostfach, Export der offenen Bestellungen und Lieferantenstammdaten, persönliche Logins, Datenschutz geklärt (`05_risiken_und_datenschutz.md`) |
| 2 bis 5 | Schattenbetrieb. Wöchentlich 30 Minuten Auswertung mit den Pilotanwendern: Was war falsch, was fehlt? |
| 6 | Messung: Trefferquote, Anteil der Prüffälle, Zeit je Mail an einer Stichprobe mit Stoppuhr. Bericht und Entscheidung |

## Rollen

| Rolle | Aufgabe | Besetzung |
|---|---|---|
| Projektleitung und Entwicklung | Aufbau, Betrieb, Auswertung, Berichte | Maximilian Schneider |
| Fachliche Leitung Einkauf | Freigabe des Piloten, Entscheidung am Ende | offen |
| Pilotanwender (2 bis 3 Personen) | Arbeiten wie bisher, bewerten die Vorschläge, melden Fehler | offen |
| IT und Betrieb | Postfach-Zugang, Rechner mit Grafikkarte, Zugänge | offen |
| Datenschutz (und Betriebsrat, falls vorhanden) | Freigabe der Verarbeitung | offen |

## Voraussetzungen

- Lesezugriff auf das Sammelpostfach (nur lesen), kein Zugriff auf einzelne Postfächer
- Export der offenen Bestellungen und Lieferantenstammdaten (Liefertreue, ABC/XYZ-Klasse)
- 200 bis 300 anonymisierte Mails für die Auswertung, von denen ein Teil als Testsatz gesperrt bleibt
- Ein Rechner mit Grafikkarte (8 GB) und jemand, der das System betreut
- Persönliche Logins und eine Löschfrist für gespeicherte Mails

**Vor dem Pilot noch zu bauen:** Anschluss an das Postfach (IMAP, nur lesen), Einlesen der Bestelldaten, persönliche Benutzer (Anforderungen F-15, F-17, F-18). Aufwand: **nicht geschätzt**.

## Messung

- **Trefferquote:** Einordnung des Tools gegen die Einordnung der Pilotanwender, je Kategorie.
- **Prüffälle:** Anteil der Mails in der Prüfliste.
- **Zeit je Mail** mit und ohne Vorbereitung durch das Tool: Stichprobe von 20 bis 30 Mails je Person mit Stoppuhr, Median statt Mittelwert.
- **Fehler mit Folgen:** Mails, die ohne Prüfung an die falsche Stelle gingen, und Betrugs- oder Stammdatenmails, die keinen Menschen erreichten.

## Erfolgskriterien (vor dem Start festzulegen, hier ein Vorschlag)

1. Keine Mail wird ohne Prüfung an die falsche Stelle geleitet.
2. Alle Betrugs- und Stammdatenfälle erreichen einen Menschen.
3. Höchstens 30 % der Mails gehen in die Prüfung.
4. Die Zeit je Mail sinkt messbar, um mindestens 15 %.
5. Die Pilotanwender halten das Tool für nützlich (kurze Befragung am Ende).

## Abbruchkriterien

- Eine Betrugs- oder Stammdatenmail erreicht keinen Menschen.
- Datenschutz oder Betriebsrat ziehen die Freigabe zurück.
- Das Tool kostet das Team nachweislich mehr Zeit, als es spart.

## Entscheidung am Ende

| Ergebnis | Folge |
|---|---|
| Kriterien erfüllt | Weiterbetrieb, Anbindung ausbauen (Anhänge, ERP), Schulung |
| Teilweise erfüllt | Schwächen beheben, kurzer zweiter Durchlauf |
| Nicht erfüllt | Einstellen, Ergebnisse und Gründe dokumentieren |

## Kommunikation

Wöchentlicher Kurzbericht an die fachliche Leitung (Zahlen, Fehlerbilder, Entscheidungen). Am Ende ein Abschlussbericht mit Empfehlung.
