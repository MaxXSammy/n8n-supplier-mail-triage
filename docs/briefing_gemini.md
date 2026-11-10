# Briefing für eine kritische Bewertung: ProcurePulse

Du bist ein erfahrener Reviewer (Einkaufs-IT, Prozessautomatisierung, UX). Bewerte das folgende Projekt **kritisch und ohne Schonung**. Ich will Fehler, Lücken und Vorführ-Risiken finden, kein Lob. Trenne in deiner Antwort klar zwischen **belegten Fehlern**, **Risiken** und **Geschmacksfragen**. Wenn dir Informationen fehlen, sag das, statt zu raten.

## 1. Was das Projekt ist

ProcurePulse ist ein self-hosted Workflow auf **n8n** mit lokalem LLM (**Ollama, qwen2.5:7b**), **PostgreSQL** und Docker. Es verarbeitet Lieferanten-Mails eines mittelständischen Einkaufs: Das LLM erkennt die Kategorie und extrahiert Daten als JSON. Alles Weitere prüft **Code**, nicht das Modell (Belegprüfung, Betrugs- und Prompt-Injection-Schutz, Plausibilität, Preis- und Mengenabgleich mit der Bestellung). Danach entsteht ein Ticket mit Aufgaben für Disposition, Einkäufer, Einkaufsleitung, Geschäftsleitung, Technik und QM, oder die Mail geht in eine Review-Queue für einen Menschen. Kein Cloud-Dienst, keine Cloud-KI.

Workflows: `01_mail_triage`, `02_arbeitsliste` (Weboberfläche), `03_fehlerbehandlung`, `04_antwortentwurf`.

## 2. Fachlogik (Kern)

- Kategorien: Angebot, Auftragsbestätigung (AB), Reklamation, Lieferverzug, Rechnung, Preiserhöhung, Sonstiges, je mit Zielteam und Pflichtfeldern.
- **AB-Prüfung:** Abgleich mit der Bestellung, Liefertreue des Lieferanten (Schwelle 90 % bzw. 80 % je nach Artikelklasse), Blindbestätigung (AB unter 30 Minuten nach Bestellung), fremde Absender-Domain, neuer Lieferant.
- **Preiserhöhung:** Prozentsatz und Mehrkosten rechnet der Code. Bis 5 % und 500 € gibt die Disposition frei, darüber der Einkäufer, ab 10 % Info an den strategischen Einkauf.
- **Jahreswirkung (Full-Year-Effekt)** aus Jahresbedarf und Preisdifferenz. Eskalation ab 5.000 € an die Einkaufsleitung, ab 50.000 € an die Geschäftsleitung.
- **Materialänderung** (Werkstoff, Maß, Abkündigung): Technik, QM, Disposition werden eingebunden. Die Preisfreigabe ist gesperrt, bis Technik und QM freigegeben haben. Das prüfen Seite, Code und Datenbank.
- **Audit-Protokoll** mit Hash-Kette und Triggern gegen Ändern und Löschen.
- Entwürfe an Lieferanten entstehen aus Vorlagen, nicht aus dem Modell. **Es wird nie automatisch gesendet.**
- Gemessene Qualität (43 Test-Mails, Eigenmessung): Klassifikation 91 %, Regel-Basislinie ohne KI 86 %, Extraktion 99 %, AB-Entscheidung 86 % (18 von 21), Aufgabenverteilung 88 %, Abteilungs-Erkennung 100 %.

## 3. Die Oberfläche, wie sie JETZT ist

Ich habe zwischenzeitlich mehrere Redesign-Runden gebaut (Split-View, Tastatursteuerung, Dark Mode, Linear-Stil, Copilot) und **alles wieder zurückgenommen**. Der aktuelle Stand ist der ursprüngliche, auf `main`:

