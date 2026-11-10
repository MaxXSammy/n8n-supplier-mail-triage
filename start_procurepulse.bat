@echo off
rem ProcurePulse starten (Windows): Docker und Ollama pruefen, Container starten, Arbeitsliste im Browser oeffnen.
rem Als Desktop-Verknuepfung mit eigenem Symbol: siehe README, Abschnitt "Starten per Doppelklick".
setlocal
cd /d "%~dp0"
title ProcurePulse

docker info >nul 2>&1
if errorlevel 1 (
  echo Docker Desktop wird gestartet ...
  start "" "%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
  for /l %%i in (1,1,60) do (
    docker info >nul 2>&1 && goto docker_bereit
    timeout /t 3 /nobreak >nul
  )
  echo Docker Desktop antwortet nicht. Bitte Docker Desktop von Hand starten.
  pause
  exit /b 1
)
:docker_bereit

curl -s -o nul http://localhost:11434/api/tags
if errorlevel 1 (
  echo Ollama wird gestartet ...
  start "" /min ollama serve
)

docker compose up -d
if errorlevel 1 (
  echo Die Container liessen sich nicht starten. Details: docker compose logs
  pause
  exit /b 1
)

echo Warte auf n8n ...
for /l %%i in (1,1,60) do (
  curl -s http://localhost:5678/healthz | find "ok" >nul && goto n8n_bereit
  timeout /t 2 /nobreak >nul
)
echo n8n antwortet nicht. Details: docker compose logs n8n
pause
exit /b 1

:n8n_bereit
start "" "http://localhost:5678/webhook/arbeitsliste"
endlocal
