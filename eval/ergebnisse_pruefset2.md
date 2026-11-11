# Auswertung der Klassifizierung

Lauf 20261111-082711 · Modell `qwen2.5:7b` · Konfidenz-Schwelle 0.75 · 27 Beispiel-Mails

| Kennzahl | Wert | Bedeutung |
|---|---|---|
| Klassifizierungsgenauigkeit LLM | **100 %** (27/27) | Kategorie des LLM stimmt mit Gold überein |
| Regel-Basislinie (Schlüsselwörter) | 78 % (21/27) | Vergleich ohne KI |
| Automatisierungsquote | 85 % (23/27) | Ticket ohne menschliche Prüfung angelegt |
| Falsch automatisch geroutet | **0** | Ticket mit falscher Kategorie, der teuerste Fehler |
| LLM-Fehler im Review abgefangen | 0 | falsche Kategorie, aber ein Mensch prüft |
| Pflicht-Reviews erkannt | 100 % (4/4) | z. B. geänderte Bankdaten |
| Extraktionsgenauigkeit | 95 % (18/19) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |
| AB-Entscheidung richtig | **100 %** (1/1) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |
| AB-Gründe exakt richtig | 100 % (1/1) | Art der Abweichung bzw. Prüfgrund stimmt |
| AB fälschlich durchgewunken | **0** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |
| Ø Antwortzeit | 5.8 s | je Mail, lokal inkl. Datenbank |

## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)

| Gold \ LLM | angebot | auftragsbestaetigung | reklamation | lieferverzug | rechnung | lieferavis | preisaenderung | stammdatenaenderung | compliance | werbung | sonstiges | (keine) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **angebot** | 1 | · | · | · | · | · | · | · | · | · | · | · |
| **auftragsbestaetigung** | · | 1 | · | · | · | · | · | · | · | · | · | · |
| **reklamation** | · | · | 1 | · | · | · | · | · | · | · | · | · |
| **lieferverzug** | · | · | · | 1 | · | · | · | · | · | · | · | · |
| **rechnung** | · | · | · | · | 1 | · | · | · | · | · | · | · |
| **lieferavis** | · | · | · | · | · | 4 | · | · | · | · | · | · |
| **preisaenderung** | · | · | · | · | · | · | 5 | · | · | · | · | · |
| **stammdatenaenderung** | · | · | · | · | · | · | · | 4 | · | · | · | · |
| **compliance** | · | · | · | · | · | · | · | · | 4 | · | · | · |
| **werbung** | · | · | · | · | · | · | · | · | · | 5 | · | · |
| **sonstiges** | · | · | · | · | · | · | · | · | · | · | · | · |

## Auftragsbestätigungen

| Mail | erwartet | Ergebnis | erwartete Gründe | Gründe |
|---|---|---|---|---|
| q23_kontrolle_ab_preis | abweichung | abweichung | preis | preis |

## Einzelergebnisse

| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |
|---|---|---|---|---|---|---|---|
| q01_avis_spedition | lieferavis | lieferavis | lieferavis | 1 | ticket | – | liefertermin (erw. 2026-11-12, ist None) |
| q02_avis_englisch | lieferavis | lieferavis | lieferavis | 1 | ticket | – | – |
| q03_avis_kurz | lieferavis | lieferavis | sonstiges | 1 | ticket | beleg_fehlt:liefertermin | – |
| q04_avis_tracking | lieferavis | lieferavis | lieferavis | 1 | ticket | – | – |
| q05_preis_rundschreiben | preisaenderung | preisaenderung | preisaenderung | 0.9 | ticket | – | – |
| q06_preis_einzelartikel | preisaenderung | preisaenderung | angebot | 0.95 | ticket | – | – |
| q07_abkuendigung | preisaenderung | preisaenderung | preisaenderung | 0.9 | ticket | – | – |
| q08_vpe_aenderung | preisaenderung | preisaenderung | preisaenderung | 0.9 | ticket | – | – |
| q09_energiezuschlag | preisaenderung | preisaenderung | auftragsbestaetigung | 0.95 | ticket | – | – |
| q10_bank_neu | stammdatenaenderung | stammdatenaenderung | auftragsbestaetigung | 1 | review | stammdatenaenderung_pruefen, bankdatenaenderung | – |
| q11_adresse_umzug | stammdatenaenderung | stammdatenaenderung | auftragsbestaetigung | 1 | review | stammdatenaenderung_pruefen | – |
| q12_ustid | stammdatenaenderung | stammdatenaenderung | stammdatenaenderung | 1 | review | stammdatenaenderung_pruefen | – |
| q13_bank_englisch | stammdatenaenderung | stammdatenaenderung | stammdatenaenderung | 1 | review | stammdatenaenderung_pruefen | – |
| q14_iso_zertifikat | compliance | compliance | compliance | 1 | ticket | – | – |
| q15_reach | compliance | compliance | compliance | 1 | ticket | – | – |
| q16_code_of_conduct | compliance | compliance | compliance | 0.9 | ticket | – | – |
| q17_konfliktmineralien | compliance | compliance | compliance | 1 | ticket | – | – |
| q18_kaltakquise | werbung | werbung | werbung | 0.9 | ticket | – | – |
| q19_webinar | werbung | werbung | werbung | 0.9 | ticket | – | – |
| q20_portal_einladung | werbung | werbung | werbung | 0.9 | ticket | – | – |
| q21_sonderangebot_newsletter | werbung | werbung | angebot | 0.9 | ticket | – | – |
| q22_messeeinladung | werbung | werbung | werbung | 0.9 | ticket | – | – |
| q23_kontrolle_ab_preis | auftragsbestaetigung | auftragsbestaetigung | auftragsbestaetigung | 0.95 | ticket | kategorie_korrigiert:preisaenderung->auftragsbestaetigung | – |
| q24_kontrolle_angebot | angebot | angebot | angebot | 0.95 | ticket | – | – |
| q25_kontrolle_reklamation_zertifikat | reklamation | reklamation | reklamation | 0.95 | ticket | – | – |
| q26_kontrolle_rechnung_preisabweichung | rechnung | rechnung | rechnung | 1 | ticket | – | – |
| q27_kontrolle_lieferverzug | lieferverzug | lieferverzug | lieferverzug | 0.95 | ticket | – | – |
