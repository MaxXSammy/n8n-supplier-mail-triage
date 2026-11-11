"""Füllt die Arbeitsliste mit Beispielmails für eine Vorführung und räumt sie danach wieder weg.

    python scripts/demo_laden.py             # Beispielmails durch den laufenden Workflow schicken
    python scripts/demo_laden.py --loeschen  # Demo-Tickets, -Reviews und -Entwürfe wieder entfernen

Die Message-IDs der Demo-Mails enden auf "-demo". Nur diese Einträge werden gelöscht.
"""
import argparse
import json
import subprocess
import sys

from webhook_client import REPO, STANDARD_URL, env_lesen, mail_senden

# (Ordner, Datei): AB mit Abweichung, Betrug, Angebot, Preisänderung, Verzug, Reklamation, Rechnung, Werbung und mehr
AUSWAHL = [
    ("mails", "22_ab_kovotech_preis"), ("mails", "27_ab_swissturning_preis_und_termin"), ("mails", "17_ab_brenner_liefertreue_ax"),
    ("mails", "21_ab_nordform_neulieferant"), ("mails", "16_ab_alpen_ok"), ("mails", "14_sonstiges_bankdaten_betrugsversuch"),
    ("mails", "01_angebot_alpen"), ("mails", "07_lieferverzug_rheinwerk"), ("mails", "05_reklamation_feldmann_mit_rechnung"),
    ("mails", "10_rechnung_brenner"), ("pruefset2/mails", "q05_preis_rundschreiben"), ("pruefset2/mails", "q18_kaltakquise"),
    ("pruefset2/mails", "q01_avis_spedition"), ("pruefset2/mails", "q14_iso_zertifikat"), ("pruefset2/mails", "q19_webinar"),
]

LOESCHEN_SQL = """
DELETE FROM entwuerfe WHERE ticket_id IN (SELECT id FROM tickets WHERE mail_id LIKE '%-demo%');
DELETE FROM review_queue WHERE mail_id LIKE '%-demo%';
DELETE FROM tickets WHERE mail_id LIKE '%-demo%';
"""


def loeschen() -> None:
    ergebnis = subprocess.run(
        ["docker", "compose", "exec", "-T", "postgres", "psql", "-U", env_lesen().get("POSTGRES_USER", "n8n"), "-d", "triage"],
        input=LOESCHEN_SQL, text=True, capture_output=True, cwd=REPO)
    print("Demo-Daten gelöscht." if ergebnis.returncode == 0 else f"Löschen fehlgeschlagen: {ergebnis.stderr}")


def laden() -> None:
    token = env_lesen().get("WEBHOOK_TOKEN", "")
    for ordner, name in AUSWAHL:
        mail = json.loads((REPO / ordner / f"{name}.json").read_text(encoding="utf-8"))
        mail["message_id"] = mail["message_id"].replace(">", "-demo>")
        _, antwort, sekunden = mail_senden(mail, STANDARD_URL, token)
        print(f"{name:42} → {antwort.get('status')} ({sekunden:.1f} s)")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--loeschen", action="store_true", help="Demo-Daten entfernen")
    args = parser.parse_args()
    loeschen() if args.loeschen else laden()


if __name__ == "__main__":
    main()
