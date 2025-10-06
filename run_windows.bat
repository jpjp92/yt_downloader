@echo off
echo 🎥 YouTube 다운로더 시작 중...
echo 📍 브라우저에서 http://localhost:8501 접속하세요
echo.

REM Python과 pip이 설치되어 있는지 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo Python을 설치하고 다시 실행하세요.
    pause
    exit /b 1
)

REM 필요한 패키지 설치
echo 📦 필요한 패키지 설치 중...
pip install streamlit yt-dlp ffmpeg-python

REM Streamlit 실행
echo 🚀 YouTube 다운로더 실행...
streamlit run app.py --server.port 8501

echo.
echo 🏁 YouTube 다운로더가 종료되었습니다.
pause