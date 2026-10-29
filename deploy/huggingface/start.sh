#!/bin/sh
# Start the local model server inside the container, wait for it, then start Vaultwise.
set -e
ollama serve > /tmp/ollama.log 2>&1 &
for i in $(seq 1 90); do
  curl -sf http://127.0.0.1:11434/api/tags > /dev/null && break
  sleep 1
done
curl -sf http://127.0.0.1:11434/api/tags > /dev/null || { echo "Ollama did not start"; cat /tmp/ollama.log; exit 1; }
echo "Ollama ready; starting Vaultwise on port ${PORT:-7860}"
exec python3 -m uvicorn vaultwise.api:app --app-dir src --host 0.0.0.0 --port "${PORT:-7860}"
