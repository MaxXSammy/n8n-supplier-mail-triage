# Auswertung der Klassifizierung

Lauf 20261111-082949 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 31 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **87 %** (27/31) | Kategorie des LLM stimmt mit Gold überein |
| Regel-Basislinie (Schlüsselwörter) | 77 % (24/31) | Vergleich ohne KI |
| Automatisierungsquote | 87 % (27/31) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **3** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 1 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (3/3) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 96 % (81/84) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| AB-Entscheidung richtig | **86 %** (12/14) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |
| AB-Gründe exakt richtig | 86 % (12/14) | Art der Abweichung bzw. Prüfgrund stimmt |
| AB fälschlich durchgewunken | **0** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |
| Ø Antwortzeit | 6.0 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | auftragsbestaetigung | reklamation | lieferverzug | rechnung | lieferavis | preisaenderung | stammdatenaenderung | compliance | werbung | sonstiges | (keine) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **angebot** | 3 | · | · | · | · | · | 1 | · | · | · | · | · |
| **auftragsbestaetigung** | · | 13 | · | 1 | · | · | · | · | · | · | · | · |
| **reklamation** | · | · | 3 | · | · | · | · | · | · | · | · | · |
| **lieferverzug** | · | · | · | 3 | · | · | · | · | · | · | · | · |
| **rechnung** | · | · | · | · | 3 | · | · | · | · | · | · | · |
| **lieferavis** | · | · | · | · | · | · | · | · | · | · | · | · |
| **preisaenderung** | · | · | · | · | · | · | · | · | · | · | · | · |
| **stammdatenaenderung** | · | · | · | · | · | · | · | · | · | · | · | · |
| **compliance** | · | · | · | · | · | · | · | · | · | · | · | · |
| **werbung** | · | · | · | · | · | · | · | · | · | · | · | · |
| **sonstiges** | · | · | · | · | · | · | · | 1 | · | 1 | 2 | · |

## Auftragsbestätigungen

| Mail | erwartet | Ergebnis | erwartete Gründe | Gründe |
|---|---|---|---|---|
| p01_ab_swiss_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| p02_ab_brenner_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| p03_ab_alpen_termin_spaeter | abweichung | abweichung | termin_spaeter | termin_spaeter |
| p04_ab_alpen_teilmenge | abweichung | None ✗ | menge | – |
| p05_ab_rheinwerk_liefertreue | manuell_pruefen | manuell_pruefen | liefertreue_unter_schwelle | liefertreue_unter_schwelle |
| p06_ab_kovotech_englisch | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| p07_ab_feldmann_preis_termin | abweichung | abweichung | preis, termin_spaeter | preis, termin_spaeter |
| p08_ab_rossi_datum_mit_schraegstrich | automatisch_bestaetigt | abweichung ✗ | – | termin_fehlt |
| p09_ab_rossi_termin_unsicher | abweichung | abweichung | termin_unsicher | termin_unsicher |
| p10_ab_swiss_blind | manuell_pruefen | manuell_pruefen | blindbestaetigung_verdacht | blindbestaetigung_verdacht |
| p11_ab_precimet_liefertreue_knapp | manuell_pruefen | manuell_pruefen | liefertreue_unter_schwelle | liefertreue_unter_schwelle |
| p12_ab_nordform_neu | manuell_pruefen | manuell_pruefen | neuer_lieferant | neuer_lieferant |
| p13_ab_bestellung_unbekannt | review | review | bestellung_unbekannt | bestellung_unbekannt |
| p14_ab_alpen_domain_vertippt | manuell_pruefen | manuell_pruefen | absender_domain_abweichend | absender_domain_abweichend |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| p01_ab_swiss_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p02_ab_brenner_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p03_ab_alpen_termin_spaeter | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p04_ab_alpen_teilmenge | auftragsbestaetigung | lieferverzug ✗ | auftragsbestaetigung | 0.95 | ticket | – | – |
| p05_ab_rheinwerk_liefertreue | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p06_ab_kovotech_englisch | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p07_ab_feldmann_preis_termin | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p08_ab_rossi_datum_mit_schraegstrich | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | beleg_fehlt:liefertermin | liefertermin (erw. 2026-12-10, ist None) |
| p09_ab_rossi_termin_unsicher | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p10_ab_swiss_blind | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p11_ab_precimet_liefertreue_knapp | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p12_ab_nordform_neu | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p13_ab_bestellung_unbekannt | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | review | bestellung_unbekannt | – |
| p14_ab_alpen_domain_vertippt | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| p15_angebot_kuhnert | angebot | angebot | angebot | 0.9 | ticket | – | – |
| p16_angebot_englisch | angebot | angebot | sonstiges | 0.95 | ticket | – | – |
| p17_angebot_ohne_nummer | angebot | angebot | angebot | 0.95 | ticket | – | – |
| p18_angebot_preisanpassung | angebot | preisaenderung ✗ | auftragsbestaetigung | 0.9 | ticket | – | – |
| p19_reklamation_8d | reklamation | reklamation | reklamation | 1 | ticket | – | – |
| p20_reklamation_ersatz | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| p21_reklamation_italienisch | reklamation | reklamation | sonstiges | 0.95 | ticket | – | – |
| p22_lieferverzug_neuer_termin | lieferverzug | lieferverzug | lieferverzug | 0.95 | ticket | – | – |
| p23_lieferverzug_teillieferung | lieferverzug | lieferverzug | lieferverzug | 0.9 | ticket | – | – |
| p24_lieferverzug_englisch | lieferverzug | lieferverzug | sonstiges | 0.95 | ticket | beleg_fehlt:liefertermin | liefertermin (erw. 2026-12-18, ist None) |
| p25_rechnung_chf | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| p26_zahlungserinnerung | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| p27_gutschrift | rechnung | rechnung | rechnung | 1 | review | pflichtfeld_fehlt:betrag, beleg_fehlt:betrag | betrag (erw. 312.5, ist None) |
| p28_betriebsferien | sonstiges | sonstiges | sonstiges | 0.9 | ticket | – | – |
| p29_bankdaten_betrug | sonstiges | stammdatenaenderung ✗ | stammdatenaenderung | 1 | review | stammdatenaenderung_pruefen, bankdatenaenderung | – |
| p30_newsletter_messe | sonstiges | werbung ✗ | werbung | 0.9 | ticket | – | – |
| p31_injektion | sonstiges | sonstiges | rechnung | 0.6 | review | konfidenz_niedrig, prompt_injection_verdacht | – |
