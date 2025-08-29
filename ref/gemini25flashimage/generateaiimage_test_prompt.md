
아래는 제공되는 코드 샘플이야 코드 적용해서 수정해줘
파라미터로 이미지파일을 받아서 base64로 변환해서 처리되는 형식으로 처리
파라미터로 프롬프트를 받아서 해당 이미지를 프롬프트 적용해서 이미지 생성
파라미터로 저장 경로를 받아서 생성된 이미지를 파일로 저장
코드 생성해줘
 - 실행예 : uv run generateAiImage.py --image genimgsrc.jpeg --prompt "머리를 빨간색으로 염색해줘"

```python

import base64 import mimetypes import os from google import genai from google.genai import types def save_binary_file(file_name, data): f = open(file_name, "wb") f.write(data) f.close() print(f"File saved to to: {file_name}") def generate(): client = genai.Client( api_key=os.environ.get("GEMINI_API_KEY"), ) model = "gemini-2.5-flash-image-preview" contents = [ types.Content( role="user", parts=[ types.Part.from_bytes( mime_type="image/jpeg", data=base64.b64decode( """/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8QEBEQCgwSExIQEw8Q+ds5N4p/+5x99ZJIGDHRoePZipnQ3eBF0/6dzr8Oxej9y/F7r8Sf3ApSn3sC9E9wMTTQfzLxCFefzV2H/DxfPgu8CJg.......NP50ivSXLaJDsaupt9DLg15E88tqfVLDQCWOtU6xts8bCWQNAPZY8bO/2/ncFdMzn8+9eN383NX5576Yf/HGwoFO+28+mX360/mDnY5skj08WByADQrplcrmTrZXzSRrrCuNro1Gu0hdzi8itPv5Hwd/2PHZ945+9KOzn//w5Cff7/jkB6c/+f7Jj39w6qPvnfz0xxc7n/zT0G/em3jmI8P/D2ytMSMFsFsAAAAAAElFTkSuQmCC""" ), ), ], ), types.Content( role="user", parts=[ types.Part.from_text(text="""INSERT_INPUT_HERE"""), ], ), ] generate_content_config = types.GenerateContentConfig( response_modalities=[ "IMAGE", "TEXT", ], ) file_index = 0 for chunk in client.models.generate_content_stream( model=model, contents=contents, config=generate_content_config, ): if ( chunk.candidates is None or chunk.candidates[0].content is None or chunk.candidates[0].content.parts is None ): continue if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data: file_name = f"ENTER_FILE_NAME_{file_index}" file_index += 1 inline_data = chunk.candidates[0].content.parts[0].inline_data data_buffer = inline_data.data file_extension = mimetypes.guess_extension(inline_data.mime_type) save_binary_file(f"{file_name}{file_extension}", data_buffer) else: print(chunk.text) if __name__ == "__main__": generate()
```
