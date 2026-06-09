#!/usr/bin/env bash
set -euo pipefail

# Creates a venv in ./venv and installs requirements.txt
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

PYTHON_CMD=python3

if ! command -v "$PYTHON_CMD" &> /dev/null; then
  echo "python3 not found. Please install Python 3 and retry."
  exit 1
fi

if [ -d "venv" ]; then
  echo "venv already exists. To recreate, delete the ./venv folder first."
else
  echo "Creating virtual environment..."
  "$PYTHON_CMD" -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
if [ -f requirements.txt ]; then
  echo "Installing requirements..."
  pip install -r requirements.txt
else
  echo "No requirements.txt found, skipping install."
fi

echo "Virtual environment ready. Activate with: source venv/bin/activate"