- Eine einzelne Seite „Arbeitsliste" (n8n-Webhook, Basic Auth), serverseitig als HTML erzeugt, **ohne externe Ressourcen** (kein CDN, keine Webfonts), weil sie vertrauliche Preise zeigt.
- Oben vier Kennzahlen-Kacheln (offene Eskalationen, offene Reviews, Auto-Quote 30 Tage, Jahreswirkung offen) und ein Balken „Savings YTD" (nur Cost Avoidance abgelehnter Erhöhungen, als vorläufig beschriftet), Streak (Tage ohne Rückstau), Procurement Rank.
- Reiter je Team, Sortierung nach Full-Year-Effekt oder Priorität.
- Jede Aufgabe ist eine **Karte**: Lieferant als Überschrift, Datengitter, farbig umrandete Warnhinweise mit Info-Symbol (zeigt die auslösende Regel mit den Werten), eine **System-Empfehlung** (regelbasiert, mit Begründung), der Vorschlag des Sprachmodells getrennt darunter als ungeprüft markiert, drei Reiter (Zusammenfassung, Original-Mail, Historie).
- Aktionen in der Karte: Freigeben, Ablehnen, Erledigt, Weiterleiten an Technik/QM/Disposition, „Empfehlung ausführen", Antwortentwurf. Jede Aktion ist ein POST an `/webhook/aufgabe`, der Server prüft Herkunft, Bearbeiter-Name und Passung zur Aufgabe.
- „Unkritische ABs freigeben" (Sammelfreigabe mit engen Kriterien, Server bestimmt die Menge, Rückfrage mit Anzahl und Summe).
- Vertretungsmodus (Übergabe-Ansicht) und Screenshot-Modus (Server anonymisiert Namen, Nummern, Beträge, bevor die Seite den Browser erreicht).
- Responsive-Verhalten: nicht gezielt auf Mobilgeräte ausgelegt.

## 4. Was ich selbst weiß, dass es schwach oder ungeprüft ist

- **Die Oberfläche sieht für mich nach „Standard-KI-Bastelei" aus**, nicht hochwertig. Das war der Auslöser der Redesign-Versuche.
- Eine **echte Freigabe oder Ablehnung** wurde in den letzten Runden nicht gegen die laufende Datenbank durchgespielt, nur gegen simulierte Antworten und Testdaten.
- Die Datenbank enthält viele **doppelte offene Aufgaben** aus wiederholten Test-Läufen (z. B. 28 identische Aufgaben eines Lieferanten). Das verfälscht die Vorführung.
- Das 7B-Modell macht bei Zahlen Fehler und erfindet gelegentlich Daten. Gegenmaßnahme ist die Belegprüfung im Code, nicht das Modell.
- Bekannte Grenzen laut README: eine Position je Bestellung, keine Mengenstaffeln, kein ERP (Stammdaten sind Testdaten), kein echtes Postfach (Mails kommen als JSON per Webhook), keine Anhänge, keine Benachrichtigungen, **alle Bearbeiter teilen sich ein Login** (Name nur aus einem Formularfeld), Audit-Protokoll nicht revisionssicher im GoBD-Sinn, **keine Freigabekette mit fester Reihenfolge** (jede Stufe entscheidet für sich, eine Ablehnung schließt andere Aufgaben desselben Tickets nicht), Cost Avoidance wird nicht mit späteren Rechnungen abgeglichen.
- Eine Akzeptanz-Metrik fehlt: Die Messwerte stammen aus 43 selbst geschriebenen Mails, nicht aus echten Mails.

## 5. Was ich von dir will

1. **Fachliche Fehler und Widersprüche** in den Regeln (Schwellen, Eskalationsstufen, Sperrlogik, Sammelfreigabe). Wo kann das System eine falsche Freigabe zulassen oder etwas Wichtiges blockieren?
2. **Sicherheits- und Missbrauchsrisiken** (gemeinsames Login, Herkunftsprüfung per Origin-Header, Prompt-Injection, Betrugs-Mails, Audit-Kette).
3. **Vorführbarkeit:** Was geht in einer 5- bis 10-Minuten-Demo vor einem Einkaufsleiter oder IT-Entscheider schief? Welche Fragen würden mich in die Enge treiben? Welche Zahlen sind angreifbar?
4. **Oberfläche:** Was wirkt unprofessionell oder verwirrend, und was würdest du konkret ändern? Bitte mit Begründung, nicht nur „moderner machen".
5. **Ehrlichkeit der Darstellung:** Wo behauptet das Projekt (README, Kennzahlen, Gamification wie Rank und Streak) mehr, als es belegt?
6. Am Ende: **die fünf wichtigsten Dinge**, die ich vor einer Vorführung ändern oder streichen sollte, nach Wirkung sortiert.

Wichtig: Wenn du etwas bemängelst, nenne bitte die konkrete Stelle oder Situation. Erfinde keine Funktionen, die oben nicht stehen.
