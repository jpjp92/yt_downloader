import streamlit as st
import yt_dlp
import os
import subprocess
from pathlib import Path
import logging
from datetime import datetime

st.set_page_config(
    page_title="YouTube 다운로더",
    page_icon="🎥",
    layout="wide",
)

st.title("🎥 YouTube 동영상 다운로더")
st.markdown("---")

# 다운로드 폴더 설정
DOWNLOAD_FOLDER = Path("downloads")
DOWNLOAD_FOLDER.mkdir(exist_ok=True)

# 로깅 설정
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
log_path = LOG_DIR / "convert.log"

logging.basicConfig(
    filename=str(log_path),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 다운로드 옵션")

    download_type = st.radio(
        "다운로드 형식",
        ["비디오 (MP4)", "오디오 (MP3)"],
    )

    st.markdown("---")
    st.header("🔄 변환 옵션")

    enable_conversion = st.checkbox("MP4 → MPEG 변환", value=False)

    conversion_quality = "균형 (중간 품질)"
    reduce_resolution = False
    fast_mode = False

    if enable_conversion:
        st.info("다운로드 후 자동으로 MPEG 형식으로 변환됩니다.")
        
        # 빠른 변환 모드
        fast_mode = st.checkbox(
            "⚡ 빠른 변환 모드 (품질 약간 낮음)",
            value=True,
            help="변환 속도를 2-3배 빠르게 합니다. 품질은 약간 낮아질 수 있습니다."
        )
        
        conversion_quality = st.select_slider(
            "변환 품질",
            options=["최소 용량 (낮은 품질)", "균형 (중간 품질)", "고품질 (큰 용량)"],
            value="균형 (중간 품질)",
            help="균형 모드는 MP4와 비슷한 크기로 변환됩니다.",
        )

        reduce_resolution = st.checkbox(
            "해상도 줄이기 (720p로)",
            value=False,
            help="파일 크기를 크게 줄일 수 있습니다. (1080p → 720p)",
        )

    # st.markdown("---")
    # st.info("💡 팁: URL 입력 후 엔터 또는 다운로드 버튼을 누르세요!")

# --- 메인 입력/버튼 구간 (st.form 활용) ---
with st.form("download_form"):
    url_col, btn_col = st.columns([4, 1])

    with url_col:
        url = st.text_input(
            "YouTube URL을 입력하세요",
            placeholder="https://www.youtube.com/watch?v=...",
            help="YouTube 동영상의 전체 URL을 입력해주세요",
            label_visibility="collapsed",
        )

    with btn_col:
        download_btn = st.form_submit_button("⬇️ 다운로드", use_container_width=True)


# --- 다운로드 및 변환 함수 정의 ---
def get_video_info(url: str):
    """동영상 정보 가져오기"""
    ydl_opts = {"quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"❌ 동영상 정보를 가져오지 못했습니다: {e}")
        return None


def download_video(url: str, download_type: str, output_path: Path) -> Path | None:
    try:
        if download_type == "비디오 (MP4)":
            ydl_opts = {
                # Streamlit Cloud용 최적화: 병합이 필요없는 단일 포맷 선택
                "format": "best[ext=mp4][height<=1080]/best[ext=mp4]/best",
                "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                # ffmpeg 병합 비활성화
                "merge_output_format": None,
                # 다운로드 속도 개선 옵션
                "concurrent_fragment_downloads": 5,
                "http_chunk_size": 10485760,
                # 오류 시 중단하지 않고 계속 진행
                "ignoreerrors": True,
                "no_warnings": True,
            }
        else:  # 오디오 (MP3)
            ydl_opts = {
                # 오디오만 추출 - 이미 오디오 전용 포맷 선택
                "format": "bestaudio[ext=m4a]/bestaudio",
                "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",  # 320에서 192로 낮춤 (안정성)
                    }
                ],
                "ignoreerrors": True,
                "no_warnings": True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if download_type == "오디오 (MP3)":
                filename = os.path.splitext(filename)[0] + ".mp3"
            return Path(filename)
    except Exception as e:
        st.error(f"❌ 다운로드 중 오류 발생: {e}")
        return None


def convert_mp4_to_mpeg(input_path: Path, output_path: Path, quality: str, reduce_res: bool,
                        fast_mode: bool = True, progress_bar=None, status_text=None) -> Path | None:
    """FFmpeg를 사용해 MP4 -> MPEG 변환 (진행 상태 표시 포함)"""
    import re
    
    # 품질 매핑 (비트레이트 기반으로 변경 - 파일 크기 제어)
    quality_settings = {
        "최소 용량 (낮은 품질)": {
            "video_bitrate": "800k",   # 800 kbps
            "audio_bitrate": "96k",    # 96 kbps
        },
        "균형 (중간 품질)": {
            "video_bitrate": "1500k",  # 1.5 Mbps (원본보다 작게)
            "audio_bitrate": "128k",   # 128 kbps
        },
        "고품질 (큰 용량)": {
            "video_bitrate": "3000k",  # 3 Mbps
            "audio_bitrate": "192k",   # 192 kbps
        },
    }
    
    settings = quality_settings.get(quality, quality_settings["균형 (중간 품질)"])

    # FFmpeg 명령어 구성 (속도 최적화 추가)
    cmd = [
        "ffmpeg", "-i", str(input_path),
        "-threads", "0",                # 모든 CPU 코어 사용 (자동)
        "-c:v", "mpeg2video",           # MPEG-2 비디오 코덱
        "-b:v", settings["video_bitrate"],  # 비디오 비트레이트 제한
        "-maxrate", settings["video_bitrate"],  # 최대 비트레이트
        "-bufsize", "2M",               # 버퍼 크기
    ]
    
    # 빠른 모드 설정
    if fast_mode:
        cmd.extend([
            "-preset", "ultrafast",     # 빠른 인코딩 (속도 우선)
            "-tune", "fastdecode",      # 빠른 디코딩 최적화
            "-g", "250",                # GOP 크기 증가 (키프레임 줄임)
            "-bf", "0",                 # B-프레임 제거 (속도 증가)
        ])
    else:
        cmd.extend([
            "-g", "150",                # 표준 GOP 크기
            "-bf", "2",                 # B-프레임 사용 (품질 증가)
        ])
    
    cmd.extend([
        "-c:a", "mp2",                  # MPEG-1 Layer 2 오디오
        "-b:a", settings["audio_bitrate"],  # 오디오 비트레이트
        "-progress", "pipe:1",
    ])
    
    if reduce_res:
        # 빠른 스케일링 알고리즘 사용
        scale_filter = "scale=-2:720:flags=fast_bilinear" if fast_mode else "scale=-2:720"
        cmd.extend(["-vf", scale_filter])
    
    cmd.extend([str(output_path), "-y"])

    try:
        # 동영상 길이 가져오기 (진행률 계산용)
        probe_cmd = [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(input_path)
        ]
        duration_result = subprocess.run(probe_cmd, capture_output=True, text=True)
        total_duration = float(duration_result.stdout.strip()) if duration_result.stdout.strip() else 0
        
        # FFmpeg 실행 (실시간 진행 상태 캡처)
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # 진행 상태 추적
        for line in process.stdout:
            if "out_time_ms=" in line:
                # 현재 처리 시간 추출 (마이크로초)
                match = re.search(r'out_time_ms=(\d+)', line)
                if match and total_duration > 0:
                    current_time = int(match.group(1)) / 1000000  # 초 단위로 변환
                    progress = min(current_time / total_duration, 1.0)
                    
                    # UI 업데이트
                    if progress_bar:
                        progress_bar.progress(progress)
                    if status_text:
                        status_text.text(f"🔄 변환 중... {progress*100:.1f}%")
        
        process.wait()
        
        if process.returncode == 0:
            if progress_bar:
                progress_bar.progress(1.0)
            if status_text:
                status_text.text("✅ 변환 완료!")
            logging.info(f"✅ 변환 완료: {output_path}")
            return output_path
        else:
            raise subprocess.CalledProcessError(process.returncode, cmd)
            
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ 변환 실패: {e}")
        st.error(f"❌ 변환 실패: {e}")
        return None
    except Exception as e:
        logging.error(f"❌ 변환 오류: {e}")
        st.error(f"❌ 변환 오류: {e}")
        return None


# --- 실행부 ---
if download_btn and url:
    st.info("📥 다운로드를 시작합니다... 잠시만 기다려주세요.")
    info = get_video_info(url)
    if info:
        st.write(f"**제목:** {info.get('title')}")
        st.write(f"**채널:** {info.get('uploader')}")

        file_path = download_video(url, download_type, DOWNLOAD_FOLDER)
        if file_path and file_path.exists():
            st.success("✅ 다운로드 완료!")
            st.write(f"저장 위치: `{file_path}`")

            mpeg_path = None
            if enable_conversion and download_type == "비디오 (MP4)":
                st.markdown("---")
                st.subheader("🔄 MPEG 변환")
                
                # 프로그레스 바와 상태 텍스트 생성
                conversion_progress = st.progress(0)
                conversion_status = st.empty()
                conversion_status.text("🔄 변환 준비 중...")
                
                output_file = file_path.with_suffix(".mpg")
                mpeg_path = convert_mp4_to_mpeg(
                    file_path, 
                    output_file, 
                    conversion_quality, 
                    reduce_resolution,
                    fast_mode=fast_mode,
                    progress_bar=conversion_progress,
                    status_text=conversion_status
                )
                
                if mpeg_path and mpeg_path.exists():
                    st.success(f"✅ 변환 완료! 저장 위치: `{mpeg_path}`")
                    # 파일 크기 비교
                    original_size = file_path.stat().st_size / (1024 * 1024)
                    converted_size = mpeg_path.stat().st_size / (1024 * 1024)
                    st.info(f"📊 크기 비교: {original_size:.1f}MB → {converted_size:.1f}MB ({converted_size/original_size*100:.0f}%)")
                else:
                    conversion_status.text("❌ 변환 실패")

            # 다운로드 버튼 제공
            st.markdown("---")
            st.subheader("💾 다운로드")
            
            col1, col2 = st.columns(2)
            
            with col1:
                with open(file_path, "rb") as f:
                    data = f.read()
                file_size = len(data) / (1024 * 1024)
                st.download_button(
                    label=f"💾 원본 파일 다운로드 ({file_size:.1f}MB)",
                    data=data,
                    file_name=file_path.name,
                    mime="video/mp4" if file_path.suffix == ".mp4" else "audio/mpeg",
                    use_container_width=True,
                )

            with col2:
                if mpeg_path and mpeg_path.exists():
                    with open(mpeg_path, "rb") as f:
                        data = f.read()
                    mpeg_size = len(data) / (1024 * 1024)
                    st.download_button(
                        label=f"💾 MPEG 파일 다운로드 ({mpeg_size:.1f}MB)",
                        data=data,
                        file_name=mpeg_path.name,
                        mime="video/mpeg",
                        use_container_width=True,
                    )
    else:
        st.error("❌ 동영상 정보를 가져올 수 없습니다. URL을 확인해주세요!")
