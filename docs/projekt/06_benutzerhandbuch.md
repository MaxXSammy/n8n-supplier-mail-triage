# Benutzerhandbuch für den Einkauf

**Stand:** 11.11.2026 · **Art des Dokuments:** nachträglich erstellt. Es beschreibt den Prototyp, so wie er heute läuft.

## Wofür das Tool da ist

Mail-Triage sortiert eingehende Lieferanten-Mails vor, prüft Auftragsbestätigungen gegen die Bestellung und legt Hinweise und Entwürfe bereit. **Es entscheidet nichts und sendet keine Mail.** Sie prüfen und entscheiden.

## Öffnen

Adresse: `http://localhost:5678/webhook/arbeitsliste`. Anmeldung mit dem Zugang, den der Betreiber vergeben hat (bisher ein gemeinsamer Zugang für alle).

## Die Arbeitsliste

- **Links die Seitenleiste:** „Alle Aufgaben", „Zur Prüfung" und je ein Eintrag pro Team mit der Zahl offener Aufgaben. Ein Klick filtert die Liste. Darunter der Link „Messwerte".
- **Oben drei Kacheln:** offene Aufgaben, Mails zur Prüfung, automatisch erledigte Mails der letzten 7 Tage. Ein Klick auf die ersten beiden filtert.
- **Suche:** oben rechts, mit der Taste `/` erreichbar. Gesucht wird in Lieferant, Betreff, Zusammenfassung, Bestellnummer und Artikel. `Esc` leert die Suche.
- **Zeilen:** Links ein runder Avatar mit den Initialen des Lieferanten, daneben der Lieferant, der Betreff, eine Zusammenfassung und darunter Kategorie und Warnungen. Rechts die Uhrzeit. Ein Klick klappt die Zeile auf.

### Farben und Hinweise

| Darstellung | Bedeutung |
|---|---|
| Roter Rand, rotes Warnzeichen | Betrugsverdacht oder Sicherheitsproblem (geänderte Bankdaten, abweichende Absender-Domain). Immer sorgfältig prüfen. |
| Rote Hinweise wie „Preis 0,92 → 0,97 CHF (+5,4 %)" | Verschlechterung gegenüber der Bestellung (höherer Preis, späterer Termin, weniger Menge, andere Währung) |
| Grüne Hinweise | Verbesserung (niedrigerer Preis) |
| Orange Hinweise | Prüfen, kein Verstoß (neuer Lieferant, Liefertreue unter der Schwelle, Termin unsicher) |
| Graue Hinweise | System-Hinweise, zum Beispiel „Einzelpreis nicht im Mailtext belegt" |
| Gelb hinterlegte Zeile unter „Zur Prüfung" | Das System war unsicher, ein Mensch entscheidet, wohin die Mail gehört |

## Typische Abläufe

**Auftragsbestätigung mit Abweichung**
1. Zeile aufklappen, Abweichungen lesen.
2. „Antwortentwurf erstellen" klicken. Das Formular öffnet sich mit eingetragener Ticket-ID, dem zuständigen Einkäufer als Bearbeiter und den Standardwerten (förmlich, gelassen). Anpassen, falls nötig, dann „Entwurf erstellen".
3. Sie landen wieder in der Liste. Unter der Aufgabe steht der Entwurf („Entwurf prüfen"). „In Mailprogramm öffnen" übernimmt Betreff und Text in Ihr Mailprogramm. **Prüfen Sie Platzhalter in eckigen Klammern wie [Datum], bevor Sie senden.**
4. Nach dem Senden „Erledigt" klicken.

**Angebot oder Preisänderung:** „Angebot anfordern" zeigt einen vorbereiteten Anfrage-Entwurf mit den Punkten, die für den Angebotsvergleich nötig sind (Stückpreis, Mindestmenge, Lieferzeit, Zahlungsziel, Skonto, Preisgleitklausel, Zertifikate, CO2, Reklamationsquote, Liefertreue). Er öffnet sich im Mailprogramm. Frist und Name tragen Sie selbst ein.

**Zur Prüfung:** Zeile aufklappen, „Mailtext anzeigen", Vorschlag des Modells lesen. „Review abschließen" öffnet ein Formular mit eingetragener Review-ID. Wählen Sie die richtige Kategorie oder „verwerfen", tragen Sie Ihren Namen ein und speichern Sie. Danach legt das System das Ticket für das richtige Team an.

**Erledigt:** Der Knopf steht in der aufgeklappten Zeile und erscheint in der Liste beim Darüberfahren. Nach dem Klick bleibt der gewählte Filter erhalten.

## Wichtig zu wissen

- Die Zusammenfassung stammt von einem Sprachmodell und **kann falsch sein**. Entscheidend ist der Mailtext.
- Ein Hinweis „nicht im Mailtext belegt" heißt: Der Wert wurde verworfen, weil er in der Mail nicht steht.
- Interne Mails und Systemmeldungen werden nur zur Hälfte richtig eingeordnet.
- Das Tool liest bisher keine PDF-Anhänge.
- Bei Auffälligkeiten wenden Sie sich an den Betreiber (`07_betriebshandbuch.md`).

## Kleines Glossar

| Begriff | Bedeutung |
|---|---|
| AB | Auftragsbestätigung des Lieferanten |
| RFQ | Anfrage, ein Angebot einzuholen (Request for Quotation) |
| Review, Prüfliste | Mails, bei denen ein Mensch entscheidet |
| Liefertreue | Anteil termingerechter Lieferungen eines Lieferanten |
| AX, AY, BX, CX | Artikelklassen mit hohem Planungsbedarf, dort gilt die höhere Schwelle |
| Blindbestätigung | AB, die so schnell kommt, dass sie kaum geprüft sein kann |
| Ticket | eine eingeordnete Mail als Aufgabe für ein Team |
