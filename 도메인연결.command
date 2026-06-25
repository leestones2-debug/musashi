#!/bin/bash
# musashi634.co.kr — GitHub 저장소 생성 + 배포 (더블클릭)
cd "$(dirname "$0")"
osascript -e 'display notification "GitHub에서 musashi 저장소 생성 창이 열립니다" with title "MUSASHI 도메인 연결"'
bash /Users/apple/glow-multi/scripts/create-and-deploy-musashi.sh
echo ""
read -r -p "완료. Enter 키로 닫기…" _
