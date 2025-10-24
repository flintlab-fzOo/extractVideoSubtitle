import argparse
from yt_dlp import YoutubeDL, DownloadError
import os
import subprocess
from dotenv import load_dotenv
import ffmpeg
from soop_downloader import download_soop_stream, download_soop_vod

# .env 파일에서 환경 변수 로드
load_dotenv(verbose=True)

# os.environ['PYTHONIOENCODING'] = 'utf-8'

def get_download_formats(target_quality):
    """
    주어진 화질에 맞는 YouTube 다운로드 포맷 문자열을 반환합니다.
    yt-dlp가 가용한 프로토콜(HLS, DASH 등)을 자동으로 선택하도록 합니다.
    """
    quality_map = {
        '2160p': 2160, '1440p': 1440, '1080p': 1080, '720p': 720,
        '480p': 480, '360p': 360, '240p': 240, '144p': 144
    }
    
    height = quality_map.get(target_quality)
    if height:
        # bv* = best video, ba = best audio, b = best (combined)
        return f'bv*[height<={height}]+ba/b[height<={height}]'
    
    return 'bv*+ba/b'

def extract_audio(video_path, output_path=None, video_id=None):
    """
    ffmpeg를 사용하여 비디오 파일에서 오디오를 추출하여 mp3로 저장합니다.

    Parameters:
        video_path (str): 입력 비디오 파일 경로.
        output_path (str): 오디오를 저장할 경로 (기본값: 비디오와 동일한 디렉토리, 확장자 .mp3).
        video_id (str): YouTube 비디오 ID (파일명으로 사용).
    """
    if not os.path.exists(video_path):
        print(f"오류: 비디오 파일을 찾을 수 없습니다 - {video_path}")
        return None

    try:
        # 출력 파일 경로가 지정되지 않은 경우, 비디오 ID 또는 비디오와 같은 이름의 mp3 파일로 설정
        if output_path is None:
            base_dir = os.path.dirname(video_path)
            if video_id:
                output_path = os.path.join(base_dir, f"{video_id}.mp3")
            else:
                base, _ = os.path.splitext(video_path)
                output_path = base + '.mp3'

        # 오디오 파일이 이미 존재하는지 확인
        if os.path.exists(output_path):
            print(f"이미 추출된 오디오 파일입니다: {output_path}")
            return output_path

        print(f"오디오 추출 시작: {video_path} -> {output_path}")
        
        # ffmpeg를 사용하여 오디오 추출
        ffmpeg.input(video_path).output(output_path, f='mp3').run(overwrite_output=True, quiet=True)
        """
        # 오디오 파일 유효성 검사 (길이 확인)
        try:
            probe = ffmpeg.probe(output_path)
            duration = float(probe['format']['duration'])
            if duration < 1:
                print(f"오류: 추출된 오디오 파일이 너무 짧거나 비어있습니다 (길이: {duration}초).")
                os.remove(output_path) # 유효하지 않은 파일 삭제
                return None
        except (ffmpeg.Error, KeyError, ValueError) as e:
            print(f"오류: 추출된 오디오 파일의 정보를 읽을 수 없습니다. {e}")
            return None
        """

        print(f"오디오 추출 완료: {output_path}")
        return output_path

    except ffmpeg.Error as e:
        print(f"오디오 추출 중 FFmpeg 오류 발생: {e.stderr.decode()}")
        print("FFmpeg가 시스템에 설치되어 있고 PATH에 등록되어 있는지 확인하세요.")
        return None
    except Exception as e:
        print(f"오디오 추출 중 알 수 없는 오류 발생: {e}")
        return None

