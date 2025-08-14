import ollama
import time
import requests
import os
import argparse

from ai.GeminiAI import GeminiAI

ollama_model_name="gpt-oss:20b"
system_prompt_file="./prompt/영상요약프롬프트.md"
prompt_file="./downloads/YC1V4EeX5Q8.srt"
result_file="./result/YC1V4EeX5Q8.md"

def chat(chatmsg, system_prompt="", model_name="gpt-oss:20b", temperature=0.5, use_gpu=True):
    try:
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
            'num_gpu': 1 if use_gpu else 0  
        }
        
        print(f"Ollama 실행 모드: {'GPU' if use_gpu else 'CPU'}")

        start_time = time.time()
        res = ollama.chat(
            model=ollama_model_name,
            messages=messages,
            options=ollama_options
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        # print(res)
        return res['message']['content'], response_time
    except Exception as e:
        return f"오류 발생: {e}", 0

def gemini(chatmsg,system_prompt="", model_name="gemini-2.5-pro",temperature=0.5):
    try:
        start_time = time.time()
        
        geminiai = GeminiAI()
        res = geminiai.chat(
            model_name=model_name,
            system_instruction=system_prompt,
            prompt=chatmsg, 
        )

        end_time = time.time()
        response_time = end_time - start_time
        
        # print(res)
        return res, response_time
    except Exception as e:
        return f"오류 발생: {e}", 0

def main():
    parser = argparse.ArgumentParser(description="AI Chat using Ollama or Gemini.")
    parser.add_argument("--input", required=True, help="Path to the input file (e.g., subtitle file).")
    parser.add_argument("--system_prompt", default="./prompt/영상요약프롬프트.md", help="Path to the system prompt file.")
    parser.add_argument("--model", default="ollama", help="AI model to use ('ollama' or 'gemini').")
    parser.add_argument("--ollama_model_name", default="gpt-oss:20b", help="Ollama model name to use.")
    parser.add_argument("--gemini_model_name", default="gemini-2.5-pro", help="Gemini model name to use.")
    parser.add_argument("--cpu", action='store_true', help="Force CPU usage for Ollama.")
    
    args = parser.parse_args()
    
    try:
        # Read system prompt
        # with open(system_prompt_file, 'r', encoding='utf-8') as f:
        with open(args.system_prompt, 'r', encoding='utf-8') as f:
            system_prompt = f.read()

        # Read user prompt
        with open(args.input, 'r', encoding='utf-8') as f:
        # with open(prompt_file, 'r', encoding='utf-8') as f:
            user_prompt = f.read()

        # Get chat completion
        print("AI 요청중...")
        if args.model == 'ollama':
            # --cpu 플래그가 있으면 GPU를 사용하지 않음 (use_gpu=False)
            use_gpu = not args.cpu
            response, response_time = chat(user_prompt, system_prompt, model_name=args.ollama_model_name, use_gpu=use_gpu)
        else:
            response, response_time = gemini(user_prompt, system_prompt, model_name=args.gemini_model_name)
        print(f"응답 시간: {response_time:.2f}초")

        # Save result to file
        with open(result_file, 'w', encoding='utf-8') as f:
            f.write(response)
        
        print(f"결과가 '{result_file}' 파일에 저장되었습니다.")

    except FileNotFoundError as e:
        print(f"오류: 파일을 찾을 수 없습니다 - {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()
