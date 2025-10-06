# 🚀 EXE 파일 빌드 가이드

YouTube 다운로더를 실행 파일(.exe)로 변환하는 방법을 안내합니다.

## 📋 사전 준비사항

### 1. 필수 소프트웨어
- **Python 3.8 이상** (https://python.org)
- **FFmpeg** (https://ffmpeg.org)
- **Git** (https://git-scm.com) - 선택사항

### 2. FFmpeg 설치 확인
```bash
# Windows (Chocolatey)
choco install ffmpeg

# Windows (Scoop)
scoop install ffmpeg

# 설치 확인
ffmpeg -version
```

## 🔧 빌드 방법

### 방법 1: 자동 빌드 (권장)

**Windows:**
```bash
# 1. 저장소 클론
git clone https://github.com/jpjp92/yt_downloader.git
cd yt_downloader

# 2. 배치 파일 실행
build_exe.bat
```

**Linux/macOS:**
```bash
# 1. 저장소 클론
git clone https://github.com/jpjp92/yt_downloader.git
cd yt_downloader

# 2. 의존성 설치
pip install -r requirements-dev.txt

# 3. 빌드 실행
python build_exe.py
```

### 방법 2: 수동 빌드

```bash
# 1. PyInstaller 설치
pip install pyinstaller

# 2. 기본 빌드
pyinstaller --onefile --name "YouTube_Downloader" main.py

# 3. 고급 빌드 (spec 파일 사용)
pyinstaller youtube_downloader.spec
```

### 방법 3: GUI 빌드 도구

```bash
# auto-py-to-exe 설치
pip install auto-py-to-exe

# GUI 도구 실행
auto-py-to-exe
```

## 📁 빌드 결과

빌드 성공 시 다음 구조가 생성됩니다:

```
yt_downloader/
├── dist/
│   └── YouTube_Downloader.exe  # 📦 최종 실행 파일
├── build/                      # 🔧 임시 빌드 파일
└── main.py                     # 🚀 런처 파일
```

## ⚡ 실행 파일 사용법

### 방법 1: Windows에서 빌드 및 실행 (권장)

**1. Windows PowerShell 또는 명령 프롬프트에서:**
```powershell
# 1. 저장소 클론
git clone https://github.com/jpjp92/yt_downloader.git
cd yt_downloader

# 2. Python 패키지 설치
pip install pyinstaller streamlit yt-dlp ffmpeg-python

# 3. 빌드 실행
pyinstaller --onefile --windowed --name YouTube_Downloader main.py

# 4. 실행
.\dist\YouTube_Downloader.exe
```

### 방법 2: 직접 Python 실행 (개발/테스트용)

**빌드하지 않고 바로 실행:**
```bash
# 1. 의존성 설치
pip install streamlit yt-dlp ffmpeg-python

# 2. Streamlit 직접 실행
streamlit run app.py

# 3. 브라우저에서 http://localhost:8501 접속
```

### 방법 3: Linux/macOS에서 실행

**1. 실행 파일 빌드:**
```bash
# PyInstaller로 빌드
pyinstaller --onefile --console --name YouTube_Downloader main.py

# 실행 권한 부여
chmod +x dist/YouTube_Downloader

# 실행
./dist/YouTube_Downloader
```

**2. 직접 Python 실행:**
```bash
# Streamlit 실행
python -m streamlit run app.py --server.port 8501
```

### 🎯 실제 권장 실행 방법

**현재 상황에서 가장 쉬운 방법:**

**Windows 사용자:**
```powershell
# 1. 저장소 이동
cd yt_downloader

# 2. 직접 실행 (빌드 없이)
python -m streamlit run app.py

# 3. 자동으로 브라우저가 열림 (http://localhost:8501)
```

**WSL/Linux 사용자:**
```bash
# 1. 저장소 이동
cd yt_downloader

# 2. 직접 실행
streamlit run app.py

# 3. 브라우저에서 http://localhost:8501 접속
```

**💡 참고:** EXE 빌드는 배포용이며, 개발/개인 사용시에는 직접 Python 실행이 더 안정적입니다.
```bash
# 필요한 파일들만 복사
mkdir YouTube_Downloader_Portable
copy dist\YouTube_Downloader.exe YouTube_Downloader_Portable\
copy README.md YouTube_Downloader_Portable\

# ZIP 파일로 압축
tar -czf YouTube_Downloader_v1.0.zip YouTube_Downloader_Portable\
```

## 🔧 빌드 옵션 설명

### 기본 옵션
- `--onefile`: 단일 실행 파일 생성
- `--windowed`: 콘솔 창 숨기기
- `--name`: 실행 파일 이름 지정

### 고급 옵션
- `--icon=icon.ico`: 아이콘 설정
- `--add-data`: 추가 데이터 파일 포함
- `--hidden-import`: 숨겨진 모듈 포함
- `--upx-dir`: UPX 압축 사용

### 최적화 옵션
```bash
# 크기 최소화
pyinstaller --onefile --strip --upx-dir=C:\upx main.py

# 시작 속도 향상
pyinstaller --onedir main.py
```

## 📊 예상 파일 크기

| 빌드 타입 | 파일 크기 | 시작 속도 |
|-----------|-----------|-----------|
| 기본 onefile | ~80-120MB | 느림 |
| UPX 압축 | ~60-90MB | 느림 |
| onedir | ~200-300MB | 빠름 |

## ❗ 주의사항

### 1. 안티바이러스 오탐
- PyInstaller로 생성된 exe는 일부 안티바이러스에서 오탐될 수 있습니다
- Windows Defender 예외 추가 필요할 수 있음

### 2. FFmpeg 의존성
- 시스템에 FFmpeg가 설치되어 있어야 합니다
- 또는 FFmpeg.exe를 실행 파일에 포함시켜야 합니다

### 3. 포터블 버전
```bash
# FFmpeg 포함 포터블 버전
pyinstaller --onefile --add-binary "C:\ffmpeg\bin\ffmpeg.exe;ffmpeg" main.py
```

## 🐛 문제 해결

### 모듈을 찾을 수 없음
```bash
# 숨겨진 import 추가
pyinstaller --hidden-import=모듈명 main.py
```

### 파일 크기가 너무 큼
```bash
# 불필요한 모듈 제외
pyinstaller --exclude-module=matplotlib --exclude-module=numpy main.py
```

### 실행 시 오류
```bash
# 디버그 모드로 빌드
pyinstaller --debug=all main.py
```

## � Linux 환경에서 실행 파일 만들기

### ❌ Linux에서 .exe 파일은 직접 만들 수 없습니다!

**하지만 다음과 같은 대안들이 있습니다:**

### 1. **Native Linux 실행 파일 생성 (권장)**

```bash
# Linux/WSL에서
pyinstaller --onefile --console --name YouTube_Downloader main.py

# 결과: dist/YouTube_Downloader (리눅스 실행 파일)
# 실행: ./dist/YouTube_Downloader
```

**장점:**
- ✅ 빠른 빌드 (5-10분)
- ✅ 작은 파일 크기 (~24MB)
- ✅ Linux/WSL에서 바로 실행 가능

### 2. **Wine을 사용한 Windows .exe 빌드**

```bash
# Wine 설치 (Ubuntu/Debian)
sudo apt update
sudo apt install wine winetricks

# Windows Python 설치 (Wine 환경)
winetricks python3

# PyInstaller 설치 및 빌드
wine pip install pyinstaller
wine pyinstaller --onefile --windowed --name YouTube_Downloader.exe main.py
```

**주의:** 복잡하고 불안정할 수 있음

### 3. **Docker를 사용한 크로스 컴파일**

```bash
# Windows 컨테이너 사용
docker run --rm -v $(pwd):/app -w /app \
  python:3.11-windowsservercore \
  powershell -c "pip install pyinstaller streamlit yt-dlp; pyinstaller --onefile main.py"
```

### 4. **GitHub Actions로 자동 빌드**

`.github/workflows/build.yml` 파일 생성:

```yaml
name: Build Executables
on: [push]
jobs:
  build:
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: pip install -r requirements-dev.txt
    - run: pyinstaller --onefile --name YouTube_Downloader main.py
    - uses: actions/upload-artifact@v3
      with:
        name: YouTube_Downloader-${{ matrix.os }}
        path: dist/
```

### 🎯 **권장 방법별 용도**

| 방법 | 용도 | 난이도 | 결과 |
|------|------|--------|------|
| **Native Linux** | WSL, Ubuntu 사용자 | ⭐ 쉬움 | 24MB Linux 실행 파일 |
| **GitHub Actions** | 배포용 자동화 | ⭐⭐ 보통 | 모든 OS용 파일 |
| **Wine** | Windows .exe 필요시 | ⭐⭐⭐ 어려움 | .exe (불안정) |
| **가상 머신** | 확실한 .exe 필요시 | ⭐⭐⭐⭐ 매우 어려움 | 완벽한 .exe |

### ✅ **현재 생성된 파일**

```bash
# 생성된 Linux 실행 파일
dist/YouTube_Downloader    # 24MB ELF 64-bit 실행 파일

# 실행 방법
./dist/YouTube_Downloader

# 또는 다른 Linux 시스템에 복사하여 실행
chmod +x YouTube_Downloader
./YouTube_Downloader
```

## 🎯 Windows .exe 파일 생성 구성

### 방법 1: **GitHub Actions 자동 빌드** (가장 쉬움)

**설정 완료!** `.github/workflows/build-executables.yml` 파일이 생성되었습니다.

```bash
# 1. GitHub에 푸시
git add .
git commit -m "Add automated build workflow"
git push

# 2. GitHub Actions에서 자동으로 다음 파일들 생성:
# - YouTube_Downloader_Windows.exe (Windows)
# - YouTube_Downloader_Linux (Linux)  
# - YouTube_Downloader_macOS (macOS)
```

**사용법:**
1. 코드를 GitHub에 푸시하면 자동으로 빌드
2. Actions 탭에서 빌드 진행상황 확인
3. Artifacts에서 각 OS별 실행 파일 다운로드

### 방법 2: **Docker로 Windows 빌드**

```bash
# Docker로 Windows EXE 빌드 (설정 완료!)
./build-windows-exe.sh

# 또는 수동으로:
docker build -f Dockerfile.windows -t yt-downloader-windows .
docker run --rm -v "$(pwd)/dist:/app/dist" yt-downloader-windows
```

### 방법 3: **Windows 환경에서 직접 빌드**

**Windows PowerShell에서:**
```powershell
# 1. 저장소 클론 (Windows에서)
git clone https://github.com/jpjp92/yt_downloader.git
cd yt_downloader

# 2. 자동 빌드
.\build_exe.bat

# 결과: dist\YouTube_Downloader.exe
```

```bash
# VirtualBox + Windows 10/11
# 1. Windows VM 생성
# 2. Python 설치
# 3. 프로젝트 복사
# 4. PyInstaller 빌드
pyinstaller --onefile --windowed --name YouTube_Downloader main.py
```

- [PyInstaller 공식 문서](https://pyinstaller.readthedocs.io/)
- [auto-py-to-exe 가이드](https://github.com/brentvollebregt/auto-py-to-exe)
- [FFmpeg 다운로드](https://ffmpeg.org/download.html)