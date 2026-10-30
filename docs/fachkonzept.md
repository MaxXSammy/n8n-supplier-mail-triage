# Fachkonzept: Ausbau um Bestellabwicklung und Antwortentwürfe

Fachliche Vorgaben aus der Praxis im Einkauf (Maximilian Schneider). Grundlage für die nächsten Ausbaustufen.

## Auftragsbestätigungen (AB)

Jede AB wird mit der Bestellung abgeglichen: Preis, Menge, Liefertermin.

| Abweichung | Beispiel | Wer handelt |
|---|---|---|
| Preis | Rohstoffzuschlag +4 % | Einkauf: akzeptieren oder verhandeln |
| Liefertermin ungewiss | „voraussichtlich KW 50, ohne Gewähr“ | Disposition: nachfassen |
| Menge auf volle Paletten angepasst | 1.000 → 1.152 Stück | Einkauf: Mehrmenge akzeptieren? |
| Menge wegen falscher Stammdaten angepasst | Verpackungseinheit im System 40 statt 50 | Stammdatenpflege korrigieren |

**AB ohne Abweichung** läuft durch eine Prüfung der Lieferantenzuverlässigkeit:

| Situation | Schwelle Liefertreue | Ergebnis |
|---|---|---|
| Artikel AX, AY, BX, CX (hohe Prognosegenauigkeit, häufig bestellt, niedriger Bestand) | ≥ 90 % | automatisch bestätigt |
| übrige Artikel (Slow Mover, geringwertig, hoher Puffer) | ≥ 80 % | automatisch bestätigt |
| unter der Schwelle | – | manuelle Plausibilitätsprüfung, Einkäufer sichert den Termin beim Lieferanten ab |
| neuer Lieferant ohne Historie (meist nach erfolgreicher Trial Order) | – | immer manuell nachhaken und Kontakt aufnehmen |

**Signal für Blindbestätigung:** Die AB kommt auffällig schnell nach dem Bestellversand. Manche Lieferanten bestätigen ungeprüft „alles wie gewünscht“ und liefern dann, wann sie wollen. Eine sehr kurze Bearbeitungszeit führt deshalb zur manuellen Prüfung, auch wenn die Liefertreue reicht.

## Antwortentwürfe an Lieferanten

- Das System formuliert Antworten mit Platzhaltern (Ansprechpartner, Bestellnummer, Termin …), die aus den Stammdaten gefüllt werden.
- Der Mitarbeiter wählt den Ton: **förmlich** oder **locker**, jeweils **mit Nachdruck** oder **gelassen**.
- Jeder Entwurf geht an den zuständigen Mitarbeiter. Er prüft ihn und sendet ihn selbst, wenn er ihn für gut befindet. Das System verschickt nichts eigenständig.
- Auch Entwürfe laufen durch die Belegprüfung: keine Nummern oder Termine, die nicht aus Mail oder Stammdaten stammen.

## Weitere Mailtypen aus der Praxis

| Mailtyp | Gewünschte Reaktion |
|---|---|
| Angebot für neues Projekt oder Produkt mit falsch geschlüsselten Daten (Zahlendreher) | Abgleich mit der Anfrage, Abweichungen markieren |
| Lieferant fragt nach Projektstatus | Antwortentwurf: „Projekt XY, Angebotsschluss am …, wir melden uns“ |
| Terminanfrage vor Ort oder per Video | Erstvorstellung: Videocall anbieten, vor Ort ablehnen; persönlich erst bei konkretem Geschäft |
| Werbung, Newsletter nach Bestellungen in Onlineshops | abbestellen |
| Versandbenachrichtigung | prüfen, ob Frachtbrief (BOL), Transportschein oder Tracking-Nummer enthalten ist; sonst Einkäufer informieren und beim Lieferanten anfordern |
| Reklamation, Mängelrüge vom QM (z. B. Maßabweichung) | häufig, an Qualitätsmanagement |
| Zahlungsdifferenz („zu wenig überwiesen, warum?“) | Kreditorenbuchhaltung |
| Vertragsverlängerung, neuer Rahmenabruf | Einkauf |
| AGB-Änderung | Compliance |
| Bedarfsabfrage des Lieferanten | Einkauf / Disposition |
| „Warum beliefern Sie mich nicht mehr?“ | Einkauf |
| Eilfreigabe von Zeichnungen oder Mustern | Technik / QM, dringend |
| Akquise | niedrige Priorität |
