# Auswertung der Klassifizierung

Lauf 20261111-084816 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 99 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **78 %** (77/99) | Kategorie des LLM stimmt mit Gold überein |
| davon ohne mehrdeutige Mails | 81 % (60/74) | Mails mit eindeutiger Lösung, mehrdeutige sind im Gold markiert |
| Regel-Basislinie (Schlüsselwörter) | 59 % (58/99) | Vergleich ohne KI |
| Automatisierungsquote | 75 % (74/99) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **11** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 11 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (3/3) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 100 % (31/31) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| AB-Entscheidung richtig | **85 %** (11/13) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |
| AB-Gründe exakt richtig | 85 % (11/13) | Art der Abweichung bzw. Prüfgrund stimmt |
| AB fälschlich durchgewunken | **1** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |
| Ø Antwortzeit | 5.8 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | auftragsbestaetigung | reklamation | lieferverzug | rechnung | lieferavis | preisaenderung | stammdatenaenderung | compliance | werbung | sonstiges | (keine) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **angebot** | 3 | 1 | · | · | · | · | · | · | · | · | · | · |
| **auftragsbestaetigung** | · | 18 | · | 1 | · | · | · | · | · | · | 1 | · |
| **reklamation** | · | · | 4 | · | · | · | · | · | · | · | · | · |
| **lieferverzug** | · | 1 | · | 8 | · | · | · | · | · | · | · | · |
| **rechnung** | · | · | 1 | · | 8 | 1 | · | · | · | · | · | · |
| **lieferavis** | · | 1 | · | · | · | 4 | · | · | · | · | · | · |
| **preisaenderung** | · | · | · | · | · | · | 2 | 1 | · | · | 1 | · |
| **stammdatenaenderung** | · | · | · | · | · | · | · | 3 | · | · | · | · |
| **compliance** | · | · | · | · | · | · | · | · | 4 | · | 1 | · |
| **werbung** | · | · | · | · | · | · | · | · | · | 10 | · | · |
| **sonstiges** | 4 | 2 | · | 1 | 1 | · | · | 4 | · | · | 13 | · |

## Auftragsbestätigungen

