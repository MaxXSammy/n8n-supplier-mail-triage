#!/bin/sh
# Läuft im Container n8n-import vor jedem Start von n8n.
# Setzt die Geheimnisse (Docker-Secrets unter /run/secrets) in die Credential-Vorlage ein, importiert
# Zugangsdaten und Workflows und veröffentlicht die Workflows, damit Webhooks und Formular sofort erreichbar sind.
# Hinweis: Die Geheimnisse dürfen die Zeichen | & \ und " nicht enthalten (sed-Ersetzung, JSON).
set -e

POSTGRES_PASSWORD=$(cat /run/secrets/postgres_password)
WEBHOOK_TOKEN=$(cat /run/secrets/webhook_token)
REVIEW_PASSWORD=$(cat /run/secrets/review_password)

sed \
  -e "s|\${POSTGRES_USER}|${POSTGRES_USER}|g" \
  -e "s|\${POSTGRES_PASSWORD}|${POSTGRES_PASSWORD}|g" \
  -e "s|\${WEBHOOK_TOKEN}|${WEBHOOK_TOKEN}|g" \
  -e "s|\${REVIEW_USER}|${REVIEW_USER}|g" \
  -e "s|\${REVIEW_PASSWORD}|${REVIEW_PASSWORD}|g" \
  /credentials/credentials.template.json > /tmp/credentials.json

n8n import:credentials --input=/tmp/credentials.json
rm /tmp/credentials.json

n8n import:workflow --separate --input=/workflows

for datei in /workflows/*.json; do
  id=$(node -e "console.log(require(process.argv[1]).id)" "$datei")
  n8n publish:workflow --id="$id"
done
