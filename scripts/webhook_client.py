"""Gemeinsame Helfer: .env lesen und eine Mail an den n8n-Webhook schicken (nur Standardbibliothek)."""
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STANDARD_URL = "http://localhost:5678/webhook/lieferanten-mail"


def env_lesen(pfad: Path = REPO / ".env") -> dict[str, str]:
    werte = {}
    if pfad.exists():
        for zeile in pfad.read_text(encoding="utf-8").splitlines():
            zeile = zeile.strip()
            if zeile and not zeile.startswith("#") and "=" in zeile:
                schluessel, wert = zeile.split("=", 1)
                werte[schluessel.strip()] = wert.strip()
    return werte


def mail_senden(mail: dict, url: str, token: str, timeout: float = 300) -> tuple[int, dict, float]:
    """Schickt eine Mail an den Webhook. Gibt (HTTP-Status, Antwort, Sekunden) zurück."""
    anfrage = urllib.request.Request(
        url,
        data=json.dumps(mail).encode("utf-8"),
        headers={"Content-Type": "application/json", "X-Webhook-Token": token},
        method="POST",
    )
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(anfrage, timeout=timeout) as antwort:
            status, inhalt = antwort.status, antwort.read()
    except urllib.error.HTTPError as fehler:
        status, inhalt = fehler.code, fehler.read()
    dauer = time.perf_counter() - start
    try:
        daten = json.loads(inhalt.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        daten = {"roh": inhalt.decode("utf-8", errors="replace")}
    return status, daten, dauer