def download_youtube_video_cli(video_url, quality='720p', output_path=None):
    """
    yt-dlp를 사용하여 YouTube 영상을 다운로드하고 파일 경로를 반환하는 CLI 함수

    Parameters:
        video_url (str): YouTube 영상 URL 또는 비디오 코드
        quality (str): 원하는 화질 (예: '720p', '1080p')
        output_path (str): 저장할 경로 (기본값: .env 파일 또는 'downloads' 폴더)
    
    Returns:
        str: 다운로드된 파일의 경로 또는 실패 시 None
    """
    # 기본 저장 경로 설정 (환경 변수 YTDN_DIC_PATH 사용, 없으면 'downloads')
    if output_path is None:
        output_path = os.environ.get('YTDN_DIC_PATH', 'downloads')

    # 저장 디렉토리가 없으면 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 임시 ydl 인스턴스로 영상 ID만 조용히 가져오기
    video_id = None
    try:
        with YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_id = info_dict.get('id')
    except Exception as e:
        print(f"비디오 정보 추출 중 오류 발생: {str(e)}")
        return None

    # 화질 재시도 리스트 (720p 실패 시 480p, 480p 실패 시 360p)
    fallback_qualities = ['720p', '480p', '360p']
    
    # 현재 요청된 quality가 fallback_qualities에 없으면 추가
    if quality and quality not in fallback_qualities:
        # 현재 quality가 720p보다 높으면 720p부터 시작하도록 조정
        # 간단하게 현재 quality를 리스트의 맨 앞에 추가하고 중복 제거
        try:
            if int(quality[:-1]) > 720: # '1080p' -> 1080
                fallback_qualities.insert(0, quality)
            else:
                # 720p보다 낮거나 같은데 리스트에 없는 경우 (예: 240p)
                # 해당 quality부터 시작하도록 리스트 재구성
                current_quality_index = -1
                for i, q in enumerate(fallback_qualities):
                    if int(q[:-1]) <= int(quality[:-1]):
                        current_quality_index = i
                        break
                if current_quality_index != -1:
                    fallback_qualities = fallback_qualities[current_quality_index:]
                else:
                    fallback_qualities.insert(0, quality)
        except ValueError: # quality가 'best' 등 숫자가 아닌 경우
            fallback_qualities.insert(0, quality)
    elif quality is None: # quality가 None인 경우 (기본값 720p로 시작)
        quality = '720p'
        
    # 중복 제거 및 순서 유지
    seen = set()
    fallback_qualities = [q for q in fallback_qualities if not (q in seen or seen.add(q))]
    
    downloaded_file_path = None
    for current_quality in fallback_qualities:
        print(f"\n다운로드 시도: {video_url} (화질: {current_quality})")
        
        # 파일 존재 여부 확인
        if video_id:
            for filename in os.listdir(output_path):
                if f"[{video_id}]" in filename:
                    existing_file_path = os.path.join(output_path, filename)
                    print(f"이미 다운로드된 파일입니다: {existing_file_path}")
                    return existing_file_path

        try:
            
            # yt-dlp 옵션 설정
            ydl_opts = {
                'outtmpl': os.path.join(output_path, f'%(title)s.{current_quality}[%(id)s].%(ext)s'),
                'quiet': False,
                'no_warnings': False,
                'merge_output_format': 'mkv',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                },
                'extractor_args': {'youtube': {'player_client': ['web_embedded', 'web']}}
            }
            
            # 환경 변수에서 프록시 설정 로드 (예: YTDN_PROXY="http://your_proxy_server:port")
            proxy = os.environ.get('YTDN_PROXY')
            if proxy:
                ydl_opts['proxy'] = proxy
                print(f"프록시 사용: {proxy}")

            ydl_opts['format'] = get_download_formats(current_quality)
            
            print(f"저장 폴더: {os.path.abspath(output_path)}")


            with YoutubeDL(ydl_opts) as ydl:
                # 다운로드 실행
                ydl.download([video_url])
                # 다운로드된 파일의 전체 경로 가져오기
                downloaded_file_path = ydl.prepare_filename(info_dict)
                
                # prepare_filename이 실제 파일과 다를 수 있으므로, ID로 다시 한번 스캔하여 정확한 경로를 찾음
                if not os.path.exists(downloaded_file_path):
                    for filename in os.listdir(output_path):
                        if f"[{video_id}]" in filename:
                            downloaded_file_path = os.path.join(output_path, filename)
                            break
            
            if downloaded_file_path and os.path.exists(downloaded_file_path):
                print(f"\n다운로드 완료! -> {downloaded_file_path}")
                return downloaded_file_path # 성공 시 즉시 반환
        except Exception as e:
            print(f"다운로드 중 알 수 없는 오류 발생: {str(e)}")



        try:
            command = ['yt-dlp']
            
            # 여러 player client를 시도하도록 명시
            command.extend(['--extractor-args', 'youtube:player_client=android,ios,web,tv_embedded'])
            
            title = info_dict.get('title', 'unknown_title')
            invalid_chars = '\\/:*?"<>|'
            for char in invalid_chars:
                title = title.replace(char, '_')
            video_id_for_filename = info_dict.get('id', 'unknown_id')

            output_template = os.path.join(output_path, f"{title}[{video_id_for_filename}].mkv")
            output_template = output_template.replace('\\','/')
            command.extend(['-o', output_template])

            command.extend(['--merge-output-format', 'mkv'])

            proxy = os.environ.get('YTDN_PROXY')
            if proxy:
                command.extend(['--proxy', proxy])

            command.append(video_url)

            print(f"저장 폴더: {os.path.abspath(output_path)}")
            print(f"yt-dlp CLI 명령 실행: {' '.join(command)}")

            result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')
            print(f"yt-dlp stdout: {result.stdout}")
            
            # 다운로드된 파일 찾기
            downloaded_file_path = None
            for filename in os.listdir(output_path):
                if video_id and f"[{video_id}]" in filename:
                    downloaded_file_path = os.path.join(output_path, filename)
                    break
            
            if downloaded_file_path and os.path.exists(downloaded_file_path):
                print(f"\n다운로드 완료! -> {downloaded_file_path}")
                return downloaded_file_path
            else:
                print("오류: 다운로드된 파일을 찾을 수 없습니다.")
                return None

        except subprocess.CalledProcessError as e:
            print(f"다운로드 중 오류 발생: {e.stderr + e.stdout}")
            return None
        except Exception as e:
            print(f"다운로드 중 알 수 없는 오류 발생: {str(e)}")
            return None

    print(f"오류: 모든 시도에서 비디오 다운로드에 실패했습니다: {video_url}")
    return None

