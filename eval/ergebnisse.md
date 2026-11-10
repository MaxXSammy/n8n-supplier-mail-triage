# Auswertung der Klassifizierung

Lauf 20261110-101114 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 43 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **91 %** (39/43) | Kategorie des LLM stimmt mit Gold überein |
| Regel-Basislinie (Schlüsselwörter) | 86 % (37/43) | Vergleich ohne KI |
| Automatisierungsquote | 84 % (36/43) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **0** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 4 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (3/3) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 99 % (118/119) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| AB-Entscheidung richtig | **86 %** (18/21) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |
| AB-Gründe exakt richtig | 86 % (18/21) | Art der Abweichung bzw. Prüfgrund stimmt |
| AB fälschlich durchgewunken | **0** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |
| Aufgaben richtig verteilt | **88 %** (21/24) | Team, Art und Status jeder Aufgabe stimmen (ABs und Preiserhöhungen) |
| Abteilungen richtig erkannt | **100 %** (43/43) | Technik, QM, Disposition nötig oder nicht |
| Fehlalarme Abteilungen | 0 | Technik/QM/Disposition gemeldet, obwohl nicht nötig |
| Ø Antwortzeit | 10.0 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | auftragsbestaetigung | reklamation | lieferverzug | rechnung | preiserhoehung | sonstiges | (keine) |
|---|---|---|---|---|---|---|---|---|
| **angebot** | 3 | · | · | · | · | · | · | · |
| **auftragsbestaetigung** | 1 | 18 | · | · | · | 2 | · | · |
| **reklamation** | · | · | 4 | · | · | · | · | · |
| **lieferverzug** | · | · | · | 3 | · | · | · | · |
| **rechnung** | · | · | · | · | 3 | · | · | · |
| **preiserhoehung** | · | · | · | · | · | 5 | · | · |
| **sonstiges** | · | · | · | · | · | 1 | 3 | · |

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
| 23_ab_feldmann_palette | abweichung | review ✗ | menge | – |
| 24_ab_precimet_stammdaten | abweichung | abweichung | menge, stammdaten_pruefen | menge, stammdaten_pruefen |
| 25_ab_rossi_termin_ungewiss | abweichung | abweichung | termin_unsicher | termin_unsicher |
| 26_ab_alpen_termin_spaeter | abweichung | abweichung | termin_spaeter | termin_spaeter |
| 27_ab_swissturning_preis_und_termin | abweichung | review ✗ | preis, termin_spaeter | – |
| 28_ab_precimet_bestellung_unbekannt | review | review | bestellung_unbekannt | bestellung_unbekannt |
| 29_ab_brenner_zahlendreher | review | review | bestellung_unbekannt | bestellung_unbekannt |
| 30_ab_kovotech_englisch_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 31_ab_feldmann_mit_zitat_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 32_ab_rossi_standard_ok | automatisch_bestaetigt | automatisch_bestaetigt | – | – |
| 33_ab_precimet_liefertreue_standard | manuell_pruefen | manuell_pruefen | liefertreue_unter_schwelle | liefertreue_unter_schwelle |
| 34_ab_alpen_fremde_domain | manuell_pruefen | manuell_pruefen | absender_domain_abweichend | absender_domain_abweichend |
| 38_ab_alpen_preis_ueber_toleranz | abweichung | abweichung | preis | preis |
| 39_ab_rheinwerk_preis_ueber_euro_grenze | abweichung | abweichung | preis | preis |

## Aufgabenverteilung

