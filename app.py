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

# 현재 상태 알림
st.warning("""
⚠️ **Streamlit Cloud 제한사항 안내**
- YouTube가 클라우드 서버 IP를 차단하여 일부 동영상 다운로드가 제한될 수 있습니다
- **오디오 다운로드**를 먼저 시도해보세요 (성공률이 더 높습니다)
- 여러 번 재시도하거나 다른 동영상으로 테스트해보세요
- 로컬 환경에서는 정상 작동합니다
""")

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
    ydl_opts = {
        "quiet": True, 
        "no_warnings": True,
        # 네트워크 안정성
        "socket_timeout": 30,
        "retries": 3,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"❌ 동영상 정보를 가져오지 못했습니다: {e}")
        return None


def download_video(url: str, download_type: str, output_path: Path) -> Path | None:
    try:
        # 기본 설정
        base_opts = {
            "outtmpl": str(output_path / "%(title)s.%(ext)s"),
            # 강화된 네트워크 설정
            "retries": 20,
            "fragment_retries": 20,
            "socket_timeout": 120,
            # 사용자 에이전트 로테이션
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            },
            # 추가 우회 옵션
            "extractor_args": {
                "youtube": {
                    "skip": ["dash", "hls"],
                    "player_client": ["android", "web"],
                }
            },
            # 지역 및 접근 우회
            "geo_bypass": True,
            "geo_bypass_country": "US",
            # 쿠키 및 세션 관리
            "cookiefile": None,
            "no_check_certificate": True,
            # 디버깅 및 로깅
            "verbose": False,
            "no_warnings": False,
            # 추가 안정성
            "sleep_interval": 3,
            "max_sleep_interval": 15,
            "sleep_interval_requests": 1,
            "sleep_interval_subtitles": 5,
        }
        
        if download_type == "비디오 (MP4)":
            # 비디오용 특별 설정 - 더 낮은 품질로 시도
            video_opts = {
                **base_opts,
                # 낮은 품질부터 시도 (더 성공률 높음)
                "format": "worst[ext=mp4][height<=360]/worst[ext=mp4]/18/17/worst",
                # 추가 비디오 설정
                "youtube_include_dash_manifest": False,
                "youtube_include_hls_manifest": False,
                "prefer_free_formats": True,
                "writesubtitles": False,
                "writeautomaticsub": False,
                # 병합 방지
                "merge_output_format": None,
            }
            ydl_opts = video_opts
            
        else:  # 오디오 (MP3)
            # 오디오용 설정 - 가장 안정적
            audio_opts = {
                **base_opts,
                "format": "worst[acodec!=none]/bestaudio[abr<=64]/worstaudio",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "96",  # 더 낮은 품질로 안정성 확보
                    }
                ],
            }
            ydl_opts = audio_opts

        # 첫 번째 시도
        try:
            st.info("🔄 다운로드 시도 중... (1차)")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                if download_type == "오디오 (MP3)":
                    filename = os.path.splitext(filename)[0] + ".mp3"
                
                file_path = Path(filename)
                if file_path.exists() and file_path.stat().st_size > 0:
                    return file_path
        except Exception as e1:
            st.warning(f"1차 시도 실패: {str(e1)[:100]}...")
            
            # 두 번째 시도 - 다른 클라이언트 사용
            try:
                st.info("🔄 다른 방법으로 재시도 중... (2차)")
                ydl_opts["extractor_args"]["youtube"]["player_client"] = ["android"]
                ydl_opts["format"] = "worstaudio" if download_type == "오디오 (MP3)" else "worst"
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    if download_type == "오디오 (MP3)":
                        filename = os.path.splitext(filename)[0] + ".mp3"
                    
                    file_path = Path(filename)
                    if file_path.exists() and file_path.stat().st_size > 0:
                        return file_path
            except Exception as e2:
                st.warning(f"2차 시도 실패: {str(e2)[:100]}...")
                
                # 세 번째 시도 - 최소 옵션으로
                try:
                    st.info("🔄 최소 옵션으로 재시도 중... (3차)")
                    minimal_opts = {
                        "outtmpl": str(output_path / "%(title)s.%(ext)s"),
                        "format": "worst" if download_type == "비디오 (MP4)" else "worstaudio",
                        "no_warnings": True,
                        "ignoreerrors": True,
                    }
                    
                    if download_type == "오디오 (MP3)":
                        minimal_opts["postprocessors"] = [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "64",
                            }
                        ]
                    
                    with yt_dlp.YoutubeDL(minimal_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        filename = ydl.prepare_filename(info)
                        if download_type == "오디오 (MP3)":
                            filename = os.path.splitext(filename)[0] + ".mp3"
                        
                        file_path = Path(filename)
                        if file_path.exists() and file_path.stat().st_size > 0:
                            return file_path
                except Exception as e3:
                    st.error(f"모든 다운로드 시도 실패")
                    st.error(f"최종 오류: {e3}")
                    return None

        return None
                
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
    
    # 동영상 정보 가져오기
    info = get_video_info(url)
    if info:
        st.write(f"**제목:** {info.get('title')}")
        st.write(f"**채널:** {info.get('uploader')}")
        
        # 사용 가능한 포맷 표시 (디버깅용)
        with st.expander("🔍 사용 가능한 포맷 정보 (디버깅)"):
            formats = info.get('formats', [])
            if formats:
                st.write("**비디오 포맷:**")
                video_formats = [f for f in formats if f.get('vcodec', 'none') != 'none' and f.get('ext') == 'mp4']
                for i, fmt in enumerate(video_formats[:5]):  # 상위 5개만 표시
                    st.write(f"- {fmt.get('format_id')}: {fmt.get('format', 'N/A')} ({fmt.get('protocol', 'N/A')})")
                
                st.write("**오디오 포맷:**")
                audio_formats = [f for f in formats if f.get('acodec', 'none') != 'none']
                for i, fmt in enumerate(audio_formats[:3]):  # 상위 3개만 표시
                    st.write(f"- {fmt.get('format_id')}: {fmt.get('format', 'N/A')} ({fmt.get('protocol', 'N/A')})")

        file_path = download_video(url, download_type, DOWNLOAD_FOLDER)
        if file_path and file_path.exists():
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            st.success(f"✅ 다운로드 완료! (파일 크기: {file_size_mb:.1f}MB)")
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
            st.error("❌ 다운로드 실패: 파일이 생성되지 않았거나 비어있습니다.")
            st.info("💡 **해결 방법:**")
            st.write("1. **오디오 모드로 시도** - 비디오보다 안정적입니다")
            st.write("2. **다른 YouTube URL로 시도** - 일부 동영상은 제한이 있을 수 있습니다")
            st.write("3. **10-15분 후 다시 시도** - 일시적인 제한일 수 있습니다")
            st.write("4. **짧은 동영상으로 시도** - 긴 동영상은 실패 확률이 높습니다")
            
            # 추천 대안
            st.warning("⚠️ **Streamlit Cloud 제한사항**")
            st.write("- 일부 YouTube 동영상은 클라우드 환경에서 다운로드가 제한될 수 있습니다")
            st.write("- 오디오 다운로드가 더 안정적으로 작동합니다")
            st.write("- 로컬 환경에서 실행하면 더 높은 성공률을 보입니다")
    else:
        st.error("❌ 동영상 정보를 가져올 수 없습니다. URL을 확인해주세요!")