def download_soop_video_cli(soop_url, quality="360p", output_path=None):
    """
    SOOP 영상을 다운로드하고 파일 경로를 반환하는 CLI 함수

    Parameters:
        soop_url (str): SOOP 영상 URL (스트리밍 또는 VOD)
        quality (str): 원하는 화질 (예: 'best', '1080p', '720p', '480p')
        output_path (str): 저장할 경로 (기본값: 'downloads' 폴더)
    
    Returns:
        str: 다운로드된 파일의 경로 또는 실패 시 None
    """
    try:
        if output_path is None:
            output_path = os.environ.get('YTDN_DIC_PATH', 'downloads')

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # SOOP 다운로드 로직 (soop_downloader.py 참고)
        downloaded_file_path = None
        if "play.sooplive.co.kr" in soop_url:
            print(f"SOOP 스트리밍 다운로드 시작: {soop_url} (화질: {quality})")
            downloaded_file_path = download_soop_stream(soop_url, quality)
        elif "vod.sooplive.co.kr" in soop_url:
            print(f"SOOP VOD 다운로드 시작: {soop_url} (화질: {quality})")
            downloaded_file_path = download_soop_vod(soop_url, quality)
        else:
            print(f"오류: 알 수 없는 SOOP URL 형식입니다: {soop_url}")
            return None
        
        if not downloaded_file_path:
            print("오류: SOOP 영상 다운로드에 실패했습니다.")
            return None
        
        print(f"SOOP 다운로드 완료! -> {downloaded_file_path}")
        return downloaded_file_path

    except Exception as e:
        print(f"SOOP 다운로드 중 오류 발생: {str(e)}")
        return None

def run_transcription(audio_path, video_path, summary=False, system_prompt="./prompt/내용정리프롬프트.md", video_id=None):
    """
    Whisper-Faster를 사용하여 오디오 파일의 텍스트를 추출합니다.

    Parameters:
        audio_path (str): 텍스트를 추출할 오디오 파일 경로.
        video_path (str): 원본 비디오 파일 경로.
        summary (bool): 텍스트 추출 후 요약을 실행할지 여부.
        video_id (str): YouTube 비디오 ID.
    """
    try:
        # 스크립트의 현재 위치를 기준으로 whisper-faster.exe 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        executable_path = os.path.join(script_dir, '.', 'Whisper-Faster', 'whisper-faster.exe')

        if not os.path.exists(executable_path):
            print(f"오류: 실행 파일을 찾을 수 없습니다 - {executable_path}")
            return

        # command = [executable_path, audio_path]
        command = [executable_path, '--batch_recursive', audio_path]
        
        print(f"\n텍스트 추출 실행: {' '.join(command)}")
        
        # 쉘 명령어 실행
        subprocess.run(command, check=True)
        
        print("\n텍스트 추출 완료.")

        # 자막 파일 경로 생성 (오디오 파일과 이름이 같고 확장자만 .srt)
        subtitle_path = os.path.splitext(audio_path)[0] + '.srt'
        
        if os.path.exists(subtitle_path):
            # 자막 파일 마지막에 영상 파일명 추가
            try:
                with open(subtitle_path, 'a', encoding='utf-8') as f:
                    f.write(f"{os.path.basename(video_path)}")
                print(f"영상 파일명을 자막 파일에 추가했습니다: {subtitle_path}")
            except Exception as e:
                print(f"자막 파일에 영상 파일명을 추가하는 중 오류 발생: {e}")

            if summary:
                print(f"{subtitle_path} 파일에 대한 요약 실행...")
                
                output_filename = ""
                if video_id:
                    output_filename = f"./result/{video_id}.md"
                else:
                    # Fallback for local video files
                    video_filename_without_ext = os.path.splitext(os.path.basename(video_path))[0]
                    output_filename = f"./result/{video_filename_without_ext}.md"
                
                summary_command = ['uv', 'run', 'aisummary.py', '--system_prompt',system_prompt, '--input', f"./{subtitle_path}", '--model','gemini','--output', output_filename]
                subprocess.run(summary_command, check=True)
        else:
            print(f"오류: 자막 파일을 찾을 수 없습니다 - {subtitle_path}")
        print(f"완료")

    except FileNotFoundError:
        print(f"오류: 'whisper-faster.exe'를 찾을 수 없습니다. 경로를 확인하세요.")
    except subprocess.CalledProcessError as e:
        print(f"텍스트 추출 또는 요약 중 오류 발생: {e}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")


