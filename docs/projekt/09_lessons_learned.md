# Lessons Learned (Rückblick)

**Stand:** 11.11.2026 · **Art des Dokuments:** Rückblick auf die ersten zwölf Tage (30.10. bis 11.11.2026). Alles hier ist so passiert und aus den Commits und Messläufen belegbar.

## Was gut lief

- **Prüfen statt vertrauen.** Die Belegprüfung (jeder Wert muss im Mailtext stehen) fing erfundene Termine und eine verkürzte Bestellnummer ab. Die Sicherheitsfälle (Bankdaten, Stammdaten) erreichten in allen Tests einen Menschen.
- **Fachliche Regeln aus der Praxis** (Liefertreue-Schwellen, Blindbestätigung) machten die AB-Prüfung glaubwürdig, ohne Modell.
- **Ehrliche Messung.** Prüfsätze mit vorab festgelegten Lösungen zeigten, dass 100 % auf eigenen Mails nur 78 % auf fremden bedeuten.
- **Zurücknehmen können.** Die Rückkehr zum Kern am 10.11.2026 war richtig.

## Was schiefging

| Was | Wie es auffiel | Folge |
|---|---|---|
| **Zu viel gleichzeitig (10.11.2026):** Freigaben, Preisfreigaben, Ränge und mehrere Oberflächen-Stile in einem Tag | Das Tool sollte Arbeit abnehmen und hatte stattdessen Verfahren und Bedienung hinzugefügt | Alles zurückgenommen (PR 8), Kern wiederhergestellt |
| **Messung am Entwicklungssatz** | 100 % auf selbst geschriebenen Mails, 60 bis 78 % auf fremden | Prüfsätze 1 bis 4, Zahlen auf fremden Mails als maßgeblich |
| **Prompt angepasst gegen einen Fehler** | Genauigkeit sank von 97 auf 94 % und eine zweite AB kippte | Anpassung zurückgenommen, feste Regel im Code für den eindeutigen Fall |
| **Neue Kategorien kosteten alte Treffer** | Erst die Messung auf allen Sätzen zeigte, dass ABs mit Preiserhöhung als „Preisänderung" eingeordnet wurden | Korrekturregel, danach alle Sätze neu gemessen |
| **Auswertung schrieb in die echte Datenbank** | Dieselben Test-Tickets erschienen mehrfach auf der Arbeitsliste | Auswertung räumt nach dem Lauf auf, Duplikate auch über den Inhalt erkannt |
| **Währung wurde nicht geprüft** | Im Test ging eine AB mit EUR statt CHF durch | Währung wird gegen die Bestellung geprüft |
| **Erledigt-Knopf wäre im Browser nie gegangen** | Herkunftsprüfung getestet nur mit curl, im Browser ist die Herkunft wegen der Sandbox `null` | Token je Aufgabe statt Herkunftsprüfung |
| **Formulare verlangten Ticket-ID und Name von Hand** | Rückmeldung bei der Bedienung | Felder werden vorbefüllt, danach zurück zur Liste |
| **Weiterleitung mit relativer Adresse** | n8n setzte „https://" davor | volle Adresse |
| **Oberfläche wirkte „billig"** | Rückmeldung nach dem ersten Entwurf | Neugestaltung mit größerem Maßstab, Seitenleiste, klaren Zeilen |

## Was ich künftig anders mache

1. **Erst messen, dann bauen.** Jede Änderung an Prompt oder Regeln wird auf allen Testsätzen gemessen, bevor sie bleibt.
2. **Testsätze mit vorab festgelegter Lösung** und ein gesperrter Teil, den man nicht zum Nachbessern benutzt.
3. **Sicherheitsfunktionen in der echten Umgebung testen**, nicht nur mit einem Skript (Beispiel: Erledigt-Knopf).
4. **Den Kern schützen.** Neue Funktionen nur, wenn sie Arbeit abnehmen. Freigaben, Spielelemente und Oberflächen-Experimente kommen nicht vor dem Pilot.
5. **Fehler und Grenzen offen schreiben** (README, Messbericht, Spickzettel). Das ist glaubwürdiger als glatte Zahlen.
6. **Vorab planen.** Dieses Projekt hatte zu Beginn keinen schriftlichen Plan. Ein Steckbrief, Anforderungen und ein Risikoregister am Anfang hätten den Umweg vom 10.11.2026 wahrscheinlich verkürzt. Die Projektdokumentation wurde deshalb nachgeholt.

## Offene Fragen

- Wie gut trägt das Tool in einem echten Postfach?
- Wie viel Zeit spart die Vorsortierung der übrigen 80 % der Mails wirklich?
- Genügt ein 7B-Modell, oder bringt ein größeres Modell einen spürbaren Gewinn? Ein Vergleich wurde bewusst nicht durchgeführt.
