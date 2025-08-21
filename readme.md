# 영상 자막 추출
## 목적
 - 자막 없는 외국 영화 추출해서 AI로 번역 돌려서 번역된 자막 만들기위해
 - 유튜브 영상 추출해서 AI로 내용 요약해서 확인하기위해

## ffmpeg 설치
 - https://ffmpeg.org/download.html
 - https://github.com/BtbN/FFmpeg-Builds/releases
 - download 후 환경변수 path에 bin 폴더 경로 추가

## 팟플레이어 다운로드 및 설치
 - https://potplayer.tv/
### 소리로 자막 생성 설치
 - https://infohelpful.com/%eb%8f%99%ec%98%81%ec%83%81-%ec%8b%a4%ec%8b%9c%ea%b0%84-%ec%9e%90%eb%a7%89-%ec%83%9d%ec%84%b1-%eb%b0%a9%eb%b2%95-%ec%b4%88%ea%b0%84%eb%8b%a8/
 - 팟플레이어 메뉴에서 [자막] → [소리로 자막 생성]으로 이동
<img src="./readme_src/Pasted image 20250712114705.png"/>
 - 다운로드 클릭하고 몇분후(모델을 다운로드 받는 시간소요) 재시도
 - 다운로드 정상적으로 되었는지 확인 : [자막] → [소리로 자막 생성] → [Whisper AI 엔진] → [엔진 폴더 열기]
<img src="./readme_src/Pasted image 20250805105050.png"/>
 - Whisper-Faster 폴더 들어가면
<img src="./readme_src/Pasted image 20250805105210.png"/>
 - 위 파일 참고 파일이 적은 경우 받는중 일수도 있습니다.
 - 다운로드 다 되었다면 Whisper-Faster 폴더 자체를 프로젝트로 복사합니다.
<img src="./readme_src/Pasted image 20250805105504.png"/>


## 실행(영상 자막파일 생성)
### 프로세스
 - 1-1. youtube 파라미터로 유튜브 videoId,url 값이 넘어온경우
	 - 영상 다운로드(기본값 480p 화질 다운로드)
	 - 오디오 추출로 진행
 - 1-2. video 파라미터로 영상 파일경로 값이 넘어온경우 바로 오디오 추출로 진행
 - 2. 영상 파일을 mp3 파일로 오디오 추출
 - 3. 오디오 파일로 소리로 자막 추출
 - downloads 폴더에 영상파일, 영상파일명.mp3, 영상파일명.srt 생성됨.
### 유튜브 영상
 - 자막 추출 실행
```
$ export PYTHONIOENCODING=utf-8

$ uv run extractVideoSubtitle.py --youtube e9S9Ai21wWo > logs/e9S9Ai21wWo.log
or
$ uv run extractVideoSubtitle.py --youtube https://www.youtube.com/watch?v=e9S9Ai21wWo > logs/e9S9Ai21wWo.log

$ tail -f logs/e9S9Ai21wWo.log
```

### 영상 파일
```
$ export PYTHONIOENCODING=utf-8
$ uv run extractVideoSubtitle.py --video "downloads/\[날씨\] 다시 전국 대부분 폭염 특보…곳곳에 소나기 ⧸ KBS  2025.08.05. \[S_TzW8DkCyE\].mkv"
```

### 유튜브 영상만 다운로드
 - 영상만 다운로드하고 자막추출은 하지 않습니다.
 - quality 옵션으로 화질을 선택할 수 있습니다.(기본값 720p)
```
$ export PYTHONIOENCODING=utf-8
$ uv run extractVideoSubtitle.py --download e9S9Ai21wWo --quality 1080p
```

## AI 요약 실행
 - 자막 추출 후 AI를 통해 내용을 요약합니다.
 - `--summary` 옵션을 추가하면 자막 생성 후 자동으로 AI 요약을 실행합니다.
 - 요약 결과는 `result` 폴더에 `{영상파일명}.md` 파일로 저장됩니다.
 - 기본 AI 모델은 `Gemini` 입니다. `Ollama` 모델을 사용하려면 `extractVideoSubtitle.py`의 `run_transcription` 함수 내 `summary_command`를 수정해야 합니다.

### 유튜브 영상 요약
```
$ export PYTHONIOENCODING=utf-8
$ uv run extractVideoSubtitle.py --summary --youtube e9S9Ai21wWo > logs/summary.log
```

### 로컬 영상 파일 요약
```
$ export PYTHONIOENCODING=utf-8
$ uv run extractVideoSubtitle.py --summary --video "downloads/\[날씨\] 다시 전국 대부분 폭염 특보…곳곳에 소나기 KBS  2025.08.05. \[S_TzW8DkCyE\].mkv"
```

### 자막파일로 요약
```
$ uv run aisummary.py --input downloads/S_TzW8DkCyE.srt --output result/S_TzW8DkCyE.md
```

### (Ollama 사용 시) CPU로 요약 실행
 - `aisummary.py`를 직접 호출하여 `--cpu`와 `--model ollama` 옵션을 사용할 수 있습니다.
```
$ uv run aisummary.py --input "downloads/영상파일명.srt" --model ollama --cpu
```
