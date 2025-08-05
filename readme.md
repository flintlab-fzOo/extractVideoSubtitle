
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
 - 1-1. code 파라미터로 유튜브 videoId 값이 넘어온경우
	 - 영상 다운로드(기본값 480p 화질 다운로드)
	 - 오디오 추출로 진행
 - 1-2. video 파라미터로 영상 파일경로 값이 넘어온경우 바로 오디오 추출로 진행
 - 2. 영상 파일을 mp3 파일로 오디오 추출
 - 3. 오디오 파일로 소리로 자막 추출
 - downloads 폴더에 영상파일, 영상파일명.mp3, 영상파일명.srt 생성됨.
### 유튜브 영상
 - 유튜브 영상에는 videoId 를 복사
	 - https://www.youtube.com/watch?v=S_TzW8DkCyE
	 - 위 URL 파라미터 v 값이 videoId
 - 자막 추출 실행
```
$ uv run extractVideoSubtitle.py --code S_TzW8DkCyE
```

### 영상 파일
```
$ uv run extractVideoSubtitle.py --video downloads/\[날씨\]\ 다시\ 전국\ 대부분\ 폭염\ 특보…곳곳에\ 소나기\ ⧸\ KBS\ \ 2025.08.05.\ \[S_TzW8DkCyE\].mkv
```