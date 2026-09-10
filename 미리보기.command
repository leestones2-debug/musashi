#!/bin/bash
cd "$(dirname "$0")"
PORT=8765
if ! lsof -i :$PORT >/dev/null 2>&1; then
  python3 -m http.server $PORT >/dev/null 2>&1 &
  sleep 0.5
fi
open -a "Google Chrome" --new "http://127.0.0.1:$PORT/index.html"
echo "미리보기: http://127.0.0.1:$PORT/index.html"
