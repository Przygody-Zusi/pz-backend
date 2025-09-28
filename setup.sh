#!/bin/bash
set -e

if ! command -v python3 &> /dev/null; then
    echo "Python3 not installed -> https://www.python.org/downloads/"
    exit 1
fi

echo "Create virtual env"
python3 -m venv .venv

echo "Activate .venv"
source .venv/bin/activate

echo "Update pip"
pip install --upgrade pip

if [ ! -f requirements.txt ]; then
    echo "\"requirements.txt\" does not exist!"
    exit 1
fi

echo "Install python dependencies..."
pip install -r requirements.txt

echo "Install pre-commit..."
pip install pre-commit

echo "Register git hooks..."
pre-commit install

echo "Done"
