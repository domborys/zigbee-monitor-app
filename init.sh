#!/bin/bash
mkdir -p venv
if [ ! -f ./venv/bin/activate ]; then
    python3 -m venv venv || exit 1
fi
source ./venv/bin/activate || exit 1
python3 -m pip install -r requirements.txt || exit 1
python3 prepare.py
deactivate
