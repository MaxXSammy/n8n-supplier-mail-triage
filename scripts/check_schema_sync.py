"""Prüft, dass das JSON-Schema im Workflow (Node "Prompt bauen") mit schema/mail_extraktion.schema.json übereinstimmt.

n8n-Code-Nodes können keine Dateien lesen, deshalb steht das Schema als Kopie im Workflow.
Dieses Skript verhindert, dass die beiden Fassungen unbemerkt auseinanderlaufen.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def main() -> int:
    datei = json.loads((REPO / "schema" / "mail_extraktion.schema.json").read_text(encoding="utf-8"))
    erwartet = {k: v for k, v in datei.items() if k not in ("$schema", "title", "description")}

    workflow = json.loads((REPO / "workflows" / "01_mail_triage.json").read_text(encoding="utf-8"))
    code = next(n for n in workflow["nodes"] if n["name"] == "Prompt bauen")["parameters"]["jsCode"]
    treffer = re.search(r"const SCHEMA = (\{.*?\n\});", code, re.DOTALL)
    if not treffer:
        print('SCHEMA-Konstante im Node "Prompt bauen" nicht gefunden')
        return 1
    if json.loads(treffer.group(1)) != erwartet:
        print("Schema im Workflow weicht von schema/mail_extraktion.schema.json ab")
        return 1
    print("Schema synchron")
    return 0


if __name__ == "__main__":
    sys.exit(main())
