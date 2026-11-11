"""Schickt alle Beispiel-Mails durch den laufenden n8n-Workflow und vergleicht mit den Gold-Daten.

    python scripts/evaluate.py

Schreibt eval/ergebnisse.md (für die README) und eval/ergebnisse.json (Rohdaten des Laufs).
Jeder Lauf hängt eine Lauf-Kennung an die Message-ID, damit die Duplikat-Erkennung nicht greift.
Danach werden diese Test-Tickets wieder gelöscht (außer mit --behalten).
"""
import argparse
import json
import sys
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path

from webhook_client import REPO, STANDARD_URL, env_lesen, mail_senden

KATEGORIEN = ["angebot", "auftragsbestaetigung", "reklamation", "lieferverzug", "rechnung", "lieferavis",
              "preisaenderung", "stammdatenaenderung", "compliance", "werbung", "sonstiges"]

# Regel-Basislinie: Schlüsselwörter je Kategorie. Zeigt, was das LLM gegenüber einfachen Regeln bringt.
REGELN = {
    "auftragsbestaetigung": r"auftragsbestätigung|\bab\b|bestätigen|conferma|order confirmation",
    "rechnung": r"rechnung|gutschrift|zahlungserinnerung|mahnung|zahlungsziel",
    "reklamation": r"reklamation|mängelrüge|8d|beschädig|n\.i\.o|qualität",
    "lieferverzug": r"liefertermin|verschiebt|verzöger|teillieferung|restmenge|nicht halten",
    "lieferavis": r"versandavis|sendungsnummer|tracking|spedition|dispatch|shipping notice",
    "stammdatenaenderung": r"bankverbindung|bank details|neue anschrift|ust-id|iban",
    "compliance": r"reach|rohs|zertifikat|code of conduct|konfliktmineralien|iso 9001",
    "werbung": r"newsletter|webinar|messe|einladung|abmelden|rabatt",
    "preisaenderung": r"preisanpassung|zuschlag|abkündigung|verpackungseinheit|preise zum",
    "angebot": r"angebot|offerta|stückpreis|preis",
}


def regel_klassifizieren(mail: dict) -> str:
    """Erste Kategorie mit einem Treffer im Betreff, sonst im Text, sonst 'sonstiges'."""
    for feld in ("subject", "body"):
        for kategorie, muster in REGELN.items():
            if re.search(muster, mail[feld], re.IGNORECASE):
                return kategorie
    return "sonstiges"


def feld_gleich(erwartet, ist) -> bool:
    if erwartet is None:
        return ist is None
    if isinstance(erwartet, (int, float)):
        return isinstance(ist, (int, float)) and abs(erwartet - ist) < 0.0001
    return isinstance(ist, str) and ist.strip().upper() == str(erwartet).upper()


def ab_ist(antwort: dict) -> tuple[str | None, list[str]]:
    """Ergebnis der AB-Prüfung aus der Webhook-Antwort: (Ergebnis, Gründe)."""
    if antwort.get("status") == "review":
        return "review", sorted(g for g in antwort.get("gruende", []) if g == "bestellung_unbekannt")
    ab = antwort.get("ab_pruefung") or {}
    gruende = [a["art"] for a in ab.get("abweichungen", [])] + ab.get("pruefgruende", [])
    return ab.get("ergebnis"), sorted(gruende)


def prozent(zaehler: int, nenner: int) -> str:
    return f"{zaehler / nenner:.0%}".replace("%", " %") if nenner else "–"


AUFRAEUMEN_SQL = """
DELETE FROM entwuerfe WHERE ticket_id IN (SELECT id FROM tickets WHERE mail_id LIKE '%-eval%');
DELETE FROM review_queue WHERE mail_id LIKE '%-eval%';
DELETE FROM tickets WHERE mail_id LIKE '%-eval%';
"""


