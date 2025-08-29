import sys
import os
import time
import threading
import itertools
import argparse
import pyttsx3
import subprocess
from pydub import AudioSegment
from ai.GeminiAI import GeminiAI

class Spinner:
    def __init__(self, message="AI 요청중... ", delay=0.1):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.spinner_thread = None
        self.message = message

    def spin(self):
        while self.busy:
            sys.stdout.write(f'\r{self.message}{next(self.spinner)}')
            sys.stdout.flush()
            time.sleep(self.delay)

    def __enter__(self):
        self.busy = True
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.busy = False
        self.spinner_thread.join()
        # Clear the line
        sys.stdout.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        sys.stdout.flush()


def gemini(chatmsg,system_prompt="", model_name="gemini-2.5-flash",temperature=0.5):
    try:
        start_time = time.time()
        # print(f"model_name:{model_name}, system_prompt:{system_prompt}, chatmsg:{chatmsg}")
        geminiai = GeminiAI()
        res = geminiai.chat(
            model_name=model_name,
            prompt=chatmsg,
            **({"system_instruction": system_prompt} if system_prompt else {})
        )
        end_time = time.time()
        response_time = end_time - start_time

        # print(res)
        return res, response_time
    except Exception as e:
        return f"오류 발생: {e}", 0

def _read_or_use_text(input_string):
    """
    주어진 문자열이 파일 경로이면 파일 내용을 읽어 반환하고,
    그렇지 않으면 문자열 자체를 반환합니다.
    """
    if os.path.exists(input_string) and os.path.isfile(input_string):
        with open(input_string, 'r', encoding='utf-8') as f:
            return f.read()
    return input_string

def speech(message, output_file, lang='ko', speech_mode='man'):
    """
    텍스트를 음성으로 변환하여 파일로 저장합니다.
    """
    try:
        print(f"Attempting to convert text to speech and save to: '{output_file}' using pyttsx3")
        engine = pyttsx3.init()
        with Spinner("오디오 생성중... "):
            # Set language/voice based on lang and speech_mode
            voices = engine.getProperty('voices')
            selected_voice = None
            # for voice in voices:
            #     print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {voice.name}")
            for voice in voices:
                # Attempt to find a Korean voice, and optionally a male voice
                # pyttsx3 voice.languages is a list of language codes, e.g., ['en-US']
                # voice.id often contains more detailed info, e.g., 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0'
                # We need to check if 'ko' is in voice.languages or voice.id
                if any(l.startswith(lang) for l in voice.languages) or lang in voice.id.lower():
                    if speech_mode == 'man' and 'male' in voice.name.lower():
                        selected_voice = voice.id
                        break
                    elif speech_mode == 'woman' and 'female' in voice.name.lower():
                        selected_voice = voice.id
                        break
                    elif speech_mode == 'default':
                        selected_voice = voice.id
                        break
                # Fallback for general Korean voice if specific gender not found or not requested
                if selected_voice is None and (any(l.startswith(lang) for l in voice.languages) or lang in voice.id.lower()):
                    selected_voice = voice.id

            if selected_voice:
                engine.setProperty('voice', selected_voice)
                engine.setProperty('volume', 1.0)  # Max volume
                print(f"Using voice: {engine.getProperty('voice')}")
            else:
                print(f"Warning: No specific voice found for lang='{lang}' and speech_mode='{speech_mode}'. Using default voice.")

            # engine.save_to_file(message, output_file)
            # print(f"음성 파일이 '{output_file}'에 저장되었습니다.")
        # play_audio(output_file)
        with Spinner("오디오 재생중... "):
            engine.say(message)
            engine.runAndWait()
    except Exception as e:
        print(f"음성 변환 중 오류 발생: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for debugging

    """
def play_audio(file_path):
    지정된 음성 파일을 재생합니다.
    try:
        print(f"음성 파일 재생: '{file_path}' using ffplay")
        # Ensure ffplay is installed and in PATH
        subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path], check=True)
    except FileNotFoundError:
        print("Error: ffplay not found. Please ensure FFmpeg is installed and ffplay is in your system's PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error playing audio with ffplay: {e}")
    except Exception as e:
        print(f"음성 파일 재생 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
"""

def main():
    print("Script started: Entering main function.")
    system_prompt_file = os.path.join(os.path.dirname(__file__), "prompt", "aispeech.md")
    system_prompt = _read_or_use_text(system_prompt_file)


    parser = argparse.ArgumentParser(description="읽어주는..")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--message", 
        help="음성으로 변환할 텍스트 또는 텍스트 파일 경로입니다."
    )
    
    parser.add_argument("--filter-mode", default="text", help="텍스트 처리 모드: 'text' (입력 텍스트 그대로 사용) 또는 'ai' (AI를 사용하여 텍스트 요약 후 사용).")
    parser.add_argument("--speech-mode", default="man", help="음성 변환 모드 (현재는 'man'만 지원).")
    parser.add_argument("--output", default="./result/speech.mp3", help="생성될 음성 파일의 경로 및 이름입니다.")
    
    args = parser.parse_args()

    # Ensure the output directory exists
    output_dir = os.path.dirname(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    message = _read_or_use_text(args.message)
    result_message = ""

    if args.filter_mode == "ai": # Changed from args.filter-mode to args.filter_mode
        with Spinner(f"AI 내용 요약중... "):
            ai_response, _ = gemini(message, system_prompt)
            result_message = ai_response[0] if isinstance(ai_response, tuple) else ai_response
            
            ai_response_file = os.path.join(output_dir, "ai_response.txt")
            with open(ai_response_file, "w", encoding="utf-8") as f:
                f.write(result_message)
            print(f"AI 응답이 '{ai_response_file}'에 저장되었습니다.")
    elif args.filter_mode == "text": # Changed from args.filter-mode to args.filter_mode
        result_message = message
    else:
        print("필터 모드값이 잘못되었습니다.")
        return

    if result_message:
        print(f"Result message prepared: {result_message}")
        print(f"Calling speech function with output file: {args.output}, speech_mode: {args.speech_mode}")
        speech(result_message, args.output, speech_mode=args.speech_mode)

if __name__ == "__main__":
    main()
        
