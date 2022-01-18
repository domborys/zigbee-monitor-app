#!/bin/bash
source ./venv/bin/activate
python3 make_admin.py "$1" "$2"
deactivate