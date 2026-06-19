#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found."
  echo "Install it from https://www.python.org/downloads/ then run this again."
  read -n1 -r -p "Press any key to close..."
  exit 1
fi
python3 vUSAlink.py
