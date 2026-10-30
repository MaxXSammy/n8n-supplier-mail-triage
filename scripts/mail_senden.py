"""Schickt eine oder mehrere Beispiel-Mails an den Workflow und zeigt die Antwort.

    python scripts/mail_senden.py mails/07_lieferverzug_rheinwerk.json
    python scripts/mail_senden.py mails/*.json --neu      # neue Message-ID, damit keine Duplikat-Erkennung greift
"""
import argparse
import glob
import json
import sys
import uuid
from pathlib import Path

from webhook_client import STANDARD_URL, env_lesen, mail_senden


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows-Konsole: ✓ und Umlaute
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dateien", nargs="+")
    parser.add_argument("--url", default=STANDARD_URL)
    parser.add_argument("--neu", action="store_true", help="Message-ID um eine Zufallskennung ergänzen")
    args = parser.parse_args()

    token = env_lesen().get("WEBHOOK_TOKEN", "")
    # Windows-Shells expandieren * nicht selbst
    dateien = [d for muster in args.dateien for d in sorted(glob.glob(muster))]
    for datei in dateien:
        mail = json.loads(Path(datei).read_text(encoding="utf-8"))
        if args.neu:
            mail["message_id"] = mail["message_id"].replace(">", f"-{uuid.uuid4().hex[:8]}>")
        status, antwort, dauer = mail_senden(mail, args.url, token)
        print(f"\n{Path(datei).name}  →  HTTP {status} in {dauer:.1f} s")
        print(json.dumps(antwort, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
