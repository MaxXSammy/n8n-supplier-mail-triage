# Auswertung der Klassifizierung

Lauf 20261030-170225 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 15 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **100 %** (15/15) | Kategorie des LLM stimmt mit Gold überein |
| Regel-Basislinie (Schlüsselwörter) | 87 % (13/15) | Vergleich ohne KI |
| Automatisierungsquote | 87 % (13/15) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **0** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 0 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (1/1) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 88 % (22/25) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| Ø Antwortzeit | 6.9 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | reklamation | lieferverzug | rechnung | sonstiges | (keine) |
|---|---|---|---|---|---|---|
| **angebot** | 3 | · | · | · | · | · |
| **reklamation** | · | 3 | · | · | · | · |
| **lieferverzug** | · | · | 3 | · | · | · |
| **rechnung** | · | · | · | 3 | · | · |
| **sonstiges** | · | · | · | · | 3 | · |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| 01_angebot_alpen | angebot | angebot | angebot | 0.9 | ticket | – | – |
| 02_angebot_rossi | angebot | angebot | angebot | 0.95 | ticket | – | betrag (erw. None, ist 298) |
| 03_angebot_kovotech_lieferzeit | angebot | angebot | angebot | 0.9 | ticket | – | – |
| 04_reklamation_brenner_8d | reklamation | reklamation | reklamation | 0.95 | ticket | beleg_fehlt:neuer_liefertermin | – |
| 05_reklamation_feldmann_mit_rechnung | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| 06_reklamation_swissturning_menge | reklamation | reklamation | reklamation | 0.9 | ticket | – | – |
| 07_lieferverzug_rheinwerk | lieferverzug | lieferverzug | lieferverzug | 0.95 | ticket | – | – |
| 08_lieferverzug_precimet_teillieferung | lieferverzug | lieferverzug | lieferverzug | 0.9 | review | pflichtfeld_fehlt:bestellnummer, beleg_fehlt:bestellnummer, beleg_fehlt:neuer_liefertermin | bestellnummer (erw. 4500018266, ist None) |
| 09_lieferverzug_alpen_kurz | lieferverzug | lieferverzug | lieferverzug | 0.9 | ticket | beleg_fehlt:neuer_liefertermin | – |
| 10_rechnung_brenner | rechnung | rechnung | rechnung | 0.95 | ticket | – | – |
| 11_rechnung_swissturning_mahnung | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| 12_rechnung_kovotech_gutschrift | rechnung | rechnung | rechnung | 0.9 | ticket | – | rechnungsnummer (erw. GS-2026-0091, ist KT-2026-3318) |
| 13_sonstiges_rossi_betriebsferien | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| 14_sonstiges_bankdaten_betrugsversuch | sonstiges | sonstiges | rechnung | 0.9 | review | bankdatenaenderung | – |
| 15_sonstiges_precimet_zertifikat | sonstiges | sonstiges | reklamation | 0.9 | ticket | – | – |
