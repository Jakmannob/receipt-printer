#!/usr/bin/env bash
set -e


echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing project..."
pip install -e .
