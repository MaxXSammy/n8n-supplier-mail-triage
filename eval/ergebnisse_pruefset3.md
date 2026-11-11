# Auswertung der Klassifizierung

Lauf 20261111-083624 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 10 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **60 %** (6/10) | Kategorie des LLM stimmt mit Gold überein |
| Regel-Basislinie (Schlüsselwörter) | 50 % (5/10) | Vergleich ohne KI |
| Automatisierungsquote | 80 % (8/10) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **3** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 1 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (1/1) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 100 % (6/6) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| AB-Entscheidung richtig | **100 %** (1/1) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |
| AB-Gründe exakt richtig | 0 % (0/1) | Art der Abweichung bzw. Prüfgrund stimmt |
| AB fälschlich durchgewunken | **0** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |
| Ø Antwortzeit | 6.5 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | auftragsbestaetigung | reklamation | lieferverzug | rechnung | lieferavis | preisaenderung | stammdatenaenderung | compliance | werbung | sonstiges | (keine) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **angebot** | · | · | · | · | · | · | · | · | · | · | · | · |
| **auftragsbestaetigung** | · | 1 | · | · | · | · | · | · | · | · | · | · |
| **reklamation** | · | · | 1 | · | · | · | · | · | · | · | · | · |
| **lieferverzug** | · | 1 | · | · | · | · | 1 | · | · | · | · | · |
| **rechnung** | · | · | · | · | 1 | · | · | · | · | · | · | · |
| **lieferavis** | · | · | · | · | · | · | · | · | · | · | · | · |
| **preisaenderung** | · | · | · | · | · | · | 1 | · | · | · | · | · |
| **stammdatenaenderung** | · | · | · | · | · | · | · | 1 | · | · | · | · |
| **compliance** | · | · | · | · | · | · | · | · | · | · | · | · |
| **werbung** | 1 | · | · | · | · | · | · | · | · | · | · | · |
| **sonstiges** | · | 1 | · | · | · | · | · | · | · | · | 1 | · |

## Auftragsbestätigungen

| Mail | erwartet | Ergebnis | erwartete Gründe | Gründe |
|---|---|---|---|---|
| r01_ab_teillieferung_karton | abweichung | abweichung ✗ | termin_unsicher | menge, termin_spaeter |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| r01_ab_teillieferung_karton | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| r02_reklamation_po_tippfehler | reklamation | reklamation | rechnung | 0.95 | ticket | – | – |
| r03_sammel_lieferverzug | lieferverzug | auftragsbestaetigung ✗ | lieferverzug | 0.95 | review | pflichtfeld_fehlt:bestellnummer, liefertermin_format, beleg_fehlt:bestellnummer | – |
| r04_preiserhoehung_zuschlag | preisaenderung | preisaenderung | auftragsbestaetigung | 0.95 | ticket | – | – |
| r05_rechnungsklaerung_preisabweichung | rechnung | rechnung | angebot | 0.95 | ticket | – | – |
| r06_interne_banf | sonstiges | auftragsbestaetigung ✗ | sonstiges | 0.95 | ticket | beleg_fehlt:liefertermin | – |
| r07_phishing_bank | stammdatenaenderung | stammdatenaenderung | stammdatenaenderung | 1 | review | stammdatenaenderung_pruefen, bankdatenaenderung, beleg_fehlt:bestellnummer | – |
| r08_kaltakquise_keywords | werbung | angebot ✗ | angebot | 0.8 | ticket | – | – |
| r09_edi_fehler | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| r10_chaos_mehrere_themen | lieferverzug | preisaenderung ✗ | compliance | 0.8 | ticket | – | – |
