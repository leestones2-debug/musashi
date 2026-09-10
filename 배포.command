#!/bin/bash
cd "$(dirname "$0")"
echo "▶ GitHub Pages (미리보기) 배포…"
bash /Users/apple/glow-multi/scripts/deploy-musashi-github-pages.sh
echo ""
echo "▶ musashi634.co.kr 도메인 배포…"
if bash /Users/apple/glow-multi/scripts/deploy-musashi634-domain.sh; then
  echo "  도메인 배포 OK"
else
  echo "  ⚠ 도메인 배포 실패 — leestones2-debug SSH 키 확인"
  echo "    scripts/keys/musashi-deploy"
fi
read -n 1 -s -r -p "Enter로 종료..."
