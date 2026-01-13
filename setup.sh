#!/bin/bash

echo "[+] Initializing NetSentry-Pro Environment..."

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 could not be found"
    exit 1
fi

# Create virtual env
if [ ! -d "venv" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[.] Virtual environment exists."
fi

# Activate and install
source venv/bin/activate
echo "[+] Installing dependencies..."
pip install -r requirements.txt

# Create log dir
mkdir -p logs

echo "[+] Setup complete. Run: sudo python3 src/main.py --help"
