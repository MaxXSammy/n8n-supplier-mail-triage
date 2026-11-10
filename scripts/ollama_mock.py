"""Ersatz für Ollama: zeichnet echte Antworten auf und spielt sie wieder ab, damit Tests ohne Sprachmodell laufen.

    python scripts/ollama_mock.py aufnehmen     # leitet an das echte Ollama weiter und speichert jede Antwort
    python scripts/ollama_mock.py abspielen     # antwortet nur aus der Aufnahme, in Millisekunden

Der Server lauscht auf Port 11435. n8n zeigt so darauf (nur für diesen Start, die .env bleibt unverändert):

    OLLAMA_BASE_URL=http://host.docker.internal:11435 docker compose up -d     # Windows PowerShell: $env:OLLAMA_BASE_URL="..."; docker compose up -d

Schlüssel einer Antwort ist der Hash aus Prompt und Mail. Die Message-ID gehört nicht dazu, Wiederholungsläufe treffen
also dieselbe Aufnahme. Ändert sich der Prompt, passt keine Aufnahme mehr: Der Mock antwortet dann mit Fehler 500,
der Workflow legt die Mail mit "llm_fehler" in die Review-Queue, und man sieht sofort, dass neu aufgenommen werden muss.
Die Aufnahme liegt in tests/mocks/ollama_antworten.json.
"""
import hashlib
import json
import sys
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUFNAHME = REPO / "tests" / "mocks" / "ollama_antworten.json"
ECHTES_OLLAMA = "http://localhost:11434"
PORT = 11435
sperre = threading.Lock()


def schluessel(anfrage: dict) -> str:
    """Hash über Modell und Nachrichten (System-Prompt und Mail). Schema und Optionen stecken im Prompt-Stand."""
    inhalt = json.dumps({"model": anfrage.get("model"), "messages": anfrage.get("messages")}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(inhalt.encode("utf-8")).hexdigest()


def laden() -> dict:
    return json.loads(AUFNAHME.read_text(encoding="utf-8")) if AUFNAHME.exists() else {}


class Mock(BaseHTTPRequestHandler):
    modus = "abspielen"
    antworten: dict = {}

    def antworten_mit(self, status: int, daten: dict) -> None:
        roh = json.dumps(daten, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(roh)))
        self.end_headers()
        self.wfile.write(roh)

    def do_GET(self) -> None:  # noqa: N802 – Name von http.server vorgegeben
        # /api/tags beantworten, damit Startskripte und Healthchecks den Mock wie Ollama sehen
        self.antworten_mit(200, {"models": [{"name": "mock"}], "modus": self.modus, "aufnahmen": len(self.antworten)})

    def do_POST(self) -> None:  # noqa: N802
        anfrage = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or "{}")
        k = schluessel(anfrage)
        if self.modus == "abspielen":
            if k in self.antworten:
                self.antworten_mit(200, self.antworten[k])
            else:
                self.antworten_mit(500, {"error": f"keine Aufnahme für {k[:12]}, neu aufnehmen"})
            return
        weiter = urllib.request.Request(ECHTES_OLLAMA + self.path, data=json.dumps(anfrage).encode("utf-8"),
                                        headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(weiter, timeout=300) as antwort:
            daten = json.loads(antwort.read())
        with sperre:
            self.antworten[k] = daten
            AUFNAHME.parent.mkdir(parents=True, exist_ok=True)
            AUFNAHME.write_text(json.dumps(self.antworten, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        self.antworten_mit(200, daten)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        sys.stdout.write(f"[{self.modus}] {format % args}\n")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2 or sys.argv[1] not in ("aufnehmen", "abspielen"):
        raise SystemExit(__doc__)
    Mock.modus = sys.argv[1]
    Mock.antworten = laden()
    print(f"Ollama-Mock ({Mock.modus}) auf Port {PORT}, {len(Mock.antworten)} Aufnahmen in {AUFNAHME.relative_to(REPO)}")
    # Nur localhost: Docker Desktop leitet host.docker.internal auf den Rechner weiter (wie bei Ollama selbst)
    ThreadingHTTPServer(("127.0.0.1", PORT), Mock).serve_forever()


if __name__ == "__main__":
    main()
