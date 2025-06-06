#!/bin/bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "Virtual environment ready."