def testdaten_loeschen() -> None:
    """Entfernt die Tickets und Reviews dieses Laufs, damit die Arbeitsliste nur echte Fälle zeigt."""
    ergebnis = subprocess.run(
        ["docker", "compose", "exec", "-T", "postgres", "psql", "-U", env_lesen().get("POSTGRES_USER", "n8n"), "-d", "triage"],
        input=AUFRAEUMEN_SQL, text=True, capture_output=True, cwd=REPO)
    print("Testdaten dieses Laufs gelöscht." if ergebnis.returncode == 0 else f"Aufräumen fehlgeschlagen: {ergebnis.stderr}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows-Konsole: ✓ und Umlaute
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--url", default=STANDARD_URL)
    parser.add_argument("--set", default="", help="Ordner mit eigenen mails/ und gold.json, z. B. pruefset (Ergebnis: eval/ergebnisse_<set>.*)")
    parser.add_argument("--behalten", action="store_true", help="Tickets und Reviews des Laufs nicht löschen")
    args = parser.parse_args()

    env = env_lesen()
    token = env.get("WEBHOOK_TOKEN", "")
    modell = env.get("OLLAMA_MODEL", "?")
    schwelle = env.get("KONFIDENZ_SCHWELLE", "?")
    mail_ordner = REPO / args.set / "mails" if args.set else REPO / "mails"
    gold_datei = REPO / args.set / "gold.json" if args.set else REPO / "eval" / "gold.json"
    ausgabe = f"ergebnisse_{args.set}" if args.set else "ergebnisse"
    gold = json.loads(gold_datei.read_text(encoding="utf-8"))
    lauf = datetime.now().strftime("%Y%m%d-%H%M%S")

    ergebnisse = []
    for name, erwartung in gold.items():
        mail = json.loads((mail_ordner / f"{name}.json").read_text(encoding="utf-8"))
        mail["message_id"] = mail["message_id"].replace(">", f"-eval{lauf}>")
        status, antwort, dauer = mail_senden(mail, args.url, token)
        daten = antwort.get("daten") or {}
        ergebnis = {
            "mail": name,
            "http": status,
            "status": antwort.get("status"),
            "gold": erwartung["kategorie"],
            "llm": daten.get("kategorie"),
            "regel": regel_klassifizieren(mail),
            "konfidenz": daten.get("konfidenz"),
            "gruende": antwort.get("gruende", []),
            "warnungen": antwort.get("warnungen", []),
            "muss_review": erwartung["muss_review"],
            "mehrdeutig": erwartung.get("mehrdeutig", False),
            "felder": {f: [w, daten.get(f)] for f, w in erwartung["felder"].items()},
            "ab": ({"erwartet": erwartung["ab"]["ergebnis"], "erwartete_gruende": sorted(erwartung["ab"]["gruende"]),
                    "ist": ab_ist(antwort)[0], "ist_gruende": ab_ist(antwort)[1]} if "ab" in erwartung else None),
            "sekunden": round(dauer, 2),
        }
        ergebnisse.append(ergebnis)
        markierung = "✓" if ergebnis["llm"] == ergebnis["gold"] else "✗"
        print(f"{markierung} {name:42} gold={ergebnis['gold']:20} llm={str(ergebnis['llm']):20} "
              f"→ {ergebnis['status']:7} {ergebnis['sekunden']:5.1f} s {' '.join(ergebnis['gruende'])}")

    n = len(ergebnisse)
    llm_richtig = sum(e["llm"] == e["gold"] for e in ergebnisse)
    regel_richtig = sum(e["regel"] == e["gold"] for e in ergebnisse)
    eindeutig = [e for e in ergebnisse if not e["mehrdeutig"]]
    eindeutig_richtig = sum(e["llm"] == e["gold"] for e in eindeutig)
    tickets = [e for e in ergebnisse if e["status"] == "ticket"]
    reviews = [e for e in ergebnisse if e["status"] == "review"]
    falsch_automatisch = [e for e in tickets if e["llm"] != e["gold"]]
    falsch_abgefangen = [e for e in reviews if e["llm"] != e["gold"]]
    pflicht_review = [e for e in ergebnisse if e["muss_review"]]
    feldvergleiche = [feld_gleich(w, i) for e in ergebnisse for w, i in e["felder"].values()]
    avg_sekunden = sum(e["sekunden"] for e in ergebnisse) / n
    abs_ = [e for e in ergebnisse if e["ab"]]
    ab_richtig = [e for e in abs_ if e["ab"]["ist"] == e["ab"]["erwartet"]]
    ab_gruende_richtig = [e for e in ab_richtig if e["ab"]["ist_gruende"] == e["ab"]["erwartete_gruende"]]
    ab_falsch_durch = [e for e in abs_ if e["ab"]["ist"] == "automatisch_bestaetigt" != e["ab"]["erwartet"]]

    matrix = Counter((e["gold"], e["llm"]) for e in ergebnisse)
    spalten = KATEGORIEN + ["(keine)"]

    zeilen = [
        f"# Auswertung der Klassifizierung",
        "",
        f"Lauf {lauf} · Modell `{modell}` · Konfidenz-Schwelle {schwelle} · {n} Beispiel-Mails",
        "",
        "| Kennzahl | Wert | Bedeutung |",
        "|---|---|---|",
        f"| Klassifizierungsgenauigkeit LLM | **{prozent(llm_richtig, n)}** ({llm_richtig}/{n}) | Kategorie des LLM stimmt mit Gold überein |",
        *([f"| davon ohne mehrdeutige Mails | {prozent(eindeutig_richtig, len(eindeutig))} ({eindeutig_richtig}/{len(eindeutig)}) | Mails mit eindeutiger Lösung, mehrdeutige sind im Gold markiert |"]
          if len(eindeutig) != n else []),
        f"| Regel-Basislinie (Schlüsselwörter) | {prozent(regel_richtig, n)} ({regel_richtig}/{n}) | Vergleich ohne KI |",
        f"| Automatisierungsquote | {prozent(len(tickets), n)} ({len(tickets)}/{n}) | Ticket ohne menschliche Prüfung angelegt |",
        f"| Falsch automatisch geroutet | **{len(falsch_automatisch)}** | Ticket mit falscher Kategorie, der teuerste Fehler |",
        f"| LLM-Fehler im Review abgefangen | {len(falsch_abgefangen)} | falsche Kategorie, aber ein Mensch prüft |",
        f"| Pflicht-Reviews erkannt | {prozent(sum(e['status'] == 'review' for e in pflicht_review), len(pflicht_review))} ({sum(e['status'] == 'review' for e in pflicht_review)}/{len(pflicht_review)}) | z. B. geänderte Bankdaten |",
        f"| Extraktionsgenauigkeit | {prozent(sum(feldvergleiche), len(feldvergleiche))} ({sum(feldvergleiche)}/{len(feldvergleiche)}) | Bestell-, Rechnungs-, Angebotsnummer, Betrag, Währung, Termin |",
        f"| AB-Entscheidung richtig | **{prozent(len(ab_richtig), len(abs_))}** ({len(ab_richtig)}/{len(abs_)}) | automatisch bestätigt, manuell prüfen, Abweichung oder Review |",
        f"| AB-Gründe exakt richtig | {prozent(len(ab_gruende_richtig), len(abs_))} ({len(ab_gruende_richtig)}/{len(abs_)}) | Art der Abweichung bzw. Prüfgrund stimmt |",
        f"| AB fälschlich durchgewunken | **{len(ab_falsch_durch)}** | automatisch bestätigt, obwohl ein Mensch prüfen sollte |",
        f"| Ø Antwortzeit | {avg_sekunden:.1f} s | je Mail, lokal inkl. Datenbank |",
        "",
        "## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)",
        "",
        "| Gold \\ LLM | " + " | ".join(spalten) + " |",
        "|---|" + "---|" * len(spalten),
    ]
    for gold_k in KATEGORIEN:
        zellen = [str(matrix.get((gold_k, k if k != "(keine)" else None), 0) or "·") for k in spalten]
        zeilen.append(f"| **{gold_k}** | " + " | ".join(zellen) + " |")

    zeilen += ["", "## Auftragsbestätigungen", "",
               "| Mail | erwartet | Ergebnis | erwartete Gründe | Gründe |", "|---|---|---|---|---|"]
    for e in abs_:
        a = e["ab"]
        ok = "" if a["ist"] == a["erwartet"] and a["ist_gruende"] == a["erwartete_gruende"] else " ✗"
        zeilen.append(f"| {e['mail']} | {a['erwartet']} | {a['ist']}{ok} | {', '.join(a['erwartete_gruende']) or '–'} "
                      f"| {', '.join(a['ist_gruende']) or '–'} |")

    zeilen += ["", "## Einzelergebnisse", "",
               "| Mail | Gold | LLM | Regel | Konfidenz | Ergebnis | Gründe / Warnungen | Felder falsch |",
               "|---|---|---|---|---|---|---|---|"]
    for e in ergebnisse:
        falsche = [f"{f} (erw. {w}, ist {i})" for f, (w, i) in e["felder"].items() if not feld_gleich(w, i)]
        hinweise = ", ".join(e["gruende"] + e["warnungen"]) or "–"
        zeilen.append(
            f"| {e['mail']} | {e['gold']} | {e['llm'] or '–'}{'' if e['llm'] == e['gold'] else ' ✗'} | {e['regel']} "
            f"| {e['konfidenz'] if e['konfidenz'] is not None else '–'} | {e['status']} | {hinweise} | {'; '.join(falsche) or '–'} |"
        )

    (REPO / "eval" / f"{ausgabe}.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    (REPO / "eval" / f"{ausgabe}.json").write_text(
        json.dumps({"lauf": lauf, "modell": modell, "schwelle": schwelle, "ergebnisse": ergebnisse},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\n" + "\n".join(zeilen[4:zeilen.index("## Konfusionsmatrix (Zeile = Gold, Spalte = LLM)")]))
    print(f"\n→ eval/{ausgabe}.md")
    if not args.behalten:
        testdaten_loeschen()


if __name__ == "__main__":
    main()
