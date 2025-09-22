import ollama
import time
import requests
import os
import argparse
import subprocess
from ai.GeminiAI import GeminiAI
import sys
import threading
import itertools

# ollama_model_name="gpt-oss:20b"
# system_prompt_file="./prompt/내용정리프롬프트.md"
# prompt_file="./downloads/YC1V4EeX5Q8.srt"

# os.environ['PYTHONIOENCODING'] =  'utf-8'


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


def chat(chatmsg, system_prompt="", model_name="gpt-oss:20b", temperature=0.5, use_gpu=True):
    try:
        # ollama 실행 안되어 있는경우 실행하기위해 커맨드 실행
        # ollama_command = ['ollama', 'list']
        # subprocess.run(ollama_command, check=True)
        
        messages = []
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        messages.append({
            'role': 'user',
            'content': chatmsg
        })
        
        # GPU 사용 여부에 따라 Ollama 옵션 설정
        # GPU를 사용하려면 num_gpu를 1 이상으로, CPU만 사용하려면 0으로 설정합니다.
        ollama_options = {
            'temperature': temperature,
            # 'num_gpu': 20 if use_gpu else 0,
            'num_gpu': 9 if use_gpu else 0,
            # "num_ctx": 2048,  # 예: context window 사이즈
            'num_thread': -1, # 자동 스레드 수 감지
        }

        # https://github.com/ollama/ollama/blob/main/docs/gpu.md
        # nvidia-smi -L
        # set CUDA_VISIBLE_DEVICES='GPU-93779944-3708-cb7b-b6f1-cf49656fe4aa'
        # export CUDA_VISIBLE_DEVICES=0
        # os.environ['CUDA_VISIBLE_DEVICES'] = 'GPU-93779944-3708-cb7b-b6f1-cf49656fe4aa'
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        os.environ['OLLAMA_USE_GPU'] = '1'
        
        print(f"Ollama 실행 모드: {{'GPU' if use_gpu else 'CPU'}}")

        start_time = time.time()
        res = ollama.chat(
            model=model_name,
            messages=messages,
            options=ollama_options
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # print(res)
        return res['message']['content'], response_time
    except Exception as e:
        return f"오류 발생: {e}", 0

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

def main():
    """
    스크립트의 메인 실행 함수. 커맨드 라인 인자를 파싱하고 다운로드를 시작합니다.
    """
    parser = argparse.ArgumentParser(description="AI Chat")
    
    # --youtube와 --video를 상호 배타적인 인수로 설정
    """
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--prompt", 
        help="Path to the prompt file."
    )
    """
    
    parser.add_argument("--output", default="./result/result.md", help="Path to the output file.")
    parser.add_argument("--prompt", default="./prompt/prompt.md", help="Path to the prompt file or direct text.")
    parser.add_argument("--ref_prompt", default="", help="Path to the prompt file or direct text.")
    parser.add_argument("--system_prompt", default="", help="Path to the system prompt file or direct text.")
    parser.add_argument("--model", default="gemini", help="AI model to use ('ollama' or 'gemini').")
    parser.add_argument("--ollama_model_name", default="gpt-oss:20b", help="Ollama model name to use.")
    parser.add_argument("--gemini_model_name", default="gemini-2.5-flash", help="Gemini model name to use.")
    parser.add_argument("--cpu", action='store_true', help="Force CPU usage for Ollama.")

    args = parser.parse_args()

    try:
        # Read system prompt or use as text
        system_prompt = _read_or_use_text(args.system_prompt)
        ref_prompt = _read_or_use_text(args.ref_prompt)

        # Read user prompt or use as text
        user_prompt = _read_or_use_text(args.prompt)
        # print(f"11 {user_prompt}")
        if ref_prompt:
            user_prompt = f"## 참고 정보 : {ref_prompt} ## 요청 정보 : {user_prompt}"
        # print(f"22 {args.subprompt}")
        # print(f"user_prompt : {user_prompt}")
        
        if not user_prompt.strip():
            print("오류: AI에 전달할 프롬프트 내용이 비어 있습니다. --prompt 또는 --subprompt 인자를 확인해주세요.")
            sys.exit(1)

        # print(f"DEBUG: user_prompt length: {len(user_prompt)}")
        # print(f"DEBUG: system_prompt length: {len(system_prompt)}")

        # Get chat completion
        modelnm = args.ollama_model_name if args.model == 'ollama' else args.gemini_model_name
        with Spinner(f"AI({args.model} {modelnm}) 요청중... "):
            if args.model == 'ollama':
                # --cpu 플래그가 있으면 GPU를 사용하지 않음 (use_gpu=False)
                use_gpu = not args.cpu
                response, response_time = chat(user_prompt, system_prompt, model_name=args.ollama_model_name, use_gpu=use_gpu)
            else:
                response, response_time = gemini(user_prompt, system_prompt, model_name=args.gemini_model_name)
        print(f"응답 시간: {response_time:.2f}초")

        # Save result to file
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(response)
        
        print(f"결과가 '{args.output}' 파일에 저장되었습니다.")

    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
