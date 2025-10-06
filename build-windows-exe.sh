#!/bin/bash

echo "🚀 Docker를 사용한 Windows EXE 빌드"
echo "=================================="

# Docker 이미지 빌드
echo "📦 Windows 빌드 환경 준비 중..."
docker build -f Dockerfile.windows -t yt-downloader-windows .

if [ $? -eq 0 ]; then
    echo "✅ Docker 이미지 빌드 완료"
    
    # 컨테이너 실행하여 EXE 빌드
    echo "🏗️  EXE 파일 빌드 중..."
    docker run --rm -v "$(pwd)/dist:/app/dist" yt-downloader-windows
    
    if [ -f "dist/YouTube_Downloader.exe" ]; then
        echo "✅ EXE 빌드 성공!"
        echo "📁 파일 위치: dist/YouTube_Downloader.exe"
        ls -la dist/YouTube_Downloader.exe
    else
        echo "❌ EXE 빌드 실패"
    fi
else
    echo "❌ Docker 이미지 빌드 실패"
fi