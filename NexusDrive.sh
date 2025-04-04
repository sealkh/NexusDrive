#!/bin/bash
# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found in PATH"
    exit 1
fi

# Configure paths
PY_MAIN="NexusDrive.py"
VENV_DIR="venv"

# Create virtual environment if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "Installing required packages..."
pip install -r requirements.txt --quiet --disable-pip-version-check

# Launch application
echo
echo "===== Starting Application ====="
python3 "$PY_MAIN"