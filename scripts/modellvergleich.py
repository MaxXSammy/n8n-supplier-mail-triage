"""Vergleicht das lokale Modell mit Cloud-Modellen auf denselben Mails, mit denselben Prüfregeln.

    python scripts/modellvergleich.py qwen
    python scripts/modellvergleich.py haiku      # Claude Code CLI, angemeldet mit eigenem Abo
    python scripts/modellvergleich.py bericht    # nur den Bericht aus den vorhandenen Antworten bauen

Prompt, JSON-Schema, Validierung und AB-Prüfung kommen aus den Code-Nodes des Workflows (pipeline.mjs).
Antworten werden je Mail gespeichert, ein abgebrochener Lauf macht beim nächsten Aufruf weiter.
Braucht Docker (Bestelldaten aus db/init.sql) und für Node.js entweder eine lokale Installation oder das n8n-Image.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from evaluate import ab_ist, feld_gleich, prozent, regel_klassifizieren

REPO = Path(__file__).resolve().parent.parent
ABLAGE = REPO / "eval" / "modellvergleich"
N8N_IMAGE = "docker.n8n.io/n8nio/n8n:2.45.7"
MODELLE = {"qwen": "qwen2.5:7b", "haiku": "haiku"}


class Abbruch(Exception):
    """Der Aufruf selbst ist gescheitert (Netz, Anmeldung, Limit). Das zählt nicht als Fehler des Modells."""


def lauf(befehl: list[str], eingabe: str | None = None, **optionen) -> str:
    ergebnis = subprocess.run(befehl, input=eingabe, capture_output=True, text=True, encoding="utf-8", **optionen)
    if ergebnis.returncode != 0:
        raise Abbruch(f"{befehl[0]} meldet Fehler:\n{ergebnis.stderr or ergebnis.stdout}")
    return ergebnis.stdout


def pipeline(schritt: str, daten: dict) -> dict:
    if shutil.which("node"):
        befehl = ["node", "scripts/pipeline.mjs", schritt]
    else:
        befehl = ["docker", "run", "--rm", "-i", "--network", "none", "--entrypoint", "node",
                  "-v", f"{REPO}:/repo:ro", "-w", "/repo", N8N_IMAGE, "scripts/pipeline.mjs", schritt]
    return json.loads(lauf(befehl, json.dumps(daten, ensure_ascii=False), cwd=REPO))


def bestellungen_laden() -> dict:
    """Startet kurz ein leeres Postgres mit db/init.sql und liest die Zeilen wie der Node "Bestellung laden"."""
    workflow = json.loads((REPO / "workflows" / "01_mail_triage.json").read_text(encoding="utf-8"))
    abfrage = next(n for n in workflow["nodes"] if n["name"] == "Bestellung laden")["parameters"]["query"]
    abfrage = abfrage.split("WHERE b.bestellnummer")[0]
    behaelter = lauf(["docker", "run", "-d", "--rm", "--network", "none", "-e", "POSTGRES_PASSWORD=nur-fuer-den-test",
                      "-v", f"{REPO / 'db' / 'init.sql'}:/docker-entrypoint-initdb.d/init.sql:ro",
                      "postgres:17-alpine"]).strip()
    try:
        for _ in range(60):
            # Über TCP erst erreichbar, wenn init.sql vollständig gelaufen ist
            bereit = subprocess.run(["docker", "exec", behaelter, "pg_isready", "-h", "127.0.0.1"], capture_output=True)
            if bereit.returncode == 0:
                break
            time.sleep(1)
        else:
            raise Abbruch("Postgres wurde nicht bereit")
        sql = f"SELECT jsonb_object_agg(x.bestellnummer, to_jsonb(x)) FROM ({abfrage}) x;"
        return json.loads(lauf(["docker", "exec", "-i", behaelter, "psql", "-U", "postgres", "-d", "triage",
                                "-At", "-v", "ON_ERROR_STOP=1"], sql))
    finally:
        subprocess.run(["docker", "stop", behaelter], capture_output=True)


def http_json(url: str, daten: dict, kopf: dict) -> dict:
    anfrage = urllib.request.Request(url, json.dumps(daten).encode(), {"Content-Type": "application/json", **kopf})
    with urllib.request.urlopen(anfrage, timeout=120) as antwort:
        return json.loads(antwort.read())


def frage_qwen(anfrage: dict) -> dict:
    start = time.perf_counter()
    try:
        r = http_json("http://127.0.0.1:11434/api/chat", anfrage, {})
    except (urllib.error.URLError, TimeoutError) as fehler:
        raise Abbruch(f"Ollama nicht erreichbar: {fehler}") from fehler
    return {"inhalt": r["message"]["content"], "sekunden": time.perf_counter() - start,
            "tokens_ein": r.get("prompt_eval_count"), "tokens_aus": r.get("eval_count"), "modell": r.get("model")}


def claude_programm() -> str:
    pfad = os.environ.get("CLAUDE_BIN") or shutil.which("claude")
    if not pfad:
        raise Abbruch("Claude Code CLI nicht gefunden. Pfad in der Umgebungsvariable CLAUDE_BIN angeben.")
    return pfad


def frage_haiku(anfrage: dict) -> dict:
    system, nutzer = (m["content"] for m in anfrage["messages"])
    # Ohne API-Key und ohne Variablen einer laufenden Sitzung, damit die eigene Abo-Anmeldung zählt
    umgebung = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "ANTHROPIC"))}
    umgebung["MAX_THINKING_TOKENS"] = "0"
    befehl = [claude_programm(), "-p", "--model", MODELLE["haiku"], "--output-format", "json",
              "--system-prompt", system, "--json-schema", json.dumps(anfrage["format"]),
              "--tools", "", "--safe-mode", "--strict-mcp-config", "--no-session-persistence"]
    start = time.perf_counter()
    with tempfile.TemporaryDirectory() as leer:  # leerer Ordner: keine Projektdateien im Kontext
        ergebnis = subprocess.run(befehl, input=nutzer, capture_output=True, text=True, encoding="utf-8",
                                  cwd=leer, env=umgebung, timeout=180)
    dauer = time.perf_counter() - start
    try:
        r = json.loads(ergebnis.stdout)
    except json.JSONDecodeError as fehler:
        raise Abbruch(f"claude -p: {ergebnis.stderr or ergebnis.stdout}") from fehler
    if r.get("is_error") or r.get("structured_output") is None:
        raise Abbruch(f"claude -p: {r.get('subtype')} {r.get('result')}")
    nutzung = r.get("usage", {})
    eingang = sum(nutzung.get(k) or 0 for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return {"inhalt": json.dumps(r["structured_output"], ensure_ascii=False), "sekunden": dauer,
            "sekunden_api": (r.get("duration_api_ms") or 0) / 1000, "tokens_ein": eingang,
            "tokens_aus": nutzung.get("output_tokens"), "kosten_usd": r.get("total_cost_usd"),
            "modell": ", ".join(r.get("modelUsage", {})) or MODELLE["haiku"]}


def mails_laden(satz: str) -> tuple[dict, dict]:
    gold = json.loads((REPO / satz / "gold.json").read_text(encoding="utf-8"))
    mails = {n: json.loads((REPO / satz / "mails" / f"{n}.json").read_text(encoding="utf-8")) for n in gold}
    return gold, mails


def messen(wer: str, satz: str, limit: int | None) -> None:
    gold, mails = mails_laden(satz)
    datei = ABLAGE / f"{satz}_{wer}.json"
    fertig = json.loads(datei.read_text(encoding="utf-8")) if datei.exists() else {}
    offen = [n for n in gold if n not in fertig][:limit]
    if not offen:
        print(f"{wer}: alle Antworten vorhanden ({datei.name})")
        return
    anfragen = pipeline("bauen", {"mails": {n: mails[n] for n in offen}})
    frage = {"qwen": frage_qwen, "haiku": frage_haiku}[wer]
    if wer == "qwen":
        frage(anfragen[offen[0]])  # Modell laden, damit die erste Zeitmessung nicht verfälscht ist
    ABLAGE.mkdir(parents=True, exist_ok=True)
    for i, name in enumerate(offen, 1):
        fertig[name] = frage(anfragen[name])
        datei.write_text(json.dumps(fertig, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{wer} {i}/{len(offen)} {name} {fertig[name]['sekunden']:.1f} s", flush=True)


def kennzahlen(gold: dict, mails: dict, antworten: dict, geprueft: dict) -> dict:
    n = len(antworten)
    kategorie = {k: (geprueft[k]["daten"] or {}).get("kategorie") for k in antworten}
    richtig = [k for k in antworten if kategorie[k] == gold[k]["kategorie"]]
    eindeutig = [k for k in antworten if not gold[k].get("mehrdeutig")]
    ohne_sonstiges = [k for k in antworten if gold[k]["kategorie"] != "sonstiges"]
    tickets = [k for k in antworten if geprueft[k]["status"] == "ticket"]
    pflicht = [k for k in antworten if gold[k]["muss_review"]]
    felder = [feld_gleich(w, (geprueft[k]["daten"] or {}).get(f)) for k in antworten for f, w in gold[k]["felder"].items()]
    ab = [k for k in antworten if "ab" in gold[k]]
    ab_ergebnis = {k: ab_ist(geprueft[k])[0] for k in ab}
    zeiten = sorted(a["sekunden"] for a in antworten.values())
    kosten = [a.get("kosten_usd") for a in antworten.values()]

    def anteil(teil: list, ganz: list) -> str:
        return f"{prozent(len(teil), len(ganz))} ({len(teil)}/{len(ganz)})"

    return {
        "Modell": ", ".join(sorted({a["modell"] for a in antworten.values()})),
        "Mails": str(n),
        "Kategorie richtig": anteil(richtig, list(antworten)),
        "ohne mehrdeutige Mails": anteil([k for k in eindeutig if k in richtig], eindeutig),
        "ohne Kategorie sonstiges": anteil([k for k in ohne_sonstiges if k in richtig], ohne_sonstiges),
        "Ticket ohne Mensch": anteil(tickets, list(antworten)),
        "falsch automatisch geroutet": str(len([k for k in tickets if k not in richtig])),
        "Pflicht-Reviews erkannt": anteil([k for k in pflicht if geprueft[k]["status"] == "review"], pflicht),
        "Felder richtig ausgelesen": anteil([f for f in felder if f], felder),
        "AB-Entscheidung richtig": anteil([k for k in ab if ab_ergebnis[k] == gold[k]["ab"]["ergebnis"]], ab),
        "AB fälschlich durchgewunken": str(sum(
            ab_ergebnis[k] == "automatisch_bestaetigt" != gold[k]["ab"]["ergebnis"] for k in ab)),
        "Antwortzeit Median": f"{zeiten[n // 2]:.1f} s",
        "Tokens je Mail (ein / aus)": " / ".join(
            f"{sum(a[f] or 0 for a in antworten.values()) / n:.0f}" for f in ("tokens_ein", "tokens_aus")),
        "Listenpreis laut CLI, 1.000 Mails": f"{sum(kosten) / n * 1000:.2f} USD" if all(k is not None for k in kosten) else "–",
        "Regel-Basislinie ohne KI": anteil(
            [k for k in antworten if regel_klassifizieren(mails[k]) == gold[k]["kategorie"]], list(antworten)),
    }


def bericht(satz: str) -> None:
    gold, mails = mails_laden(satz)
    vorhanden = {w: json.loads(p.read_text(encoding="utf-8")) for w in MODELLE
                 if (p := ABLAGE / f"{satz}_{w}.json").exists()}
    if not vorhanden:
        raise Abbruch("Noch keine Antworten gespeichert")
    bestellungen = bestellungen_laden()
    spalten = {}
    for wer, antworten in vorhanden.items():
        faelle = {k: {"mail": mails[k], "antwort": {"message": {"content": a["inhalt"]}}} for k, a in antworten.items()}
        spalten[wer] = kennzahlen(gold, mails, antworten, pipeline("pruefen", {"faelle": faelle, "bestellungen": bestellungen}))
    namen = list(next(iter(spalten.values())))
    zeilen = [f"# Modellvergleich auf `{satz}`", "",
              "Gleicher Prompt, gleiches JSON-Schema, gleiche Prüfregeln. Alle Mails sind synthetisch.", "",
              "| Kennzahl | " + " | ".join(spalten) + " |", "|---|" + "---|" * len(spalten),
              *(f"| {z} | " + " | ".join(s[z] for s in spalten.values()) + " |" for z in namen)]
    if any(len(a) < len(gold) for a in vorhanden.values()):
        zeilen += ["", f"**Unvollständig:** Nicht jedes Modell hat alle {len(gold)} Mails beantwortet, die Spalten sind nicht vergleichbar."]
    ziel = REPO / "eval" / f"modellvergleich_{satz}.md"
    ziel.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    print("\n".join(zeilen))
    print(f"\n→ {ziel.relative_to(REPO)}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("modell", choices=[*MODELLE, "bericht"])
    parser.add_argument("--set", default="pruefset4", help="Ordner mit mails/ und gold.json")
    parser.add_argument("--limit", type=int, help="nur so viele offene Mails messen (Probelauf)")
    args = parser.parse_args()
    try:
        if args.modell != "bericht":
            messen(args.modell, args.set, args.limit)
        bericht(args.set)
    except Abbruch as fehler:
        print(f"Abgebrochen: {fehler}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