def main():
    """
    스크립트의 메인 실행 함수. 커맨드 라인 인자를 파싱하고 다운로드를 시작합니다.
    """
    parser = argparse.ArgumentParser(description="YouTube 비디오를 다운로드하거나 로컬 비디오 파일을 사용하여 오디오 및 텍스트를 추출합니다.")
    
    # --youtube와 --video를 상호 배타적인 인수로 설정
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--youtube", 
        help="다운로드할 YouTube 비디오의 코드 또는 전체 URL. (오디오/자막 추출 실행)"
    )
    group.add_argument(
        "--video",
        help="처리할 로컬 비디오 파일의 경로. (오디오/자막 추출 실행)"
    )
    group.add_argument(
        "--download",
        help="YouTube 비디오를 다운로드만 실행."
    )
    group.add_argument(
        "--soop_url",
        help="다운로드할 SOOP 영상 URL (스트리밍 또는 VOD). (오디오/자막 추출 실행)"
    )
    
    parser.add_argument(
        "--quality", 
        default=None, 
        help="YouTube 다운로드 시 사용할 비디오 화질 (예: 1080p, 720p 등). 기본값: --youtube(144p), --download(720p)"
    )
    parser.add_argument(
        "--summary",
        action='store_true',
        help="자막 추출 후 AI 요약을 실행합니다."
    )
    parser.add_argument("--system_prompt", default="./prompt/내용정리프롬프트.md", help="Path to the system prompt file.")
    
    args = parser.parse_args()
    
    video_file_path = None
    quality = args.quality

    if args.download:
        if quality is None:
            quality = "720p"
        video_file_path = download_youtube_video_cli(args.download, quality)
        return
    elif args.youtube:
        if quality is None:
            quality = "144p"
        # 1. YouTube 비디오 다운로드
        video_file_path = download_youtube_video_cli(args.youtube, quality)
    elif args.soop_url:
        if quality is None and args.summary:
            quality = "360p"
        elif quality is None:
            quality = "720p"
        # 1. SOOP 비디오 다운로드
        video_file_path = download_soop_video_cli(args.soop_url, quality)
    elif args.video:
        # 로컬 비디오 파일 사용
        if not os.path.exists(args.video):
            print(f"오류: 로컬 비디오 파일을 찾을 수 없습니다 - {args.video}")
            return
        video_file_path = args.video

    # 2. 오디오 추출 (파일 경로가 유효한 경우)
    if video_file_path:
        # YouTube 비디오인 경우 video_id 추출
        video_id = None
        if args.youtube or args.download:
            with YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                info_dict = ydl.extract_info(args.youtube or args.download, download=False)
                video_id = info_dict.get('id')
        elif args.soop_url and video_file_path:
            # SOOP 비디오의 경우, 다운로드된 파일명에서 ID 추출
            base_filename = os.path.basename(video_file_path)
            # 파일명 형식: %(uploader)s_%(id)s.{quality}.%(ext)s 또는 %(title)s.{quality}.%(ext)s
            # .quality.ext 부분을 제거하여 순수한 ID 부분만 남김
            # 예: uploader_id.best.mp4 -> uploader_id
            # 예: title.best.mp4 -> title
            video_id = base_filename.rsplit('.', 2)[0] # 마지막 두 점(.)을 기준으로 분리하여 앞 부분 가져오기

        audio_file = extract_audio(video_file_path, video_id=video_id)
        
        # 3. 텍스트 추출 (오디오 추출 성공 시)
        if audio_file:
            print(f"system_prompt : {args.system_prompt}")
            run_transcription(audio_file, video_file_path, args.summary, system_prompt=args.system_prompt, video_id=video_id)


if __name__ == "__main__":
    main()
