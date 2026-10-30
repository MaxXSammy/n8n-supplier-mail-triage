"""Holt Änderungen aus der n8n-Oberfläche zurück ins Repo.

    python scripts/export_workflows.py

Exportiert die drei Workflows aus dem laufenden Container und behält nur die portablen Felder.
Zeitstempel, Versions- und Projekt-IDs gehören zur jeweiligen Instanz und würden beim Import stören.
"""
import json
import subprocess
import sys

from check_schema_sync import main as schema_pruefen
from webhook_client import REPO

WORKFLOWS = {
    "mailTriageHaupt1": "01_mail_triage.json",
    "mailTriageReview": "02_review_human_in_the_loop.json",
    "mailTriageFehler": "03_fehlerbehandlung.json",
    "mailTriageEntwrf": "04_antwortentwurf.json",
}
PORTABEL = ["id", "name", "nodes", "connections", "settings", "pinData", "tags"]


def main() -> int:
    for workflow_id, datei in WORKFLOWS.items():
        ausgabe = subprocess.run(
            ["docker", "compose", "exec", "-T", "n8n", "n8n", "export:workflow", f"--id={workflow_id}"],
            cwd=REPO, capture_output=True, text=True, encoding="utf-8", check=True,
        ).stdout
        # Die CLI schreibt vor dem JSON noch Log-Zeilen, deshalb ab der ersten eckigen Klammer lesen
        workflow = json.loads(ausgabe[ausgabe.index("["):])[0]
        bereinigt = {feld: workflow[feld] for feld in PORTABEL}
        bereinigt["active"] = False  # veröffentlicht wird beim Import (scripts/n8n_import.sh)
        (REPO / "workflows" / datei).write_text(
            json.dumps(bereinigt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"exportiert: {datei}")
    return schema_pruefen()


if __name__ == "__main__":
    sys.exit(main())
