"""Rechnet die Zeitersparnis hoch. Alle Eingaben kommen aus Messungen im Team, nicht aus Annahmen.

    python scripts/einsparung.py --mails-pro-monat 600 --min-manuell 4 --min-pruefung 2 --stundensatz 55

--mails-pro-monat  Lieferanten-Mails im Sammelpostfach pro Monat (aus dem Postfach zählen)
--min-manuell      Minuten je Mail ohne Tool: lesen, zuordnen, Daten abtippen, weiterleiten (Stoppuhr-Messung)
--min-pruefung     Minuten je Mail, die das Tool einem Menschen vorlegt (Prüfen mit fertiger Zusammenfassung)
--stundensatz      Vollkosten je Arbeitsstunde in Euro
--quote            Automatisierungsquote, Standard aus dem letzten Eval-Lauf (eval/ergebnisse.json)
"""
import argparse
import json
from pathlib import Path

ERGEBNISSE = Path(__file__).resolve().parent.parent / "eval" / "ergebnisse.json"


def quote_aus_eval() -> float:
    daten = json.loads(ERGEBNISSE.read_text(encoding="utf-8"))["ergebnisse"]
    return sum(e["status"] == "ticket" for e in daten) / len(daten)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mails-pro-monat", type=float, required=True)
    p.add_argument("--min-manuell", type=float, required=True)
    p.add_argument("--min-pruefung", type=float, required=True)
    p.add_argument("--stundensatz", type=float, required=True)
    p.add_argument("--quote", type=float, default=None)
    a = p.parse_args()
    q = a.quote if a.quote is not None else quote_aus_eval()

    vorher = a.mails_pro_monat * a.min_manuell / 60
    nachher = a.mails_pro_monat * (1 - q) * a.min_pruefung / 60
    spar = vorher - nachher
    print(f"Automatisierungsquote:   {q:.0%}")
    print(f"Aufwand ohne Tool:       {vorher:7.1f} Std./Monat")
    print(f"Aufwand mit Tool:        {nachher:7.1f} Std./Monat")
    print(f"Ersparnis:               {spar:7.1f} Std./Monat = {spar * 12:.0f} Std./Jahr = {spar * a.stundensatz * 12:,.0f} Euro/Jahr".replace(",", "."))
    print("Nicht eingerechnet: vermiedene Fehlrouten, schnellere Reaktion, Betrugs-Warnungen.")


if __name__ == "__main__":
    main()
