import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
import re

# 환경변수
import os
from dotenv import load_dotenv
dotenv_file=".env.ai"
load_dotenv(dotenv_path=dotenv_file)

"""
    use example

    geminiai = GeminiAI()
    response = geminiai.chat(
        model_name="gemini-2.5-flash-preview-04-17",
        system_instruction=data['system_prompt'],
        generation_config = {
            "temperature": 0,
            "top_p": 0,
            "top_k": 64,
            "max_output_tokens": 65536,
            "response_mime_type": "text/plain",
        },
        prompt=json.dumps(data['base_prompt']), 
    )
"""
class GeminiAI:
    api_key = None
    client = None
    history = []

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.configure(api_key=self.api_key)
        self.history = []

    def history_init(self):
        self.history = []

    def chat(self, prompt, model_name=None, system_instruction=None, generation_config=None):
        if model_name == None:
            model_name = "gemini-2.5-flash-preview-04-17"
        
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            system_instruction=system_instruction,
            safety_settings=safety_settings
        )
        
        chat_session = model.start_chat(history=self.history)
        response = chat_session.send_message(prompt)
        self.history.append({"role": "user", "parts": prompt})
        
        try:
            return response.text
        except ValueError as e:
            print(f"Error accessing response.text: {e}")
            print(f"Full response object: {response}")
            # Check if there are candidates and a finish_reason
            if response.candidates:
                finish_reason = response.candidates[0].finish_reason
                return f"오류 발생: Gemini API가 빈 응답을 반환했습니다. Finish reason: {finish_reason}. 프롬프트 내용이나 안전 설정에 문제가 있을 수 있습니다."
            else:
                return f"오류 발생: Gemini API가 빈 응답을 반환했습니다. 응답에 후보가 없습니다."