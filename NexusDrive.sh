#!/bin/bash

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 not found in PATH"
    exit 1
fi

PY_MAIN="NexusDrive.py"
VENV_DIR="venv"

# Create virtual environment if missing
if [ ! -d "$VENV_DIR/bin" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR" || exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate" || exit 1

# Install pipreqs if needed
if ! pip show pipreqs &> /dev/null; then
    echo "Installing pipreqs..."
    pip install pipreqs --quiet --disable-pip-version-check
fi

# Generate requirements.txt
echo "Analyzing project dependencies..."
pipreqs ./ --force || {
    echo "[ERROR] pipreqs failed"
    exit 1
}

# Install dependencies
echo "Installing required packages..."
pip install -r requirements.txt --quiet --disable-pip-version-check || exit 1

# Launch application
echo
echo "===== Starting Application ====="
python "$PY_MAIN"
