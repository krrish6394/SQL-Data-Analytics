#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

PORT=${NEWS_AGG_PORT:-5001}

echo "Starting News Aggregator on port $PORT..."
# Start the app in background
NEWS_AGG_PORT=$PORT python app.py &
APP_PID=$!

cleanup() {
  echo "Stopping app (pid=$APP_PID)"
  kill "$APP_PID" || true
}
trap cleanup EXIT

# Wait for health endpoint
echo "Waiting for health endpoint..."
for i in {1..20}; do
  if curl -sS "http://127.0.0.1:$PORT/api/health" >/dev/null 2>&1; then
    echo "Health check passed"
    break
  fi
  sleep 1
done

echo "Running integration checks..."

HEALTH=$(curl -sS "http://127.0.0.1:$PORT/api/health") || { echo "Health request failed"; exit 2; }
echo "HEALTH: $HEALTH"

CATS=$(curl -sS "http://127.0.0.1:$PORT/api/categories") || { echo "Categories request failed"; exit 3; }
echo "CATEGORIES: $CATS"

SUMM=$(curl -sS -X POST -H "Content-Type: application/json" -d '{"content":"Docker integration test. Summarize this text.", "num_sentences":1}' "http://127.0.0.1:$PORT/api/summarize") || { echo "Summarize request failed"; exit 4; }
echo "SUMMARIZE: $SUMM"

echo "Integration tests passed"
exit 0
