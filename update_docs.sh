#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FLARE_DIR="$(cd "$SCRIPT_DIR/../flare" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "=============================================="
echo "      Flare Docs Code-Group Auto-Updater      "
echo "=============================================="
echo "Docs Directory:  $SCRIPT_DIR"
echo "Flare Directory: $FLARE_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in .venv..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "Installing/updating local flare package ($FLARE_DIR)..."
pip install --quiet --editable "$FLARE_DIR"

echo "Updating code-group outputs in documentation markdown files..."
python "$SCRIPT_DIR/update_docs.py" "$@"

echo "=============================================="
echo "Success! Documentation code-groups up to date."
echo "=============================================="
