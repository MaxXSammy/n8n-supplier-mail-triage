# Fachkonzept: Ausbau um Bestellabwicklung und Antwortentwürfe

Fachliche Vorgaben aus der Praxis im Einkauf (Maximilian Schneider). Grundlage für die nächsten Ausbaustufen.

## Auftragsbestätigungen (AB)

Jede AB wird mit der Bestellung abgeglichen: Preis, Menge, Liefertermin.

| Abweichung | Beispiel | Wer handelt |
|---|---|---|
| Preis | Rohstoffzuschlag +4 % | bis 5 % und 500 € Disposition, darüber Einkauf (siehe Preiserhöhungen) |
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

## Preiserhöhungen

Preiserhöhungen kommen häufig vor und betreffen zwei Rollen: Die Disposition braucht den bestätigten Termin, der Einkäufer entscheidet über den Preis. Eine Mail kann deshalb mehrere Aufgaben für verschiedene Teams auslösen.

**Preiserhöhung in einer AB**

| Situation | Disposition | Einkäufer | Strategischer Einkauf |
|---|---|---|---|
| jede AB | Liefertermin prüfen bzw. übernehmen | – | – |
| Erhöhung bis 5 % und Mehrkosten bis 500 € je Bestellung | Preis selbst freigeben | Info ohne Aufgabe | – |
| Erhöhung über 5 % oder Mehrkosten über 500 € | – | Preiserhöhung prüfen, hohe Priorität | – |
| Erhöhung ab 10 % | wie oben | wie oben | Info |

**Angekündigte Preiserhöhung** („ab 01.01. erhöhen wir alle Preise um 6 %“, neuer Stückpreis): eigene Kategorie, immer an den zuständigen Einkäufer. Er bekommt alles für die Entscheidung mit:

- Erhöhung in Prozent und ab wann sie gilt. Nennt der Lieferant nur den neuen Stückpreis, wird der Prozentsatz gegen den bisherigen Preis gerechnet.
- Mehrkosten, hochgerechnet auf die offenen Bestellungen
- letzte Erhöhung des Lieferanten und Summe der Erhöhungen der letzten zwölf Monate
- Liefertreue des Lieferanten

Ab 10 % bekommt zusätzlich der strategische Einkauf bzw. Category Manager eine Info. Alle Schwellen stehen in der Tabelle `einstellungen`.

## Einkaufssteuerung: Jahreswirkung, Eskalation, Konditionen, Audit

Ausgangspunkt war ein Konzept mit festen Enterprise-Regeln. Vor der Umsetzung wurde jede Regel auf Fehlalarme und blinde Flecken geprüft. Die Tabelle zeigt, was übernommen und was geändert wurde.

| Vorschlag | Einwand | Umsetzung |
|---|---|---|
| Full-Year-Effekt (Jahresbedarf × Preisdifferenz) | richtig, aber kein Jahresbedarf in den Daten; „0 €“ bei fehlendem Bedarf wäre ein blinder Fleck; CHF verzerrt Euro-Schwellen | Tabelle `artikel_konditionen` mit Jahresbedarf. Fehlt er, steht „Jahresbedarf fehlt“ auf der Aufgabe. CHF über einen festen Kurs in `einstellungen` |
| Ab 5.000 € Jahreswirkung Status „Eskalation Geschäftsleitung“ | Fehlalarme: 3 % auf einen A-Artikel mit 200.000 € Volumen sind schon 6.000 €. Die Geschäftsleitung würde den Alarm bald ignorieren. Eskalation ist zudem kein Status, sondern eine Zuständigkeit. | gestuft als zusätzliche Aufgabe: ab 5.000 € Einkaufsleitung, ab 50.000 € zusätzlich Geschäftsleitung. Der Einkäufer bleibt zuständig. |
| Über 10 % bei Liefertreue unter 85 % eskalieren | gutes Signal, aber ein Thema fürs Lieferantenmanagement | Aufgabe für die Einkaufsleitung mit Hinweis „Alternativlieferant prüfen“ |
| Erhöhung für bereits bestätigte Bestellungen automatisch blockieren | Bestätigte Bestellung = Vertrag zum alten Preis, das stimmt. Aber das System kann im ERP nichts sperren, und eine Sperre kann einen Lieferstopp auslösen. Bei einer AB greift die Regel nicht: Sie ist ein Gegenangebot. | markieren statt sperren: „zum alten Preis bestätigt, alter Preis gilt, Rechnung prüfen“. Diese Bestellungen zählen nicht zu den Mehrkosten. |
| Heimliche Änderungen bei VPE und Mindestmenge | Jedes weitere Feld für das LLM erhöht die Fehlerquote. Aufrunden auf volle Einheiten ist oft in Ordnung. | ohne neue LLM-Felder: Abgleich der bestätigten Menge mit VPE und Mindestmenge aus den Stammdaten, Hinweis mit Mehrwert in Euro statt Alarm |
| Revisionssicherer Audit-Trail | „revisionssicher“ im Sinne der GoBD ist mit einer Tabelle nicht erreichbar. „Wer“ ist ein frei getippter Name, alle teilen ein Login. | Protokoll nur zum Anhängen (Trigger verbieten Ändern und Löschen), Hash-Kette mit Prüffunktion. Bezeichnet als manipulationserschwert. |
| Screenshot-Modus per Skript im Browser | Die echten Daten blieben im Quelltext. Freitext wie Mailtexte oder Entwürfe wird leicht übersehen: falsche Sicherheit. | anonyme Ansicht, die der Server erzeugt: Lieferant A, ID-001, Mitarbeiter 1, [Betrag]. Mailtexte, Betreffs und Entwürfe fallen ganz weg. |

