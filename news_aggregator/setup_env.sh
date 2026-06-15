#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "Setting up environment for News Aggregator..."

if command -v conda >/dev/null 2>&1; then
  echo "Conda detected — creating 'newsagg' environment with recommended packages (includes scikit-learn, numpy)."
  conda create -n newsagg python=3.11 -y || true
  echo "To activate and install full requirements run:"
  echo "  conda activate newsagg"
  echo "  pip install -r requirements.txt"
  exit 0
fi

PYTHON_3_10_CANDIDATE="/opt/homebrew/anaconda3/envs/tfseq/bin/python"

if [ -d ".venv" ]; then
  VENV_PY=".venv/bin/python"
  if [ -x "$VENV_PY" ] && "$VENV_PY" -V 2>/dev/null | grep -q "Python 3.10"; then
    echo "Using existing Python 3.10 .venv virtualenv"
  else
    echo "Existing .venv is not Python 3.10, recreating it with Python 3.10..."
    rm -rf .venv
  fi
fi

if [ ! -d ".venv" ]; then
  echo "Creating virtualenv .venv with Python 3.10"
  if [ -x "$PYTHON_3_10_CANDIDATE" ]; then
    "$PYTHON_3_10_CANDIDATE" -m venv .venv
  elif command -v python3.10 >/dev/null 2>&1; then
    python3.10 -m venv .venv
  else
    echo "ERROR: Python 3.10 interpreter not found. Please install Python 3.10 or use conda env with Python 3.10."
    exit 1
  fi
fi

echo "Activating .venv and installing runtime dependencies (Flask, nltk, requests)."
. .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install Flask==2.3.0 nltk==3.8.1 requests==2.31.0 python-dotenv==1.0.0 urllib3==2.0.0

echo "Note: scikit-learn, numpy, gensim and other compiled packages are intentionally omitted here.
If you require them, use conda or install platform-specific wheels."

echo "Setup complete. To run the app:"
echo "  . .venv/bin/activate"
echo "  python app.py"
