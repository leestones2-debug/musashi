#!/bin/bash
cd "$(dirname "$0")"
cp index.html /Users/apple/glow-multi/docs/musashi/index.html
bash /Users/apple/glow-multi/scripts/deploy-musashi-github-pages.sh
read -n 1 -s -r -p "Enter로 종료..."
