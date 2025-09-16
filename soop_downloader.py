
import argparse
import re
import sys
import os

# yt-dlp 라이브러리 임포트 시도
try:
    import yt_dlp
except ImportError:
    print("오류: yt-dlp 라이브러리가 설치되어 있지 않습니다.")
    print("다음 명령어를 사용하여 설치해주세요: pip install yt-dlp")
    sys.exit(1)

def _progress_hook(d):
    """yt-dlp 다운로드 진행 상황을 출력하는 훅."""
    if d['status'] == 'downloading':
        # 현재 다운로드 중인 파일명, 진행률, 예상 시간을 한 줄에 출력
        # '\r'을 사용하여 줄바꿈 없이 업데이트합니다.
        print(f"진행 상태: {d['status']} | 파일명: {os.path.basename(d.get('filename', 'N/A'))} | "
              f"진행률: {d.get('_percent_str', 'N/A')} | 예상 시간: {d.get('_eta_str', 'N/A')}", end='\r')
    elif d['status'] == 'finished':
        print(f"\n다운로드 완료: {d.get('filename', 'N/A')}")
    elif d['status'] == 'error':
        print(f"\n다운로드 중 오류 발생: {d.get('filename', 'N/A')}")

def download_soop_stream(url, quality="best", username=None, password=None):
    """
    SOOP 라이브 스트림을 다운로드합니다.
    """
    print(f"\nSOOP 스트리밍 다운로드를 시작합니다: {url}")

    # yt-dlp 포맷 문자열 구성
    if quality == "best":
        format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    else:
        # 특정 화질 요청 시, 해당 화질의 비디오와 최상 오디오를 시도하고, 없으면 최상으로 폴백
        format_string = f'bestvideo[height<={quality[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    ydl_opts = {
        'format': format_string, # 가능한 최상의 MP4 비디오 및 오디오, 없으면 최상
        'outtmpl': f'downloads/%(uploader)s_%(id)s.{quality}.%(ext)s', # 출력 파일 이름 템플릿: 업로더_방송ID.화질.확장자

        'noplaylist': True, # 단일 비디오만 다운로드 (플레이리스트 방지)
        'progress_hooks': [_progress_hook], # 진행 상황 출력 훅
        'merge_output_format': 'mp4', # 비디오와 오디오를 합칠 때 MP4 형식으로 병합
        'verbose': False, # yt-dlp의 상세 출력 비활성화
        'no_warnings': True, # 경고 메시지 비활성화
        'live_from_start': False, # 라이브 스트림 시작부터 다운로드 시도 안 함 (현재 시점부터)
        'wait_for_video': 60, # 비디오가 시작될 때까지 최대 60초 기다림 (라이브용)
    }

    if username and password:
        ydl_opts['username'] = username
        ydl_opts['password'] = password

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 다운로드 전에 비디오 정보를 미리 추출하여 제목/업로더 확인
            info = ydl.extract_info(url, download=False)
            title = info.get('title', '알 수 없는 스트림 제목')
            uploader = info.get('uploader', '알 수 없는 BJ')
            
            print(f"스트림 정보 확인 - BJ: {uploader}, 제목: {title}")
            
            # 실제 다운로드 시작
            ydl.download([url])
            downloaded_file_path = ydl.prepare_filename(info)
            print(f"\n'{title}' 스트리밍 다운로드가 성공적으로 완료되었습니다! -> {downloaded_file_path}")
            return downloaded_file_path

    except yt_dlp.utils.DownloadError as e:
        print(f"\n\n스트리밍 다운로드 중 오류 발생: {e}")
        print("yt-dlp가 이 URL을 처리하지 못했거나 네트워크 문제일 수 있습니다.")
        print("yt-dlp를 업데이트(pip install --upgrade yt-dlp)하거나, URL을 확인해보세요.")
    except Exception as e:
        print(f"\n\n예상치 못한 오류가 발생했습니다: {e}")

def download_soop_vod(url, quality="best", username=None, password=None):
    """
    SOOP VOD를 다운로드합니다.
    """
    print(f"\nSOOP VOD 다운로드를 시작합니다: {url}")

    # yt-dlp 포맷 문자열 구성
    if quality == "best":
        format_string = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    else:
        # 특정 화질 요청 시, 해당 화질의 비디오와 최상 오디오를 시도하고, 없으면 최상으로 폴백
        format_string = f'bestvideo[height<={quality[:-1]}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    ydl_opts = {
        'format': format_string, # 가능한 최상의 MP4 비디오 및 오디오, 없으면 최상
        'outtmpl': f'downloads/%(title)s.{quality}.%(ext)s', # 출력 파일 이름 템플릿: 제목.화질.확장자

        'noplaylist': True, # 단일 비디오만 다운로드
        'progress_hooks': [_progress_hook], # 진행 상황 출력 훅
        'merge_output_format': 'mp4', # 비디오와 오디오를 합칠 때 MP4 형식으로 병합
        'verbose': False, # yt-dlp의 상세 출력 비활성화
        'no_warnings': True, # 경고 메시지 비활성화
    }

    if username and password:
        ydl_opts['username'] = username
        ydl_opts['password'] = password

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 다운로드 전에 비디오 정보를 미리 추출하여 제목 확인
            info = ydl.extract_info(url, download=False)
            title = info.get('title', '알 수 없는 VOD 제목')
            
            print(f"VOD 정보 확인 - 제목: {title}")
            
            # 실제 다운로드 시작
            ydl.download([url])
            downloaded_file_path = ydl.prepare_filename(info)
            print(f"\n'{title}' VOD 다운로드가 성공적으로 완료되었습니다! -> {downloaded_file_path}")
            return downloaded_file_path

    except yt_dlp.utils.DownloadError as e:
        print(f"\n\nVOD 다운로드 중 오류 발생: {e}")
        print("yt-dlp가 이 URL을 처리하지 못했거나 네트워크 문제일 수 있습니다.")
        print("URL을 확인하거나 yt-dlp를 업데이트(pip install --upgrade yt-dlp)해보세요.")
    except Exception as e:
        print(f"\n\n예상치 못한 오류가 발생했습니다: {e}")

def main():
    parser = argparse.ArgumentParser(description="SOOP (아프리카TV) 라이브 스트림 및 VOD 다운로더")
    parser.add_argument("--url", required=True, help="다운로드할 SOOP 영상 URL (스트리밍 또는 VOD)")
    parser.add_argument("--quality", default="360p", help="다운로드할 영상의 화질 (예: 'best', '1080p', '720p', '480p'). 기본값은 'best'.")
    parser.add_argument("--username", help="SOOP 계정 사용자 이름 (구독자 전용 영상 다운로드 시 필요)")
    parser.add_argument("--password", help="SOOP 계정 비밀번호 (구독자 전용 영상 다운로드 시 필요)")
    args = parser.parse_args()

    target_url = args.url
    username = args.username
    password = args.password

    # URL 패턴을 분석하여 스트리밍 또는 VOD를 구분
    if "play.sooplive.co.kr" in target_url:
        download_soop_stream(target_url, args.quality, username, password)
    elif "vod.sooplive.co.kr" in target_url:
        download_soop_vod(target_url, args.quality, username, password)
    else:
        print(f"오류: 알 수 없는 SOOP URL 형식입니다: {target_url}")
        print("지원되는 URL 형식:")
        print("  - 스트리밍: https://play.sooplive.co.kr/ksh7637/287010756")
        print("  - VOD:      https://vod.sooplive.co.kr/player/169833005")

if __name__ == "__main__":
    main()