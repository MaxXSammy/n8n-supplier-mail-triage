# Testkonzept und Testbericht

**Stand:** 11.11.2026 · **Art des Dokuments:** Konzept nachträglich zusammengefasst, Ergebnisse aus den Läufen vom 11.11.2026. Alle Mails sind synthetisch.

## Ziel und Grundsatz

Die Tests sollen zeigen, wie gut das Tool Mails einordnet und prüft, und ehrlich machen, wo es versagt. Grundsatz: **Zu jeder Testmail steht die richtige Lösung vorher fest.** Nach einem Lauf wird nicht am Prompt oder an den Regeln nachgebessert, ohne dass für die nächste Messung frische Mails dazukommen. Wer an einem Satz nachbessert, darf ihn nicht mehr als unabhängig ausgeben.

## Teststufen

| Stufe | Was | Womit |
|---|---|---|
| Robustheit und Sicherheit | zwölf Angriffe und Grenzfälle mit erwartetem Ergebnis (kaputte Eingaben, SQL-Injection, HTML im Betreff, Prompt-Injection, Bankdaten ohne Schlüsselwörter, dieselbe Mail fünfmal) | `scripts/robustheit.py` |
| Klassifikation und Auslesen | Kategorie, Nummern, Beträge, Termine gegen die Lösung | `scripts/evaluate.py` (auch `--set pruefset4`) |
| AB-Prüfung | Entscheidung (automatisch bestätigt, manuell prüfen, Abweichung, Prüfliste) und Gründe | `scripts/evaluate.py` |
| Statische Prüfungen | JSON gültig, Schema im Workflow gleich Schema-Datei, Skripte übersetzbar, Docker-Konfiguration | CI (GitHub Actions) |
| Bedienung der Arbeitsliste | Filter, Suche, Erledigt, Formulare, Weiterleitung | von Hand und mit Skriptaufrufen, nicht automatisiert |

## Testdaten

| Satz | Ordner | Mails | Herkunft | Als unabhängig zu werten |
|---|---|---|---|---|
| Entwicklungsmails | `mails/`, `eval/gold.json` | 34 | selbst geschrieben, daran wurde entwickelt | nein |
| Prüfsatz 1 | `pruefset/` | 31 | selbst geschrieben, neue Lieferanten und Fälle | nein, nach den Korrekturregeln |
| Prüfsatz 2 | `pruefset2/` | 27 | selbst geschrieben, fünf neue Kategorien und Kontrollmails | nein, nach der Korrekturregel |
| Prüfsatz 3 | `pruefset3/` | 10 | von einem anderen KI-Modell geschrieben, absichtliche Fallen | ja |
| Prüfsatz 4 | `pruefset4/` | 99 | von einem fremden Modell erzeugt, 25 Mails als mehrdeutig markiert | ja |

Die Entwicklungsmails und die Prüfsätze 1 und 2 wurden mit Unterstützung von Claude Code geschrieben, die Mails der Prüfsätze 3 und 4 stammen von einem anderen KI-Modell. Die Lösungen aller Prüfsätze wurden festgelegt, bevor das Tool die Mails sah, ebenfalls mit Unterstützung von Claude Code und nicht durch unabhängige Fachleute. Sie sind in Git vor dem Lauf eingecheckt.

## Ergebnisse (Läufe vom 11.11.2026)

| Satz | Mails | Kategorie richtig | Hinweis |
|---|---|---|---|
| Entwicklungsmails | 34 | 94 % (32) | AB-Entscheidung 19 von 19 |
| Prüfsatz 1 | 31 | 87 % (27) | |
| Prüfsatz 2 | 27 | 100 % (27) | |
| Prüfsatz 3 | 10 | 60 % (6) | Fallen: Kaltakquise als Angebot, interne Anforderung als AB, Sammelmail, Mischmail |
| Prüfsatz 4 | 99 | 78 % (77) | ohne mehrdeutige Mails 81 %, nur Lieferanten-Mails 86 % |

**Prüfsatz 4 im Detail:** Reklamation 4 von 4, Werbung 10 von 10, Stammdatenänderung 3 von 3, Auftragsbestätigung 18 von 20, Lieferverzug 8 von 9, Compliance 4 von 5, Lieferavis 4 von 5, Rechnung 8 von 10, Angebot 3 von 4, Preisänderung 2 von 4, Sonstiges 13 von 25. Betrugs- und Stammdatenfälle: alle beim Menschen (14 von 14 über alle Sätze). AB-Entscheidung 12 von 13, keine AB fälschlich ohne Prüfung. Ohne die KI, nur mit Schlüsselwörtern: 59 %.

Die Rohdaten stehen in `eval/ergebnisse*.json`, die Auswertung in `eval/ergebnisse*.md`.

## Bewertung

- Die Lieferanten-Kategorien und die Sicherheitsfälle funktionieren in den Tests. Die Zahl auf eigenen Mails (94 bis 100 %) ist kein Beleg, die auf fremden (60 bis 78 %) ist die ehrliche.
- Schwach: Preisänderung, das Sammelbecken Sonstiges (interne Mails, Systemmeldungen) und Mischmails.
- Zwischen zwei Läufen mit gleichem Code streuen die Ergebnisse um ein bis zwei Mails.

## Bekannte Fehlerbilder

Kaltakquise mit Wörtern wie „Angebot" wird als Angebot eingeordnet, interne Bedarfsanforderungen mit Bestellnummer als Auftragsbestätigung, eine AB mit Teilmenge teils als Lieferverzug, Datumsformate wie `10/12/2026` und „18 December 2026" werden verworfen (Termin geht verloren, Fehlalarm zur sicheren Seite). Die Fehler sind gemessen und bewusst nicht an den Testmails wegoptimiert.

## Nicht getestet

Echte Mails und echte Postfächer, Last (viele Mails gleichzeitig über längere Zeit), Anhänge, Bedienung durch fremde Anwender, Zugänglichkeit, andere Browser als Chrome und Edge, ein extern durchgeführter Sicherheitstest.

## Wiederholen

```bash
python scripts/evaluate.py --set pruefset4     # einen Satz messen, Ergebnis in eval/
python scripts/robustheit.py                   # Angriffe und Grenzfälle
python scripts/check_schema_sync.py            # Schema im Workflow gleich Schema-Datei
```

`evaluate.py` räumt die Test-Tickets nach dem Lauf selbst wieder weg (`--behalten` hebt sie auf). Der Lauf braucht ein laufendes n8n und Ollama und dauert für 99 Mails etwa 10 Minuten.

## Kriterien für den Pilot

Siehe `08_pilotplan.md`. Dort steht, was an echten Mails gemessen wird und ab wann das Tool als bestanden gilt.
