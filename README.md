# 🎥 YouTube 다운로더

**로컬 환경 최적화 버전** - 고품질 다운로드 및 빠른 변환 지원

YouTube 동영상을 MP4, MP3 형식으로 다운로드하고, 선택적으로 MPEG 형식으로 변환할 수 있는 Streamlit 웹 애플리케이션입니다.

## ✨ 주요 기능

### 📥 고품질 다운로드
- **비디오**: 최대 1080p HD 해상도, H.264 코덱
- **오디오**: 최대 320kbps MP3 고음질
- **성능 최적화**: 동시 8개 청크 다운로드로 2-3배 빠른 속도
- **품질 선택**: 고품질/표준 품질 모드 선택 가능

### 🚀 로컬 환경 최적화
- **빠른 다운로드 모드**: 멀티스레드 동시 다운로드
- **고품질 모드**: 최상의 화질/음질 우선
- **네트워크 최적화**: 재시도 및 타임아웃 설정
- **메모리 효율성**: 청크 단위 스트리밍 다운로드

## 🏠 설치 및 실행

### 1. 필수 요구사항
- **Python 3.8 이상**
- **FFmpeg** (오디오 변환 및 MPEG 변환에 필요)

### 2. FFmpeg 설치
**Windows:**
```powershell
# Chocolatey 사용
choco install ffmpeg

# 또는 Scoop 사용  
scoop install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux/WSL:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 3. 프로젝트 설치
```bash
git clone https://github.com/jpjp92/yt_downloader.git
cd yt_downloader
pip install -r requirements.txt
```

### 4. 실행
```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하세요.

## 📦 EXE 파일로 변환

### 간편 설치 및 빌드
```bash
# Windows 사용자
build_exe.bat

# Linux/macOS 사용자  
python build_exe.py
```

### 수동 빌드
```bash
pip install pyinstaller
pyinstaller --onefile --name "YouTube_Downloader" main.py
```

자세한 내용은 [BUILD_GUIDE.md](BUILD_GUIDE.md)를 참고하세요.

## ✨ 주요 기능

### 📥 다운로드
- **비디오 다운로드 (MP4)**: 최대 1080p 해상도, H.264 코덱 우선
- **오디오 다운로드 (MP3)**: 최대 320kbps 고음질
- **멀티스레드 다운로드**: 동시 5개 청크로 빠른 다운로드
- **최적화된 포맷 선택**: 자동으로 최적의 화질/음질 선택

### 🔄 MPEG 변환 (선택 사항)
- **실시간 진행 상태**: 프로그레스 바로 변환 진행률 확인
- **빠른 변환 모드**: 2-3배 빠른 변환 속도 (기본 활성화)
- **3가지 품질 옵션**:
  - 최소 용량 (낮은 품질): 800kbps 비디오
  - 균형 (중간 품질): 1500kbps 비디오 **(권장)**
  - 고품질 (큰 용량): 3000kbps 비디오
- **해상도 조정**: 1080p → 720p 다운스케일 옵션
- **멀티코어 최적화**: 모든 CPU 코어 활용

### 📊 추가 기능
- 동영상 정보 미리보기 (제목, 채널, 조회수)
- 파일 크기 비교 (원본 vs 변환)
- 다운로드 버튼으로 브라우저에서 즉시 다운로드
- 변환 로그 자동 저장

## 🚀 빠른 시작

### 필수 요구사항

1. **Python 3.8 이상**
2. **FFmpeg** (MPEG 변환 및 오디오 추출에 필요)

#### FFmpeg 설치

**Windows:**
```powershell
# Chocolatey 사용
choco install ffmpeg

# 또는 Scoop 사용
scoop install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**WSL (Windows Subsystem for Linux):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 설치 방법

1. **저장소 클론**
```bash
git clone https://github.com/yourusername/yt_downloader.git
cd yt_downloader
```

2. **의존성 패키지 설치**
```bash
pip install -r requirements.txt
```

3. **애플리케이션 실행**
```bash
streamlit run app.py
```

4. **브라우저에서 열기**
   - 자동으로 브라우저가 열립니다 (기본: `http://localhost:8501`)

## 📖 사용 방법

### 기본 다운로드

1. 사이드바에서 **다운로드 형식** 선택 (비디오 또는 오디오)
2. YouTube URL 입력
3. **다운로드** 버튼 클릭
4. 다운로드 완료 후 **파일 다운로드** 버튼으로 저장

### MPEG 변환

1. 사이드바에서 **MP4 → MPEG 변환** 체크박스 활성화
2. 변환 옵션 설정:
   - ⚡ **빠른 변환 모드**: 속도 우선 (권장)
   - **변환 품질**: 파일 크기와 품질 선택
   - **해상도 줄이기**: 720p로 다운스케일 (선택 사항)
3. 다운로드 후 자동으로 변환 시작
4. 진행 상태를 실시간으로 확인
5. 완료 후 원본과 변환 파일 모두 다운로드 가능

## 📁 프로젝트 구조

```
yt_downloader/
├── app.py              # 메인 애플리케이션
├── requirements.txt    # Python 의존성
├── README.md          # 프로젝트 문서
├── downloads/         # 다운로드된 파일 저장 (자동 생성)
└── logs/              # 변환 로그 저장 (자동 생성)
```

## ⚙️ 기술 스택

- **Streamlit**: 웹 UI 프레임워크
- **yt-dlp**: YouTube 다운로드 엔진
- **FFmpeg**: 비디오/오디오 변환 및 처리
- **Python 3.8+**: 주 프로그래밍 언어

## 🎯 성능 최적화

### 다운로드 속도
- 동시 5개 청크 다운로드
- 10MB 청크 크기로 대용량 파일 최적화
- H.264 코덱 우선 선택으로 빠른 병합

### 변환 속도
- 멀티코어 CPU 활용 (`-threads 0`)
- 빠른 모드: ultrafast 프리셋 사용
- B-프레임 제거로 인코딩 단순화
- GOP 크기 최적화

### 파일 크기
- 비트레이트 제한으로 파일 크기 제어
- 균형 모드: 원본과 비슷한 크기 유지
- 해상도 조정 옵션으로 추가 크기 절감

## 🔧 문제 해결

### FFmpeg 관련 오류
```
❌ FFmpeg가 설치되어 있지 않습니다.
```
**해결**: 위의 FFmpeg 설치 방법을 참고하여 설치

### 다운로드 오류
```
❌ 동영상 정보를 가져올 수 없습니다.
```
**해결**: 
- YouTube URL이 올바른지 확인
- 인터넷 연결 확인
- 비공개 동영상인지 확인

### 변환이 느린 경우
**해결**:
- "⚡ 빠른 변환 모드" 활성화
- "해상도 줄이기" 옵션 사용
- CPU 사용률 확인 (다른 프로그램 종료)

## 📝 라이선스

이 프로젝트는 교육 목적으로만 사용해주세요. 저작권을 존중해주세요.

## 🤝 기여

버그 리포트 및 기능 제안은 Issues를 통해 제출해주세요.

## ⚠️ 주의사항

- YouTube의 이용 약관을 준수해주세요
- 저작권이 있는 콘텐츠는 개인적 용도로만 사용하세요
- 상업적 목적으로 사용하지 마세요
- 다운로드한 콘텐츠의 재배포를 금지합니다