**Eskalationsstufen nach Jahreswirkung**

| Jährliche Mehrkosten | Einkäufer | Einkaufsleitung | Geschäftsleitung |
|---|---|---|---|
| unter 5.000 € | Aufgabe | – | – |
| ab 5.000 € | Aufgabe | Aufgabe | – |
| ab 50.000 € | Aufgabe | Aufgabe | Aufgabe |
| über 10 % bei Liefertreue unter 85 % | Aufgabe | Aufgabe, Alternativlieferant prüfen | – |

Eine kleine Erhöhung in einer AB darf die Disposition nur freigeben, wenn auch die Jahreswirkung unter 5.000 € liegt.

**Entscheiden in der Arbeitsliste**

| Aufgabe | Aktionen | Wirkung |
|---|---|---|
| Preis freigeben, Preiserhöhung prüfen, Eskalation | Freigeben, Ablehnen | freigegebener AB-Preis wird neuer Preis in der Preishistorie |
| alle anderen | Erledigt | – |
| Sammelfreigabe „unkritische ABs“ | Freigeben | nur Preisfreigaben der Disposition ohne Warnhinweis: Angabe des Lieferanten passt zur Rechnung, Erhöhungen der letzten zwölf Monate zusammen höchstens 5 % |

Nach jeder Preisentscheidung entsteht ein Entwurf an den Lieferanten: „Preis bestätigt“ nach der letzten Freigabe im Vorgang, „Erhöhung nicht akzeptiert“ nach einer Ablehnung. Jeder Entwurf wird eine Aufgabe „Entwurf prüfen und senden“ für den zuständigen Einkäufer. Gesendet wird nie automatisch.

## Materialänderung und Abkündigung: Technik, QM, Disposition

Ändert ein Lieferant Werkstoff, Material oder Fertigung oder kann er einen Artikel nicht mehr liefern, ist das kein reines Preisthema. Der Einkauf darf das nicht allein entscheiden.

| Schritt | Wer | Was |
|---|---|---|
| Erkennen | Sprachmodell und feste Regel | Merker Technik, QM, Disposition, dazu alter und neuer Werkstoff. Eins von beiden reicht. „Werkstoff 42CrMo4“ in einem Angebot oder „gestiegene Materialkosten“ lösen nichts aus. |
| Einbinden | Einkäufer per Knopf | Aufgaben für Technik und QM, bei Abkündigung auch für die Disposition (Bestand, letzte Bestellung), dazu ein interner Entwurf an Technik und QM |
| Unterlagen anfordern | Einkäufer per Knopf | Entwurf an den Lieferanten: Datenblatt, Werkstoffzeugnis 3.1 nach EN 10204, Erstmuster mit Prüfbericht, Umstellungstermin. Bis zur Freigabe im bisherigen Werkstoff liefern. |
| Freigeben | Technik und QM | je eine Entscheidung in der Arbeitsliste |
| Preis freigeben | Einkauf | erst, wenn Technik und QM freigegeben haben, auch wenn sie noch nicht eingebunden sind. Das prüfen Seite, Code und Datenbank. |

Die Merker des Modells sind ein Vorschlag. Aufgaben für Technik und QM entstehen erst, wenn ein Mensch einbindet. So führt ein Fehlalarm des Modells nicht zu unnötigen Aufgaben in anderen Abteilungen. Die Handlungsempfehlung des Modells erscheint ausdrücklich als ungeprüfter Vorschlag.

Jede Entscheidung braucht einen Namen und landet im Audit-Protokoll. Die Sammelfreigabe ist bewusst eng gefasst: Massenfreigaben verleiten zum Durchwinken. Mehrere kleine Erhöhungen hintereinander („Salami-Taktik“) fallen über die Zwölf-Monats-Summe heraus und brauchen eine Einzelentscheidung.

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
