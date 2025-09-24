#!/usr/bin/env python3

import argparse
import subprocess
import os
import re
import sys

# 지원하는 해상도 및 해당 크기 매핑
RESOLUTIONS = {
    "1080p": "1920:1080",
    "720p": "1280:720",
    "540p": "960:540",
    "480p": "854:480",
    "360p": "640:360",
    # 필요에 따라 더 많은 해상도를 추가할 수 있습니다.
    # 예: "1440p": "2560:1440", "2160p": "3840:2160"
}

def get_video_resolution(input_path: str) -> tuple[int, int]:
    """
    ffprobe를 사용하여 비디오 파일의 현재 해상도를 가져옵니다.
    """
    try:
        cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
            input_path
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        if 'x' in output:
            width, height = map(int, output.split('x'))
            return width, height
        else:
            raise ValueError(f"ffprobe 출력에서 해상도를 파싱할 수 없습니다: {output}")
    except FileNotFoundError:
        print(f"오류: 'ffprobe' 명령어를 찾을 수 없습니다. FFmpeg/ffprobe가 시스템 PATH에 설치되어 있는지 확인하세요.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"오류: ffprobe 실행 중 문제가 발생했습니다. 파일이 유효한 비디오 파일인지 확인하세요.", file=sys.stderr)
        print(f"ffprobe 에러: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"비디오 해상도를 가져오는 중 예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)
        sys.exit(1)


def generate_output_filename(input_path: str, target_scale_str: str) -> str:
    """
    입력 파일 경로와 목표 해상도 문자열을 기반으로 출력 파일 이름을 생성합니다.
    예: input.1080p.mp4 -> input.720p.mp4
    """
    base_name, ext = os.path.splitext(input_path)
    
    # 파일 이름에서 기존 해상도 패턴 (예: 1080p, 720p) 찾기
    # 대소문자 구분 없이 숫자 뒤에 'p'가 오는 패턴을 찾습니다.
    resolution_pattern = r'\b(\d+p)\b' 
    
    # 파일 이름에서 찾은 모든 해상도 패턴을 저장할 리스트
    found_resolutions = []
    
    # 정규식 패턴과 일치하는 모든 해상도 문자열을 찾습니다.
    # re.finditer를 사용하여 각 일치 항목의 시작 및 끝 인덱스를 얻습니다.
    for match in re.finditer(resolution_pattern, base_name, re.IGNORECASE):
        found_resolutions.append((match.group(1), match.start(), match.end()))
        
    new_base_name = base_name

    # 가장 마지막에 발견된 해상도 문자열을 변경합니다.
    if found_resolutions:
        # 일반적으로 가장 마지막 해상도가 해당 비디오의 최종 해상도를 나타낼 가능성이 높습니다.
        last_res_str, start_idx, end_idx = found_resolutions[-1]
        
        # 새로운 해상도 문자열로 교체
        new_base_name = base_name[:start_idx] + target_scale_str + base_name[end_idx:]
    else:
        # 파일 이름에 해상도 패턴이 없는 경우, 확장자 앞에 추가
        new_base_name = f"{base_name}.{target_scale_str}"
            
    return f"{new_base_name}{ext}"

def main():
    parser = argparse.ArgumentParser(
        description="FFmpeg를 사용하여 NVIDIA GPU 가속으로 비디오 해상도를 조정합니다."
    )
    parser.add_argument(
        "--input", 
        type=str, 
        required=True,
        help="입력 비디오 파일 경로"
    )
    parser.add_argument(
        "--scale", 
        type=str, 
        default="720p",
        choices=RESOLUTIONS.keys(),
        help=f"목표 해상도 (예: 720p). 지원되는 값: {', '.join(RESOLUTIONS.keys())}"
    )
    parser.add_argument(
        "--codec", 
        type=str, 
        default="h264_nvenc",
        choices=["h264_nvenc", "hevc_nvenc"],
        help="사용할 NVIDIA GPU 비디오 코덱 (기본값: h264_nvenc)"
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="fast",
        help="NVENC 인코딩 프리셋 (예: fast, medium, slow, hp, hq, bd, ll, llhq, llhp). 기본값: fast"
    )
    parser.add_argument(
        "--bitrate",
        type=str,
        default="5M",
        help="비디오 비트 전송률 설정 (예: 5M, 10M). 설정하지 않으면 FFmpeg 기본값이 사용됩니다."
    )

    args = parser.parse_args()

    # 입력 파일 존재 여부 확인
    if not os.path.exists(args.input):
        print(f"오류: 입력 파일 '{args.input}'을(를) 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)
    
    # 해상도 값 가져오기
    target_dimensions_str = RESOLUTIONS[args.scale] # argparse choices에서 이미 유효성 검사됨
    target_width, target_height = map(int, target_dimensions_str.split(':'))

    # 현재 비디오 해상도 가져오기
    current_width, current_height = get_video_resolution(args.input)

    # 현재 해상도가 목표 해상도와 동일한지 확인
    if current_width == target_width and current_height == target_height:
        print(f"정보: 입력 비디오의 현재 해상도 ({current_width}x{current_height})가 "
              f"이미 목표 해상도 ({target_width}x{target_height})와 동일합니다.")
        sys.exit(0)

    # 출력 파일 이름 생성
    output_filename = generate_output_filename(args.input, args.scale)
    
    # 입력 파일과 출력 파일이 같으면 오류
    if os.path.abspath(args.input) == os.path.abspath(output_filename):
        print(f"오류: 입력 파일과 출력 파일 이름이 동일합니다. 출력 파일 이름을 변경할 수 없습니다. "
              f"파일 이름에 '{args.scale}'과(와) 충돌하는 해상도 패턴이 있는지 확인하거나, 수동으로 이름을 변경하십시오.", file=sys.stderr)
        sys.exit(1)

    # FFmpeg 명령어 구성
    # GPU (NVIDIA NVENC) 사용 예시:
    # uv run videoScale.py --input "input.mp4" --scale 720p --codec h264_nvenc --preset fast --bitrate 5M
    #
    # CPU (libx264) 사용 예시 (GPU 가속이 없거나 다른 코덱을 사용할 경우):
    # ffmpeg -i input.mp4 -vf "scale=1280:720" -c:v libx264 -preset medium -b:v 5M output.720p.mp4
    # (참고: 이 스크립트는 현재 GPU 가속을 기본으로 하며, CPU 사용을 위해서는 코드 수정이 필요합니다.)
    ffmpeg_cmd = [
        "ffmpeg",
        "-hwaccel", "cuda",          # CUDA 가속 활성화
        "-i", args.input,            # 입력 파일 지정
        "-vf", f"scale={target_dimensions_str}", # 비디오 크기 조정 필터
        "-c:v", args.codec,          # 비디오 코덱 (NVENC)
        "-preset", args.preset,      # NVENC 프리셋
    ]
    
    if args.bitrate:
        ffmpeg_cmd.extend(["-b:v", args.bitrate]) # 비트레이트 설정

    ffmpeg_cmd.append(output_filename) # 출력 파일 지정

    print(f"변환을 시작합니다. 목표 해상도: {args.scale} ({target_dimensions_str})")
    print(f"입력 파일: '{args.input}'")
    print(f"출력 파일: '{output_filename}'")
    print(f"실행될 FFmpeg 명령어:\n{' '.join(ffmpeg_cmd)}\n")

    try:
        # subprocess.run을 사용하여 FFmpeg 명령어 실행
        # check=True: 명령어 실행 실패 시 CalledProcessError 발생
        # capture_output=False (기본값):@video FFmpeg 출력을 콘솔에 직접 표시
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"\n비디오 변환이 성공적으로 완료되었습니다: '{output_filename}'")
    except FileNotFoundError:
        print(f"\n오류: 'ffmpeg' 명령어를 찾을 수 없습니다. FFmpeg가 시스템 PATH에 설치되어 있는지 확인하세요.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n오류: FFmpeg 명령어 실행 중 문제가 발생했습니다.", file=sys.stderr)
        print(f"종료 코드: {e.returncode}", file=sys.stderr)
        # FFmpeg의 에러 메시지는 stderr에 출력되므로, 여기서 추가로 출력할 필요는 없습니다.
        # print(f"FFmpeg 출력 (stderr):\n{e.stderr.decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

