#!/bin/bash
cd "$(dirname "$0")"
/Users/apple/glow-multi/.venv-barona/bin/python3 scripts/capture-homepage.py
open captures/home
