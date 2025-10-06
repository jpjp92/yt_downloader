@echo off
echo ==========================================
echo    YouTube 다운로더 EXE 빌드 도구
echo ==========================================
echo.

echo [1/3] Python 환경 확인 중...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았습니다.
    echo https://python.org 에서 Python을 설치하세요.
    pause
    exit /b 1
)

echo.
echo [2/3] 필요한 패키지 설치 중...
pip install pyinstaller
pip install -r requirements.txt

echo.
echo [3/3] EXE 파일 빌드 시작...
python build_exe.py

echo.
echo ==========================================
echo 빌드 완료! dist 폴더를 확인하세요.
echo ==========================================
pause