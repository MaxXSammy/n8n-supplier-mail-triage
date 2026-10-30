# Auswertung der Klassifizierung

Lauf 20261030-193432 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 34 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **97 %** (33/34) | Kategorie des LLM stimmt mit Gold überein |
| Regel-Basislinie (Schlüsselwörter) | 91 % (31/34) | Vergleich ohne KI |
| Automatisierungsquote | 88 % (30/34) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **0** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 1 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (3/3) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 100 % (95/95) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| AB-Entscheidung richtig | **95 %** (18/19) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |
| AB-Gründe exakt richtig | 95 % (18/19) | Art der Abweichung bzw. Prüfgrund stimmt |
| AB fälschlich durchgewunken | **0** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |
| Ø Antwortzeit | 6.8 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | auftragsbestaetigung | reklamation | lieferverzug | rechnung | sonstiges | (keine) |
|---|---|---|---|---|---|---|---|
| **angebot** | 3 | · | · | · | · | · | · |
| **auftragsbestaetigung** | 1 | 18 | · | · | · | · | · |
| **reklamation** | · | · | 3 | · | · | · | · |
| **lieferverzug** | · | · | · | 3 | · | · | · |
| **rechnung** | · | · | · | · | 3 | · | · |
| **sonstiges** | · | · | · | · | · | 3 | · |

## Auftragsbestätigungen

| Mail | erwartet | Ergebnis | erwartete Gründe | Gründe |
|---|---|---|---|---|
| 16_ab_alpen_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 17_ab_brenner_liefertreue_ax | manuell_pruefen | manuell_pruefen | liefertreue_unter_schwelle | liefertreue_unter_schwelle |
| 18_ab_brenner_c_artikel_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 19_ab_rheinwerk_blind | manuell_pruefen | manuell_pruefen | blindbestaetigung_verdacht, liefertreue_unter_schwelle | blindbestaetigung_verdacht, liefertreue_unter_schwelle |
| 20_ab_swissturning_blind_premium | manuell_pruefen | manuell_pruefen | blindbestaetigung_verdacht | blindbestaetigung_verdacht |
| 21_ab_nordform_neulieferant | manuell_pruefen | manuell_pruefen | neuer_lieferant | neuer_lieferant |
| 22_ab_kovotech_preis | abweichung | review ✗ | preis | – |
| 23_ab_feldmann_palette | abweichung | abweichung | menge | menge |
| 24_ab_precimet_stammdaten | abweichung | abweichung | menge, stammdaten_pruefen | menge, stammdaten_pruefen |
| 25_ab_rossi_termin_ungewiss | abweichung | abweichung | termin_unsicher | termin_unsicher |
| 26_ab_alpen_termin_spaeter | abweichung | abweichung | termin_spaeter | termin_spaeter |
| 27_ab_swissturning_preis_und_termin | abweichung | abweichung | preis, termin_spaeter | preis, termin_spaeter |
| 28_ab_precimet_bestellung_unbekannt | review | review | bestellung_unbekannt | bestellung_unbekannt |
| 29_ab_brenner_zahlendreher | review | review | bestellung_unbekannt | bestellung_unbekannt |
| 30_ab_kovotech_englisch_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 31_ab_feldmann_mit_zitat_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 32_ab_rossi_standard_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 33_ab_precimet_liefertreue_standard | manuell_pruefen | manuell_pruefen | liefertreue_unter_schwelle | liefertreue_unter_schwelle |
| 34_ab_alpen_fremde_domain | manuell_pruefen | manuell_pruefen | absender_domain_abweichend | absender_domain_abweichend |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| 01_angebot_alpen | angebot | angebot | angebot | 0.95 | ticket | beleg_fehlt:einzelpreis | – |
| 02_angebot_rossi | angebot | angebot | angebot | 0.9 | ticket | – | – |
| 03_angebot_kovotech_lieferzeit | angebot | angebot | angebot | 0.95 | ticket | – | – |
| 04_reklamation_brenner_8d | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| 05_reklamation_feldmann_mit_rechnung | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| 06_reklamation_swissturning_menge | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| 07_lieferverzug_rheinwerk | lieferverzug | lieferverzug | lieferverzug | 1 | ticket | – | – |
| 08_lieferverzug_precimet_teillieferung | lieferverzug | lieferverzug | lieferverzug | 0.9 | ticket | beleg_fehlt:liefertermin | – |
| 09_lieferverzug_alpen_kurz | lieferverzug | lieferverzug | lieferverzug | 0.9 | ticket | beleg_fehlt:liefertermin | – |
| 10_rechnung_brenner | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| 11_rechnung_swissturning_mahnung | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| 12_rechnung_kovotech_gutschrift | rechnung | rechnung | rechnung | 0.9 | ticket | – | – |
| 13_sonstiges_rossi_betriebsferien | sonstiges | sonstiges | sonstiges | 0.8 | ticket | – | – |
| 14_sonstiges_bankdaten_betrugsversuch | sonstiges | sonstiges | auftragsbestaetigung | 0.9 | review | bankdatenaenderung | – |
| 15_sonstiges_precimet_zertifikat | sonstiges | sonstiges | reklamation | 1 | ticket | – | – |
| 16_ab_alpen_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 17_ab_brenner_liefertreue_ax | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 18_ab_brenner_c_artikel_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 19_ab_rheinwerk_blind | auftragsbestaetigung | auftragsbestaetigung | lieferverzug | 0.95 | ticket | – | – |
| 20_ab_swissturning_blind_premium | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 21_ab_nordform_neulieferant | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 22_ab_kovotech_preis | auftragsbestaetigung | angebot ✗ | auftragsbestaetigung | 0.95 | review | kategorie_unplausibel | – |
| 23_ab_feldmann_palette | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 24_ab_precimet_stammdaten | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 25_ab_rossi_termin_ungewiss | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | beleg_fehlt:liefertermin | – |
| 26_ab_alpen_termin_spaeter | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 27_ab_swissturning_preis_und_termin | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 28_ab_precimet_bestellung_unbekannt | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | review | bestellung_unbekannt | – |
| 29_ab_brenner_zahlendreher | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | review | bestellung_unbekannt | – |
| 30_ab_kovotech_englisch_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 31_ab_feldmann_mit_zitat_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 32_ab_rossi_standard_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 33_ab_precimet_liefertreue_standard | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 34_ab_alpen_fremde_domain | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
