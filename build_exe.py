"""
YouTube 다운로더 EXE 빌드 스크립트
PyInstaller를 사용하여 실행 파일을 생성합니다.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """EXE 파일 빌드"""
    print("🔧 YouTube 다운로더 EXE 빌드 시작...")
    
    # PyInstaller 설치 확인
    try:
        import PyInstaller
        print("✅ PyInstaller가 설치되어 있습니다.")
    except ImportError:
        print("❌ PyInstaller가 설치되지 않았습니다.")
        print("설치 중...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 빌드 디렉토리 정리
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    print("🗂️ 빌드 디렉토리 정리 완료")
    
    # PyInstaller 명령어 구성
    # OS에 따른 데이터 구분자 설정
    separator = ":" if os.name != "nt" else ";"
    
    cmd = [
        "pyinstaller",
        "--name", "YouTube_Downloader",
        "--onefile",  # 단일 exe 파일로 생성
        "--console",  # 콘솔 창 표시 (Linux/macOS에서는 windowed 대신)
        f"--add-data=requirements.txt{separator}.",
        "--hidden-import", "streamlit",
        "--hidden-import", "yt_dlp", 
        "--hidden-import", "ffmpeg",
        "--collect-all", "streamlit",
        "--collect-all", "yt_dlp",
        "main.py"
    ]
    
    print("🔨 PyInstaller 실행 중...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ EXE 파일 빌드 성공!")
        print(f"📁 출력 위치: {Path('dist').absolute()}")
        
        # 결과 파일 확인
        exe_name = "YouTube_Downloader.exe" if os.name == "nt" else "YouTube_Downloader"
        exe_path = Path("dist") / exe_name
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 파일 크기: {size_mb:.1f}MB")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False
    
    return True

def create_launcher():
    """Streamlit 실행을 위한 main.py 생성"""
    launcher_content = '''"""
YouTube 다운로더 실행 파일
Streamlit 앱을 자동으로 실행합니다.
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket
from pathlib import Path

def find_free_port():
    """사용 가능한 포트 찾기"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """메인 실행 함수"""
    print("🎥 YouTube 다운로더 시작 중...")
    
    # 현재 디렉토리로 이동
    app_dir = Path(__file__).parent
    os.chdir(app_dir)
    
    # downloads 폴더 생성
    Path("downloads").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    
    # 사용 가능한 포트 찾기
    port = find_free_port()
    
    print(f"🌐 서버 시작 중... 포트: {port}")
    
    # Streamlit 실행
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", str(port),
        "--server.address", "localhost",
        "--browser.gatherUsageStats", "false",
        "--global.developmentMode", "false"
    ]
    
    try:
        # 서버 시작
        process = subprocess.Popen(cmd)
        
        # 잠시 대기 후 브라우저 열기
        time.sleep(3)
        url = f"http://localhost:{port}"
        print(f"🌐 브라우저에서 열기: {url}")
        webbrowser.open(url)
        
        print("✅ YouTube 다운로더가 실행되었습니다!")
        print("📌 종료하려면 이 창을 닫으세요.")
        
        # 서버 프로세스 대기
        process.wait()
        
    except KeyboardInterrupt:
        print("\\n🛑 사용자에 의해 종료되었습니다.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        input("엔터를 눌러 종료하세요...")

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✅ main.py 런처 파일 생성 완료")

if __name__ == "__main__":
    print("=" * 50)
    print("🎥 YouTube 다운로더 EXE 빌더")
    print("=" * 50)
    
    # 런처 파일 생성
    create_launcher()
    
    # EXE 빌드
    if build_exe():
        print("\\n🎉 빌드 완료!")
        print("📁 dist/YouTube_Downloader.exe 파일을 실행하세요.")
    else:
        print("\\n❌ 빌드 실패")
        input("엔터를 눌러 종료하세요...")