| Mail | erwartet | Ergebnis |
|---|---|---|
| 16_ab_alpen_ok | Disposition:liefertermin_pruefen:erledigt | Disposition:liefertermin_pruefen:erledigt |
| 17_ab_brenner_liefertreue_ax | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 18_ab_brenner_c_artikel_ok | Disposition:liefertermin_pruefen:erledigt | Disposition:liefertermin_pruefen:erledigt |
| 19_ab_rheinwerk_blind | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 20_ab_swissturning_blind_premium | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 21_ab_nordform_neulieferant | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 22_ab_kovotech_preis | Disposition:liefertermin_pruefen:erledigt, Disposition:preis_freigeben:offen, Einkauf:preis_info:info | – ✗ |
| 23_ab_feldmann_palette | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | – ✗ |
| 24_ab_precimet_stammdaten | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 25_ab_rossi_termin_ungewiss | Disposition:liefertermin_pruefen:offen | Disposition:liefertermin_pruefen:offen |
| 26_ab_alpen_termin_spaeter | Disposition:liefertermin_pruefen:offen | Disposition:liefertermin_pruefen:offen |
| 27_ab_swissturning_preis_und_termin | Disposition:liefertermin_pruefen:offen, Einkauf:preiserhoehung_pruefen:offen | – ✗ |
| 30_ab_kovotech_englisch_ok | Disposition:liefertermin_pruefen:erledigt | Disposition:liefertermin_pruefen:erledigt |
| 31_ab_feldmann_mit_zitat_ok | Disposition:liefertermin_pruefen:erledigt | Disposition:liefertermin_pruefen:erledigt |
| 32_ab_rossi_standard_ok | Disposition:liefertermin_pruefen:erledigt | Disposition:liefertermin_pruefen:erledigt |
| 33_ab_precimet_liefertreue_standard | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 34_ab_alpen_fremde_domain | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:ab_klaeren:offen |
| 35_preiserhoehung_alpen_allgemein | Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen | Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen |
| 36_preiserhoehung_precimet_zwoelf_prozent | Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen, Strategischer Einkauf:preis_info:info | Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen, Strategischer Einkauf:preis_info:info |
| 37_preiserhoehung_swissturning_neuer_preis | Einkauf:preiserhoehung_pruefen:offen | Einkauf:preiserhoehung_pruefen:offen |
| 38_ab_alpen_preis_ueber_toleranz | Disposition:liefertermin_pruefen:erledigt, Einkauf:preiserhoehung_pruefen:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:preiserhoehung_pruefen:offen |
| 39_ab_rheinwerk_preis_ueber_euro_grenze | Disposition:liefertermin_pruefen:erledigt, Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen | Disposition:liefertermin_pruefen:erledigt, Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen |
| 40_preiserhoehung_feldmann_jahreswirkung | Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen, Geschäftsleitung:eskalation:offen, Strategischer Einkauf:preis_info:info | Einkauf:preiserhoehung_pruefen:offen, Einkaufsleitung:eskalation:offen, Geschäftsleitung:eskalation:offen, Strategischer Einkauf:preis_info:info |
| 41_preiserhoehung_rheinwerk_werkstoffwechsel | Einkauf:preiserhoehung_pruefen:offen | Einkauf:preiserhoehung_pruefen:offen |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| 01_angebot_alpen | angebot | angebot | angebot | 1 | ticket | – | – |
| 02_angebot_rossi | angebot | angebot | angebot | 1 | ticket | – | – |
| 03_angebot_kovotech_lieferzeit | angebot | angebot | angebot | 1 | ticket | – | – |
| 04_reklamation_brenner_8d | reklamation | reklamation | reklamation | 1 | ticket | – | – |
| 05_reklamation_feldmann_mit_rechnung | reklamation | reklamation | reklamation | 1 | ticket | – | – |
| 06_reklamation_swissturning_menge | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| 07_lieferverzug_rheinwerk | lieferverzug | lieferverzug | lieferverzug | 0.95 | ticket | – | – |
| 08_lieferverzug_precimet_teillieferung | lieferverzug | lieferverzug | lieferverzug | 0.9 | ticket | beleg_fehlt:liefertermin | – |
| 09_lieferverzug_alpen_kurz | lieferverzug | lieferverzug | lieferverzug | 0.95 | ticket | beleg_fehlt:liefertermin | – |
| 10_rechnung_brenner | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| 11_rechnung_swissturning_mahnung | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| 12_rechnung_kovotech_gutschrift | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| 13_sonstiges_rossi_betriebsferien | sonstiges | sonstiges | sonstiges | 1 | ticket | – | – |
| 14_sonstiges_bankdaten_betrugsversuch | sonstiges | sonstiges | auftragsbestaetigung | 1 | review | bankdatenaenderung | – |
| 15_sonstiges_precimet_zertifikat | sonstiges | sonstiges | reklamation | 0.8 | ticket | – | – |
| 16_ab_alpen_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 17_ab_brenner_liefertreue_ax | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 18_ab_brenner_c_artikel_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 19_ab_rheinwerk_blind | auftragsbestaetigung | auftragsbestaetigung | lieferverzug | 1 | ticket | – | – |
| 20_ab_swissturning_blind_premium | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 21_ab_nordform_neulieferant | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 22_ab_kovotech_preis | auftragsbestaetigung | preiserhoehung ✗ | auftragsbestaetigung | 0.95 | review | kategorie_unplausibel | liefertermin (erw. 2026-12-11, ist None) |
| 23_ab_feldmann_palette | auftragsbestaetigung | angebot ✗ | auftragsbestaetigung | 0.95 | review | kategorie_unplausibel | – |
| 24_ab_precimet_stammdaten | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 25_ab_rossi_termin_ungewiss | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | beleg_fehlt:liefertermin | – |
| 26_ab_alpen_termin_spaeter | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | – | – |
| 27_ab_swissturning_preis_und_termin | auftragsbestaetigung | preiserhoehung ✗ | auftragsbestaetigung | 1 | review | kategorie_unplausibel, beleg_fehlt:preis_prozent | – |
| 28_ab_precimet_bestellung_unbekannt | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | review | bestellung_unbekannt | – |
| 29_ab_brenner_zahlendreher | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | review | bestellung_unbekannt | – |
| 30_ab_kovotech_englisch_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 31_ab_feldmann_mit_zitat_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 32_ab_rossi_standard_ok | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 33_ab_precimet_liefertreue_standard | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 34_ab_alpen_fremde_domain | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 35_preiserhoehung_alpen_allgemein | preiserhoehung | preiserhoehung | preiserhoehung | 1 | ticket | – | – |
| 36_preiserhoehung_precimet_zwoelf_prozent | preiserhoehung | preiserhoehung | preiserhoehung | 1 | ticket | – | – |
| 37_preiserhoehung_swissturning_neuer_preis | preiserhoehung | preiserhoehung | preiserhoehung | 1 | ticket | beleg_fehlt:preis_prozent | – |
| 38_ab_alpen_preis_ueber_toleranz | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | prozent_ist_einzelpreis | – |
| 39_ab_rheinwerk_preis_ueber_euro_grenze | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 1 | ticket | – | – |
| 40_preiserhoehung_feldmann_jahreswirkung | preiserhoehung | preiserhoehung | auftragsbestaetigung | 1 | ticket | – | – |
| 41_preiserhoehung_rheinwerk_werkstoffwechsel | preiserhoehung | preiserhoehung | auftragsbestaetigung | 0.95 | ticket | beleg_fehlt:einzelpreis | – |
| 42_sonstiges_swissturning_abkuendigung | sonstiges | preiserhoehung ✗ | sonstiges | 0.6 | review | pflichtfeld_fehlt:preis_prozent|einzelpreis, konfidenz_niedrig | – |
| 43_reklamation_feldmann_sonderfreigabe | reklamation | reklamation | lieferverzug | 1 | ticket | abteilungen_nur_regel | – |