| Mail | erwartet | Ergebnis | erwartete Gründe | Gründe |
|---|---|---|---|---|
| s005 | abweichung | automatisch_bestaetigt ✗ | waehrung | – |
| s007 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s012 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s014 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s016 | manuell_pruefen | manuell_pruefen | liefertreue_unter_schwelle | liefertreue_unter_schwelle |
| s018 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s020 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s091 | abweichung | abweichung | termin_fehlt | termin_fehlt |
| s092 | abweichung | review ✗ | termin_fehlt | – |
| s093 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s094 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s095 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| s100 | automatisch_bestaetigt | automatisch_bestaetigt | – | – |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| s001 | auftragsbestaetigung | auftragsbestaetigung | lieferverzug | 0.95 | ticket | beleg_fehlt:menge | – |
| s002 | lieferavis | lieferavis | lieferavis | 1 | ticket | – | – |
| s003 | lieferverzug | lieferverzug | sonstiges | 0.95 | ticket | – | – |
| s004 | reklamation | reklamation | reklamation | 1 | ticket | – | – |
| s005 | auftragsbestaetigung | auftragsbestaetigung | lieferverzug | 0.95 | ticket | – | – |
| s006 | lieferverzug | lieferverzug | sonstiges | 0.95 | ticket | – | – |
| s007 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| s008 | lieferverzug | auftragsbestaetigung ✗ | sonstiges | 0.95 | ticket | – | – |
| s009 | lieferavis | lieferavis | sonstiges | 1 | ticket | – | – |
| s010 | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| s011 | lieferavis | auftragsbestaetigung ✗ | sonstiges | 0.95 | ticket | – | – |
| s012 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| s013 | lieferverzug | lieferverzug | sonstiges | 0.95 | ticket | – | – |
| s014 | auftragsbestaetigung | auftragsbestaetigung | angebot | 0.95 | ticket | – | – |
| s015 | lieferavis | lieferavis | sonstiges | 1 | ticket | – | – |
| s016 | auftragsbestaetigung | auftragsbestaetigung | angebot | 0.95 | ticket | – | – |
| s017 | auftragsbestaetigung | lieferverzug ✗ | lieferverzug | 0.9 | ticket | – | – |
| s018 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | ticket | – | – |
| s019 | lieferverzug | lieferverzug | sonstiges | 0.95 | ticket | – | – |
| s020 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| s021 | sonstiges | auftragsbestaetigung ✗ | sonstiges | 0.95 | review | pflichtfeld_fehlt:bestellnummer | – |
| s022 | sonstiges | sonstiges | sonstiges | 0.8 | ticket | – | – |
| s023 | sonstiges | sonstiges | sonstiges | 0.8 | ticket | – | – |
| s024 | sonstiges | angebot ✗ | sonstiges | 0.95 | ticket | beleg_fehlt:bestellnummer, beleg_fehlt:rechnungsnummer, beleg_fehlt:angebotsnummer | – |
| s025 | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| s026 | sonstiges | stammdatenaenderung ✗ | sonstiges | 1 | review | stammdatenaenderung_pruefen | – |
| s027 | sonstiges | angebot ✗ | sonstiges | 0.9 | ticket | – | – |
| s028 | sonstiges | angebot ✗ | sonstiges | 0.9 | review | kategorie_unplausibel | – |
| s029 | sonstiges | sonstiges | sonstiges | 0.8 | ticket | – | – |
| s030 | sonstiges | stammdatenaenderung ✗ | sonstiges | 0.9 | review | stammdatenaenderung_pruefen | – |
| s031 | angebot | angebot | angebot | 0.95 | ticket | – | – |
| s032 | preisaenderung | preisaenderung | compliance | 0.95 | ticket | – | – |
| s033 | preisaenderung | stammdatenaenderung ✗ | preisaenderung | 0.95 | review | stammdatenaenderung_pruefen | – |
| s034 | sonstiges | sonstiges | sonstiges | 0.8 | ticket | – | – |
| s035 | angebot | angebot | angebot | 0.95 | ticket | – | – |
| s036 | preisaenderung | preisaenderung | angebot | 0.95 | ticket | – | – |
| s037 | preisaenderung | sonstiges ✗ | preisaenderung | 0.6 | review | konfidenz_niedrig | – |
| s038 | angebot | angebot | angebot | 0.95 | ticket | – | – |
| s039 | lieferverzug | lieferverzug | reklamation | 0.8 | review | pflichtfeld_fehlt:bestellnummer | – |
| s040 | compliance | sonstiges ✗ | sonstiges | 0.8 | ticket | – | – |
| s041 | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| s042 | rechnung | rechnung | angebot | 0.95 | review | pflichtfeld_fehlt:rechnungsnummer, pflichtfeld_fehlt:betrag | – |
| s043 | rechnung | rechnung | rechnung | 0.95 | ticket | – | – |
| s044 | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| s045 | rechnung | lieferavis ✗ | rechnung | 0.9 | ticket | beleg_fehlt:rechnungsnummer | – |
| s046 | rechnung | rechnung | rechnung | 0.95 | review | pflichtfeld_fehlt:rechnungsnummer, pflichtfeld_fehlt:betrag | – |
| s047 | rechnung | rechnung | rechnung | 1 | review | pflichtfeld_fehlt:betrag | – |
| s048 | rechnung | reklamation ✗ | rechnung | 0.95 | review | pflichtfeld_fehlt:bestellnummer|artikel | – |
| s049 | rechnung | rechnung | rechnung | 0.95 | review | pflichtfeld_fehlt:betrag | – |
| s050 | rechnung | rechnung | rechnung | 0.95 | review | pflichtfeld_fehlt:betrag | – |
| s051 | sonstiges | stammdatenaenderung ✗ | sonstiges | 0.8 | review | stammdatenaenderung_pruefen | – |
| s052 | compliance | compliance | sonstiges | 0.9 | ticket | – | – |
| s053 | stammdatenaenderung | stammdatenaenderung | stammdatenaenderung | 1 | review | stammdatenaenderung_pruefen, bankdatenaenderung | – |
| s054 | sonstiges | sonstiges | sonstiges | 1 | ticket | – | – |
| s055 | compliance | compliance | compliance | 0.9 | ticket | – | – |
| s056 | sonstiges | sonstiges | auftragsbestaetigung | 0.6 | review | konfidenz_niedrig | – |
| s057 | stammdatenaenderung | stammdatenaenderung | rechnung | 1 | review | stammdatenaenderung_pruefen | – |
| s058 | compliance | compliance | compliance | 0.95 | ticket | – | – |
| s060 | compliance | compliance | compliance | 0.9 | ticket | – | – |
| s061 | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| s062 | werbung | werbung | werbung | 0.9 | ticket | – | – |
| s063 | sonstiges | lieferverzug ✗ | auftragsbestaetigung | 0.8 | ticket | – | – |
| s064 | sonstiges | sonstiges | sonstiges | 0.6 | review | konfidenz_niedrig | – |
| s065 | sonstiges | sonstiges | sonstiges | 0.8 | ticket | – | – |
| s066 | sonstiges | sonstiges | sonstiges | 1 | ticket | – | – |
| s067 | sonstiges | auftragsbestaetigung ✗ | sonstiges | 0.95 | ticket | – | – |
| s068 | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| s069 | sonstiges | rechnung ✗ | sonstiges | 0.9 | review | pflichtfeld_fehlt:betrag | – |
| s070 | sonstiges | stammdatenaenderung ✗ | sonstiges | 0.9 | review | stammdatenaenderung_pruefen | – |
| s071 | werbung | werbung | sonstiges | 0.9 | ticket | – | – |
| s072 | werbung | werbung | werbung | 0.9 | ticket | – | – |
| s073 | werbung | werbung | sonstiges | 0.9 | ticket | – | – |
| s074 | werbung | werbung | werbung | 0.9 | ticket | – | – |
| s075 | werbung | werbung | sonstiges | 0.9 | ticket | – | – |
| s076 | werbung | werbung | sonstiges | 0.9 | ticket | – | – |
| s077 | werbung | werbung | angebot | 0.9 | ticket | – | – |
| s078 | werbung | werbung | sonstiges | 0.9 | ticket | – | – |
| s079 | werbung | werbung | auftragsbestaetigung | 0.9 | ticket | – | – |
| s080 | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| s081 | lieferverzug | lieferverzug | auftragsbestaetigung | 0.9 | review | pflichtfeld_fehlt:bestellnummer, liefertermin_format, beleg_fehlt:bestellnummer | – |
| s082 | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| s083 | stammdatenaenderung | stammdatenaenderung | stammdatenaenderung | 0.95 | review | stammdatenaenderung_pruefen, bankdatenaenderung, beleg_fehlt:bestellnummer | – |
| s084 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | beleg_fehlt:rechnungsnummer, beleg_fehlt:angebotsnummer | – |
| s085 | angebot | auftragsbestaetigung ✗ | angebot | 0.95 | ticket | – | – |
| s086 | lieferverzug | lieferverzug | lieferverzug | 0.95 | ticket | – | – |
| s087 | sonstiges | angebot ✗ | angebot | 0.9 | review | kategorie_unplausibel | – |
| s088 | reklamation | reklamation | reklamation | 0.9 | ticket | – | – |
| s089 | lieferverzug | lieferverzug | rechnung | 0.9 | ticket | – | – |
| s090 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | review | pflichtfeld_fehlt:bestellnummer, liefertermin_format, beleg_fehlt:bestellnummer | – |
| s091 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | ticket | – | – |
| s092 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | review | pflichtfeld_fehlt:bestellnummer, beleg_fehlt:bestellnummer | – |
| s093 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | ticket | – | – |
| s094 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | ticket | – | – |
| s095 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | ticket | – | – |
| s096 | auftragsbestaetigung | sonstiges ✗ | sonstiges | 0.8 | ticket | – | – |
| s097 | lieferavis | lieferavis | sonstiges | 0.95 | ticket | – | – |
| s098 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| s099 | auftragsbestaetigung | auftragsbestaetigung | sonstiges | 0.95 | ticket | – | – |
| s100 | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
