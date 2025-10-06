#!/bin/bash
# YouTube 다운로더 실행 스크립트

echo "🎥 YouTube 다운로더 시작 중..."
echo "📍 브라우저에서 http://localhost:8501 접속하세요"
echo ""

# conda 환경 활성화
source ~/miniconda/etc/profile.d/conda.sh
conda activate base

# 현재 디렉토리 확인
cd "$(dirname "$0")"

# Streamlit 실행
streamlit run app.py --server.port 8501 --server.headless true

echo "🏁 YouTube 다운로더가 종료되었습니다."