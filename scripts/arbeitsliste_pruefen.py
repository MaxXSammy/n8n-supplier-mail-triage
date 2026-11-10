"""Schneller Test der Arbeitsliste ohne Datenbank und ohne Sprachmodell.

    python scripts/arbeitsliste_pruefen.py

Rendert den Code-Node "HTML-Seite bauen" aus workflows/02 mit festen Testdaten (tests/mocks/arbeitsliste_daten.json)
und prüft System-Empfehlungen, Sperren, Screenshot-Modus und Escaping. Braucht Node.js: lokal, sonst im laufenden
n8n-Container. Dauert rund eine Sekunde.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def rendern(daten: dict, anonym: bool, meldung: str = "") -> str:
    workflow = json.loads((REPO / "workflows" / "02_review_human_in_the_loop.json").read_text(encoding="utf-8"))
    code = next(n for n in workflow["nodes"] if n["name"] == "HTML-Seite bauen")["parameters"]["jsCode"]
    d = {**daten, "Webhook Arbeitsliste": [{"query": {"anonym": "1" if anonym else "0", "meldung": meldung}}]}
    skript = ("const D=" + json.dumps(d, ensure_ascii=False) + ";\nconst $=(k)=>({all:()=>D[k].map(j=>({json:j})),first:()=>({json:D[k][0]})});\n"
              "(async()=>{const r=await (async()=>{" + code + "})();process.stdout.write(r.json.html);})()"
              ".catch(e=>{console.error(e);process.exit(1)});")
    befehl = ["node", "-"] if shutil.which("node") else ["docker", "compose", "exec", "-T", "n8n", "node", "-"]
    r = subprocess.run(befehl, input=skript, capture_output=True, text=True, encoding="utf-8", cwd=REPO)
    if r.returncode:
        raise SystemExit(f"Rendern fehlgeschlagen:\n{r.stderr}")
    return r.stdout


def karte(html: str, ticket: int) -> str:
    """HTML der ersten Karte zu einem Ticket."""
    start = html.index(f"#{ticket} ·")
    return html[html.rfind("<article", 0, start):html.index("</article>", start)]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    daten = json.loads((REPO / "tests" / "mocks" / "arbeitsliste_daten.json").read_text(encoding="utf-8"))
    normal = rendern(daten, anonym=False, meldung="<script>alert(1)</script> Freigegeben")
    anonym = rendern(daten, anonym=True)
    lieferanten = {a["lieferant"] for a in daten["Offene Aufgaben laden"]}
    faelle = [
        ("Jede Karte hat eine System-Empfehlung", normal.count("<article") == normal.count("System-Empfehlung")),
        ("Festpreis-Vereinbarung führt zu 'Ablehnen'", "Ablehnen: Festpreis vereinbart" in karte(normal, 101)),
        ("Werkstoffwechsel: Abteilungen einbinden, Empfehlung ausführbar", "einbinden." in karte(normal, 102) and 'value="einbinden"' in karte(normal, 102)),
        ("Werkstoffwechsel: Preisfreigabe gesperrt", "disabled" in karte(normal, 102) and 'value="freigegeben"' not in karte(normal, 102)),
        ("Technik-Aufgabe: Freigeben möglich", 'value="freigegeben"' in karte(normal, 104)),
        ("Eskalation an die Geschäftsleitung als kritisch markiert", "Eskalation GL" in karte(normal, 103)),
        ("Entwurf: Als gesendet markieren", "Als gesendet markieren" in karte(normal, 105)),
        ("VPE passt nicht: Stammdaten korrigieren", "Stammdaten korrigieren" in karte(normal, 106)),
        ("Historie mit Vereinbarung und Verlauf", "Festpreis bis Q1/2027" in karte(normal, 101) and "zeitleiste" in karte(normal, 104)),
        ("Weiterleiten an Technik, QM, Disposition", all(f'name="ziel" value="{z}"' in karte(normal, 101) for z in ("technik", "qm", "dispo"))),
        ("Meldung nach der Aktion wird escaped", "&lt;script&gt;" in normal and "<script>alert(1)</script>" not in normal),
        ("Savings-Balken und Streak", "Savings YTD" in normal and "STREAK: 3 TAGE OHNE RÜCKSTAU" in normal),
        ("Screenshot-Modus: keine Lieferantennamen", not any(n in anonym for n in lieferanten)),
        ("Screenshot-Modus: keine Bestellnummern", not re.search(r"45\d{8}", anonym)),
        ("Screenshot-Modus: keine Beträge in Euro", not re.search(r"\d[\d.]*,\d\d(&nbsp;|\s)*€", anonym)),
        ("Screenshot-Modus: kein Mailtext, keine Aktionen", "16MnCr5 ist nicht mehr verfügbar" not in anonym and 'action="/webhook/aufgabe"' not in anonym),
        ("Review mit Bankdaten als kritisch markiert", "Bankdaten geändert" in normal and "badge krit" in normal),
    ]
    fehler = 0
    for name, ok in faelle:
        fehler += not ok
        print(f"{'OK    ' if ok else 'FEHLER'} {name}")
    print(f"\n{len(faelle) - fehler}/{len(faelle)} bestanden")
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
