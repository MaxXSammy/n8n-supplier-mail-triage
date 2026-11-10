#!/usr/bin/env sh
# ProcurePulse starten (macOS, Linux): Container starten, auf n8n warten, Arbeitsliste im Browser öffnen.
set -e
cd "$(dirname "$0")"

if ! docker info >/dev/null 2>&1; then
  echo "Docker läuft nicht. Bitte Docker starten und das Skript erneut ausführen." >&2
  exit 1
fi

if ! curl -s -o /dev/null http://localhost:11434/api/tags; then
  echo "Ollama wird gestartet ..."
  (ollama serve >/dev/null 2>&1 &)
fi

docker compose up -d

printf "Warte auf n8n "
versuche=0
until curl -s http://localhost:5678/healthz | grep -q ok; do
  versuche=$((versuche + 1))
  if [ "$versuche" -gt 60 ]; then
    echo
    echo "n8n antwortet nicht. Details: docker compose logs n8n" >&2
    exit 1
  fi
  printf "."
  sleep 2
done
echo

adresse="http://localhost:5678/webhook/arbeitsliste"
if command -v open >/dev/null 2>&1; then
  open "$adresse"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$adresse"
else
  echo "Arbeitsliste: $adresse"
fi
