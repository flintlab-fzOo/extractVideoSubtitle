.\Whisper-Faster\whisper-faster.exe --batch_recursive 

자주 쓰는 Whisper-Faster 주요 옵션
1. 모델 지정
기본: small 또는 설치된 사전 지정 모델
예시:
Code
--model medium
크기별 성능: tiny < base < small < medium < large (클수록 정확하고 느림)
2. GPU 사용/연산 장치 지정
예시:
Code
--device cuda
CUDA가 깔린 NVIDIA GPU면 자동 감지하는 경우가 많지만, 명시적으로 쓸 수 있음.
CPU만 쓸 땐:
Code
--device cpu
3. 출력 형식 지정
예시:
Code
--output_format srt
txt, srt, vtt, lrc, json, tsv, all 등 다양
(여러 개 원하면 all)
4. 출력 폴더 지정
예시:
Code
--output_dir "C:\output"
지정 안 하면 입력 파일 폴더로 출력됨.
5. 결과 언어번역 or 자동 감지
언어 지정 고정 (한국어 오디오라면):
Code
--language ko
번역 (영어로):
Code
--task translate
자동감지하고 텍스트 추출: 기본값.
6. 시간정보 포함(워드타임스탬프)
Code
--word_timestamps
단어 단위 타임스탬프 정보 함께 출력(srt 아닐 때 유용)
7. 처리 성능(스레드, 배치, chunk)
스레드 수(고성능 CPU에서):
Code
--threads 8
chunk 길이(짧게 끊어 처리):
Code
--chunk_length 30
→ 초 단위, 길수록 메모리 많이, 짧을수록 쪼개서 정확성 높임
8. VAD(음성활동감지) 필터
소음 구간 등 자동으로 skip
Code
--vad_filter
9. 기타 자주 활용 예시 조합
영어로 번역해서 srt로 출력:
sh
.\Whisper-Faster\whisper-faster.exe --model large --output_format srt --task translate --language en "yourfile.mkv"
파일 여러 개 한번에 하위폴더까지:
sh
.\Whisper-Faster\whisper-faster.exe --batch_recursive --output_format all "C:\folder\to\transcribe"
GPU 강제 사용, 한국어 음성만 변환, 출력 txt+json:
sh
.\Whisper-Faster\whisper-faster.exe --device cuda --language ko --output_format all "yourfile.mkv"
옵션 빠른 목록
옵션	설명	예시
--model	모델 크기	--model medium-large
--device	연산장치(GPU/CPU)	--device cuda
--output_format	결과파일 형식	--output_format srt
--output_dir	결과 저장폴더	--output_dir "out"
--language	음성 언어 고정	--language ko
--task	번역/필사	--task translate (번역)
--word_timestamps	워드시각 포함	--word_timestamps
--vad_filter	음성구간만 자동처리	--vad_filter
--threads	CPU 스레드 개수	--threads 8
--chunk_length	분할 길이(초)	--chunk_length 30
--output_dir	출력폴더	--output_dir "C:\output"
--print_progress	작업진행률 표시	--print_progress


PS C:\workspace\ai-cli-prompts> .\Whisper-Faster\whisper-faster.exe --help
usage: whisper-faster.exe [-h] [--model MODEL] [--model_dir MODEL_DIR] [--device DEVICE] [--output_dir OUTPUT_DIR]
                          [--output_format {lrc,txt,text,vtt,srt,tsv,json,all}] [--verbose VERBOSE]
                          [--task {transcribe,translate}]
                          [--language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
                          [--language_detection_threshold LANGUAGE_DETECTION_THRESHOLD]
                          [--language_detection_segments LANGUAGE_DETECTION_SEGMENTS] [--temperature TEMPERATURE]
                          [--best_of BEST_OF] [--beam_size BEAM_SIZE] [--patience PATIENCE]
                          [--length_penalty LENGTH_PENALTY] [--repetition_penalty REPETITION_PENALTY]
                          [--no_repeat_ngram_size NO_REPEAT_NGRAM_SIZE] [--suppress_blank SUPPRESS_BLANK]
                          [--suppress_tokens SUPPRESS_TOKENS] [--initial_prompt INITIAL_PROMPT] [--prefix PREFIX]
                          [--condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT]
                          [--prompt_reset_on_temperature PROMPT_RESET_ON_TEMPERATURE]
                          [--without_timestamps WITHOUT_TIMESTAMPS] [--max_initial_timestamp MAX_INITIAL_TIMESTAMP]
                          [--temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK]
                          [--compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD]
                          [--logprob_threshold LOGPROB_THRESHOLD] [--no_speech_threshold NO_SPEECH_THRESHOLD]
                          [--v3_offsets_off] [--hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD]
                          [--hallucination_silence_th_temp {0.0,0.2,0.5,0.8,1.0}] [--clip_timestamps CLIP_TIMESTAMPS]
                          [--no_speech_strict_lvl {0,1,2}] [--word_timestamps WORD_TIMESTAMPS]
                          [--highlight_words HIGHLIGHT_WORDS] [--prepend_punctuations PREPEND_PUNCTUATIONS]
                          [--append_punctuations APPEND_PUNCTUATIONS] [--threads THREADS] [--version]
                          [--vad_filter VAD_FILTER] [--vad_threshold VAD_THRESHOLD]
                          [--vad_min_speech_duration_ms VAD_MIN_SPEECH_DURATION_MS]
                          [--vad_max_speech_duration_s VAD_MAX_SPEECH_DURATION_S]
                          [--vad_min_silence_duration_ms VAD_MIN_SILENCE_DURATION_MS]
                          [--vad_speech_pad_ms VAD_SPEECH_PAD_MS] [--vad_window_size_samples VAD_WINDOW_SIZE_SAMPLES]
                          [--vad_dump] [--max_new_tokens MAX_NEW_TOKENS] [--chunk_length CHUNK_LENGTH]
                          [--compute_type {default,auto,int8,int8_float16,int8_float32,int8_bfloat16,int16,float16,float32,bfloat16}]
                          [--batch_recursive] [--beep_off] [--skip] [--checkcuda] [--print_progress] [--postfix]
                          [--check_files] [--PR163_off] [--hallucinations_list_off] [--one_word {0,1,2}] [--sentence]
                          [--standard] [--standard_asia] [--max_comma MAX_COMMA]
                          [--max_comma_cent {50,60,70,80,90,100}] [--max_gap MAX_GAP]
                          [--max_line_width MAX_LINE_WIDTH] [--max_line_count MAX_LINE_COUNT]
                          [--min_dist_to_end {0,4,5,6,7,8,9,10,11,12}] [--prompt_max {16,32,64,128,223}]
                          [--reprompt {0,1,2}] [--prompt_reset_on_no_end {0,1,2}] [--ff_dump]
                          [--ff_track {1,2,3,4,5,6}] [--ff_fc] [--ff_mp3] [--ff_sync] [--ff_rnndn_sh]
                          [--ff_rnndn_xiph] [--ff_fftdn [0 - 97]] [--ff_tempo [0.5 - 2.0]] [--ff_gate]
                          [--ff_speechnorm] [--ff_loudnorm] [--ff_silence_suppress noise duration] [--ff_lowhighpass]
                          audio [audio ...]

positional arguments:
  audio                 audio file(s). You can enter a file wildcard, filelist (txt. m3u, m3u8, lst) or directory to
                        do batch processing. Note: non-media files in list or directory are filtered out by extension.

optional arguments:
  -h, --help            show this help message and exit
  --model MODEL, -m MODEL
                        name of the Whisper model to use (default: medium)
  --model_dir MODEL_DIR
                        the path to save model files; uses C:\workspace\ai-cli-prompts\Whisper-Faster\_models by
                        default (default: None)
  --device DEVICE, -d DEVICE
                        Device to use. Default is 'cuda' if CUDA device is detected, else is 'cpu'. If CUDA GPU is a
                        second device then set 'cuda:1'. (default: cuda)
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        directory to save the outputs. By default the same folder where the executable file is or
                        where media file is if --batch_recursive=True. '.'- sets to the current folder. 'source' -
                        sets to where media file is. (default: default)
  --output_format {lrc,txt,text,vtt,srt,tsv,json,all}, -f {lrc,txt,text,vtt,srt,tsv,json,all}
                        format of the output file; if not specified srt will be produced (default: srt)
  --verbose VERBOSE, -v VERBOSE
                        whether to print out debug messages (default: False)
  --task {transcribe,translate}
                        whether to perform X->X speech recognition ('transcribe') or X->English translation
                        ('translate') (default: transcribe)
  --language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}, -l {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}
                        language spoken in the audio, specify None to perform language detection (default: None)
  --language_detection_threshold LANGUAGE_DETECTION_THRESHOLD
                        If the maximum probability of the language tokens is higher than this value, the language is
                        detected. (default: None)
  --language_detection_segments LANGUAGE_DETECTION_SEGMENTS
                        Number of segments/chunks to consider for the language detection. (default: 1)
  --temperature TEMPERATURE
                        temperature to use for sampling (default: 0)
  --best_of BEST_OF, -bo BEST_OF
                        number of candidates when sampling with non-zero temperature (default: 5)
  --beam_size BEAM_SIZE, -bs BEAM_SIZE
                        number of beams in beam search, only applicable when temperature is zero (default: 5)
  --patience PATIENCE, -p PATIENCE
                        optional patience value to use in beam decoding, as in https://arxiv.org/abs/2204.05424, the
                        default (1.0) is equivalent to conventional beam search (default: 2.0)
  --length_penalty LENGTH_PENALTY
                        optional token length penalty coefficient (alpha) as in https://arxiv.org/abs/1609.08144, uses
                        simple length normalization by default (default: 1.0)
  --repetition_penalty REPETITION_PENALTY
                        Penalty applied to the score of previously generated tokens (set > 1.0 to penalize). (default:
                        1.0)
  --no_repeat_ngram_size NO_REPEAT_NGRAM_SIZE
                        Prevent repetitions of ngrams with this size (set 0 to disable). (default: 0)
  --suppress_blank SUPPRESS_BLANK
                        Suppress blank outputs at the beginning of the sampling. (default: True)
  --suppress_tokens SUPPRESS_TOKENS
                        comma-separated list of token ids to suppress during sampling; '-1' will suppress most special
                        characters except common punctuations (default: -1)
  --initial_prompt INITIAL_PROMPT, -prompt INITIAL_PROMPT
                        optional text to provide context as a prompt for the first window. Use 'None' to disable it.
                        Note: 'auto' and 'default' are experimental ~universal prompt presets, they work if --language
                        is set. (default: auto)
  --prefix PREFIX       Optional text to provide as a prefix for the first window (default: None)
  --condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT, -condition CONDITION_ON_PREVIOUS_TEXT
                        if True, provide the previous output of the model as a prompt for the next window; disabling
                        may make the text inconsistent across windows, but the model becomes less prone to getting
                        stuck in a failure loop. If disabled then you may want to disable --reprompt too. (default:
                        True)
  --prompt_reset_on_temperature PROMPT_RESET_ON_TEMPERATURE
                        Resets prompt if temperature is above this value. Arg has effect only if
                        condition_on_previous_text is True. (default: 0.5)
  --without_timestamps WITHOUT_TIMESTAMPS
                        Only sample text tokens. (default: False)
  --max_initial_timestamp MAX_INITIAL_TIMESTAMP
                        The initial timestamp cannot be later than this. (default: 1.0)
  --temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK, -fallback TEMPERATURE_INCREMENT_ON_FALLBACK
                        temperature to increase when falling back when the decoding fails to meet either of the
                        thresholds below. To disable fallback set it to 'None'. (default: 0.2)
  --compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD
                        if the gzip compression ratio is higher than this value, treat the decoding as failed
                        (default: 2.4)
  --logprob_threshold LOGPROB_THRESHOLD
                        if the average log probability is lower than this value, treat the decoding as failed
                        (default: -1.0)
  --no_speech_threshold NO_SPEECH_THRESHOLD
                        if the probability of the <|nospeech|> token is higher than this value AND the decoding has
                        failed due to 'logprob_threshold', consider the segment as silence (default: 0.6)
  --v3_offsets_off      Disables custom offsets to the defaults of pseudo-vad thresholds when 'large-v3' models are in
                        use. Note: Offsets made to combat 'large-v3' hallucinations. (default: False)
  --hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD, -hst HALLUCINATION_SILENCE_THRESHOLD
                        (Experimental) When word_timestamps is True, skip silent periods longer than this threshold
                        (in seconds) when a possible hallucination is detected. Optimal value is somewhere between 2 -
                        8 seconds. Inactive if None. (default: None)
  --hallucination_silence_th_temp {0.0,0.2,0.5,0.8,1.0}, -hst_temp {0.0,0.2,0.5,0.8,1.0}
                        (Experimental) Additional heuristic for '--hallucination_silence_threshold'. If temperature is
                        higher that this threshold then consider segment as possible hallucination ignoring the hst
                        score. Inactive if 1.0. (default: 1.0)
  --clip_timestamps CLIP_TIMESTAMPS
                        Comma-separated list start,end,start,end,... timestamps (in seconds) of clips to process. The
                        last end timestamp defaults to the end of the file. VAD is auto-disabled. (default: 0)
  --no_speech_strict_lvl {0,1,2}
                        (experimental) Level of stricter actions when no_speech_prob > 0.93. Use beam_size=5 if this
                        is enabled. Options: 0 - Disabled (do nothing), 1 - Reset propmt (see
                        condition_on_previous_text), 2 - Invalidate the cached encoder output (if no_speech_threshold
                        is not None). Arg meant to combat cases where the model is getting stuck in a failure loop or
                        outputs nonsense (default: 0)
  --word_timestamps WORD_TIMESTAMPS, -wt WORD_TIMESTAMPS
                        Extract word-level timestamps and refine the results based on them (default: True)
  --highlight_words HIGHLIGHT_WORDS, -hw HIGHLIGHT_WORDS
                        underline each word as it is spoken AKA karaoke in srt and vtt output formats (default: False)
  --prepend_punctuations PREPEND_PUNCTUATIONS
                        if word_timestamps is True, merge these punctuation symbols with the next word (default:
                        "'“¿([{-)
  --append_punctuations APPEND_PUNCTUATIONS
                        if word_timestamps is True, merge these punctuation symbols with the previous word (default:
                        "'.。,，!！?？:：”)]}、)
  --threads THREADS     number of threads used for CPU inference; By default number of the real cores but no more that
                        4 (default: 0)
  --version             Show Faster-Whisper's version number
  --vad_filter VAD_FILTER, -vad VAD_FILTER
                        Enable the voice activity detection (VAD) to filter out parts of the audio without speech.
                        (default: True)
  --vad_threshold VAD_THRESHOLD
                        Probabilities above this value are considered as speech. (default: 0.45)
  --vad_min_speech_duration_ms VAD_MIN_SPEECH_DURATION_MS
                        Final speech chunks shorter min_speech_duration_ms are thrown out. (default: 350)
  --vad_max_speech_duration_s VAD_MAX_SPEECH_DURATION_S
                        Maximum duration of speech chunks in seconds. Longer will be split at the timestamp of the
                        last silence. (default: None)
  --vad_min_silence_duration_ms VAD_MIN_SILENCE_DURATION_MS
                        In the end of each speech chunk time to wait before separating it. (default: 3000)
  --vad_speech_pad_ms VAD_SPEECH_PAD_MS
                        Final speech chunks are padded by speech_pad_ms each side. (default: 900)
  --vad_window_size_samples VAD_WINDOW_SIZE_SAMPLES
                        Size of audio chunks fed to the silero VAD model. Values other than 512, 1024, 1536 may affect
                        model perfomance!!! (default: 1536)
  --vad_dump            Dumps VAD timings to a subtitle file for inspection. (default: False)
  --max_new_tokens MAX_NEW_TOKENS
                        Maximum number of new tokens to generate per-chunk. (default: None)
  --chunk_length CHUNK_LENGTH
                        The length of audio segments. If it is not None, it will overwrite the default chunk_length of
                        the FeatureExtractor. (default: None)
  --compute_type {default,auto,int8,int8_float16,int8_float32,int8_bfloat16,int16,float16,float32,bfloat16}, -ct {default,auto,int8,int8_float16,int8_float32,int8_bfloat16,int16,float16,float32,bfloat16}
                        Type of quantization to use (see https://opennmt.net/CTranslate2/quantization.html). (default:
                        auto)
  --batch_recursive, -br
                        Enables recursive batch processing. Note: If set then it changes defaults of --output_dir.
                        (default: False)
  --beep_off            Disables the beep sound when operation is finished. (default: False)
  --skip                Skips media file if subtitle exists. Works if input is wildcard or directory. (default: False)
  --checkcuda, -cc      Returns CUDA device count. (for Subtitle Edit's internal use)
  --print_progress, -pp
                        Prints progress bar instead of transcription. (default: False)
  --postfix             Adds language as a postfix to subtitle's filename. (default: False)
  --check_files         Checks input files for errors before passing all them for transcription. Works if input is
                        wildcard or directory. (default: False)
  --PR163_off           (For dev experiments) Disables PR163. . (default: False)
  --hallucinations_list_off
                        (For dev experiments) Disables hallucinations_list, allows hallucinations added to prompt.
                        (default: False)
  --one_word {0,1,2}    0) Disabled. 1) Outputs srt and vtt subtitles with one word per line. 2) As '1', plus removes
                        whitespace and ensures >= 50ms for sub lines. Note: VAD may slightly reduce the accuracy of
                        timestamps on some lines. (default: 0)
  --sentence            Enables splitting lines to sentences for srt and vtt subs. Every sentence starts in the new
                        segment. By default meant to output whole sentence per line for better translations, but not
                        limited to, read about '--max_...' parameters. Note: has no effect on 'highlight_words'.
                        (default: False)
  --standard            Quick hardcoded preset to split lines in standard way. 42 chars per 2 lines with
                        max_comma_cent=70 and --sentence are activated automatically. (default: False)
  --standard_asia       Quick hardcoded preset to split lines in standard way for some Asian languages. 16 chars per 2
                        lines with max_comma_cent=80 and --sentence are activated automatically. (default: False)
  --max_comma MAX_COMMA
                        (requires --sentence) After this line length a comma is treated as the end of sentence. Note:
                        disabled if it's over or equal to --max_line_width. (default: 250)
  --max_comma_cent {50,60,70,80,90,100}
                        (requires --sentence) Percentage of --max_line_width when it starts breaking the line after
                        comma. Note: 100 = disabled. (default: 100)
  --max_gap MAX_GAP     (requires --sentence) Threshold for a gap length in seconds, longer gaps are treated as dots.
                        (default: 3.0)
  --max_line_width MAX_LINE_WIDTH
                        The maximum number of characters in a line before breaking the line. (default: 1000)
  --max_line_count MAX_LINE_COUNT
                        The maximum number of lines in one sub segment. (default: 1)
  --min_dist_to_end {0,4,5,6,7,8,9,10,11,12}
                        (requires --sentence) If from words like 'the', 'Mr.' and ect. to the end of line distance is
                        less than set then it starts in a new line. Note: 0 = disabled. (default: 0)
  --prompt_max {16,32,64,128,223}
                        (experimental) The maximum size of prompt. (default: 223)
  --reprompt {0,1,2}    (experimental) 0) Disabled. 1) Inserts initial_prompt after the prompt resets. 2) Ensures that
                        initial_prompt is present in prompt for all windows/chunks. Note: auto-disabled if
                        initial_prompt=None. It's similar to 'hotwords' feature. (default: 2)
  --prompt_reset_on_no_end {0,1,2}
                        (experimental) Resets prompt if there is no end of sentence in window/chunk. 0 - disabled, 1 -
                        looks for period, 2 - looks for period or comma. Note: it's auto-disabled if reprompt=0.
                        (default: 2)
  --ff_dump             Dumps pre-processed audio by the filters to the 16000Hz file and prevents deletion of some
                        intermediate audio files. (default: False)
  --ff_track {1,2,3,4,5,6}
                        Audio track selector. 1 - selects the first audio track. (default: 1)
  --ff_fc               Selects only front-center channel (FC) to process. (default: False)
  --ff_mp3              Audio filter: Conversion to MP3 and back. (default: False)
  --ff_sync             Audio filter: Stretch/squeeze samples to the given timestamps, with a maximum of 3600 samples
                        per second compensation. Input file must be container that support storing PTS like mp4,
                        mkv... (default: False)
  --ff_rnndn_sh         Audio filter: Suppress non-speech with GregorR's SH model using Recurrent Neural Networks.
                        Notes: It's more aggressive than Xiph, discards singing. (default: False)
  --ff_rnndn_xiph       Audio filter: Suppress non-speech with Xiph's original model using Recurrent Neural Networks.
                        (default: False)
  --ff_fftdn [0 - 97]   Audio filter: General denoise with Fast Fourier Transform. Notes: 12 - normal strength, 0 -
                        disabled. (default: 0)
  --ff_tempo [0.5 - 2.0]
                        Audio filter: Adjust audio tempo. Values below 1.0 slows down audio, above - speeds up. 1.0 =
                        disabled. (default: 1.0)
  --ff_gate             Audio filter: Reduce lower parts of a signal. (default: False)
  --ff_speechnorm       Audio filter: Extreme and fast speech amplification. (default: False)
  --ff_loudnorm         Audio filter: EBU R128 loudness normalization. (default: False)
  --ff_silence_suppress noise duration
                        Audio filter: Suppress quiet parts of audio. Takes two values. First value - noise tolerance
                        in decibels [-70 - 0] (0=disabled), second value - minimum silence duration in seconds [0.1 -
                        10]. (default: [0, 3.0])
  --ff_lowhighpass      Audio filter: Pass 50Hz - 7800 band. sinc + afir. (default: False)



PS C:\workspace\ai-cli-prompts> .\Whisper-Faster\whisper-faster.exe --help
사용법: whisper-faster.exe [-h] [--model 모델] [--model_dir 모델_디렉토리] [--device 장치] [--output_dir 출력_디렉토리]
                          [--output_format {lrc,txt,text,vtt,srt,tsv,json,all}] [--verbose 상세_출력]
                          [--task {transcribe,translate}]
                          [--language {af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,yi,yo,yue,zh,Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,Cantonese,Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,Maltese,Mandarin,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,Yoruba}]
                          [--language_detection_threshold 언어_감지_임계값]
                          [--language_detection_segments 언어_감지_세그먼트] [--temperature 온도]
                          [--best_of BEST_OF] [--beam_size BEAM_SIZE] [--patience 인내심]
                          [--length_penalty 길이_패널티] [--repetition_penalty 반복_패널티]
                          [--no_repeat_ngram_size NO_REPEAT_NGRAM_SIZE] [--suppress_blank 공백_억제]
                          [--suppress_tokens 토큰_억제] [--initial_prompt 초기_프롬프트] [--prefix 접두사]
                          [--condition_on_previous_text 이전_텍스트_조건화]
                          [--prompt_reset_on_temperature 온도에_따른_프롬프트_재설정]
                          [--without_timestamps 타임스탬프_없음] [--max_initial_timestamp 최대_초기_타임스탬프]
                          [--temperature_increment_on_fallback 폴백시_온도_증가]
                          [--compression_ratio_threshold 압축_비율_임계값]
                          [--logprob_threshold 로그_확률_임계값] [--no_speech_threshold 무음_임계값]
                          [--v3_offsets_off] [--hallucination_silence_threshold 환각_침묵_임계값]
                          [--hallucination_silence_th_temp {0.0,0.2,0.5,0.8,1.0}] [--clip_timestamps 클립_타임스탬프]
                          [--no_speech_strict_lvl {0,1,2}] [--word_timestamps 단어_타임스탬프]
                          [--highlight_words 단어_강조] [--prepend_punctuations 앞에_붙는_구두점]
                          [--append_punctuations 뒤에_붙는_구두점] [--threads 스레드] [--version]
                          [--vad_filter VAD_필터] [--vad_threshold VAD_임계값]
                          [--vad_min_speech_duration_ms VAD_최소_음성_지속시간_ms]
                          [--vad_max_speech_duration_s VAD_최대_음성_지속시간_s]
                          [--vad_min_silence_duration_ms VAD_최소_침묵_지속시간_ms]
                          [--vad_speech_pad_ms VAD_음성_패딩_ms] [--vad_window_size_samples VAD_창_크기_샘플]
                          [--vad_dump] [--max_new_tokens 최대_새_토큰] [--chunk_length 청크_길이]
                          [--compute_type {default,auto,int8,int8_float16,int8_float32,int8_bfloat16,int16,float16,float32,bfloat16}]
                          [--batch_recursive] [--beep_off] [--skip] [--checkcuda] [--print_progress] [--postfix]
                          [--check_files] [--PR163_off] [--hallucinations_list_off] [--one_word {0,1,2}] [--sentence]
                          [--standard] [--standard_asia] [--max_comma 최대_쉼표]
                          [--max_comma_cent {50,60,70,80,90,100}] [--max_gap 최대_간격]
                          [--max_line_width 최대_줄_너비] [--max_line_count 최대_줄_수]
                          [--min_dist_to_end {0,4,5,6,7,8,9,10,11,12}] [--prompt_max {16,32,64,128,223}]
                          [--reprompt {0,1,2}] [--prompt_reset_on_no_end {0,1,2}] [--ff_dump]
                          [--ff_track {1,2,3,4,5,6}] [--ff_fc] [--ff_mp3] [--ff_sync] [--ff_rnndn_sh]
                          [--ff_rnndn_xiph] [--ff_fftdn [0 - 97]] [--ff_tempo [0.5 - 2.0]] [--ff_gate]
                          [--ff_speechnorm] [--ff_loudnorm] [--ff_silence_suppress noise duration] [--ff_lowhighpass]
                          audio [audio ...]

위치 인수:
  audio                 오디오 파일. 파일 와일드카드, 파일 목록(txt, m3u, m3u8, lst) 또는 디렉토리를 입력하여
                        일괄 처리를 수행할 수 있습니다. 참고: 목록이나 디렉토리의 미디어 파일이 아닌 파일은 확장자에 따라 필터링됩니다.

선택적 인수:
  -h, --help            이 도움말 메시지를 표시하고 종료합니다.
  --model MODEL, -m MODEL
                        사용할 Whisper 모델의 이름 (기본값: medium)
  --model_dir MODEL_DIR
                        모델 파일을 저장할 경로. 기본적으로 C:\workspace\ai-cli-prompts\Whisper-Faster\_models 를 사용합니다. (기본값: 없음)
  --device DEVICE, -d DEVICE
                        사용할 장치. CUDA 장치가 감지되면 기본값은 'cuda'이고, 그렇지 않으면 'cpu'입니다. CUDA GPU가
                        두 번째 장치인 경우 'cuda:1'로 설정합니다. (기본값: cuda)
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        출력물을 저장할 디렉토리. 기본적으로 실행 파일이 있는 폴더 또는
                        --batch_recursive=True인 경우 미디어 파일이 있는 폴더입니다. '.' - 현재 폴더로 설정합니다. 'source' -
                        미디어 파일이 있는 위치로 설정합니다. (기본값: default)
  --output_format {lrc,txt,text,vtt,srt,tsv,json,all}, -f {lrc,txt,text,vtt,srt,tsv,json,all}
                        출력 파일의 형식. 지정하지 않으면 srt가 생성됩니다. (기본값: srt)
  --verbose VERBOSE, -v VERBOSE
                        디버그 메시지를 출력할지 여부 (기본값: False)
  --task {transcribe,translate}
                        X->X 음성 인식('transcribe') 또는 X->영어 번역('translate')을 수행할지 여부 (기본값: transcribe)
  --language LANGUAGE, -l LANGUAGE
                        오디오에서 사용되는 언어. 언어 감지를 수행하려면 None을 지정합니다. (기본값: None)
  --language_detection_threshold LANGUAGE_DETECTION_THRESHOLD
                        언어 토큰의 최대 확률이 이 값보다 높으면 언어가 감지됩니다. (기본값: 없음)
  --language_detection_segments LANGUAGE_DETECTION_SEGMENTS
                        언어 감지를 위해 고려할 세그먼트/청크 수. (기본값: 1)
  --temperature TEMPERATURE
                        샘플링에 사용할 온도 (기본값: 0)
  --best_of BEST_OF, -bo BEST_OF
                        온도가 0이 아닌 샘플링 시 후보 수 (기본값: 5)
  --beam_size BEAM_SIZE, -bs BEAM_SIZE
                        빔 검색의 빔 수. 온도가 0일 때만 적용됩니다. (기본값: 5)
  --patience PATIENCE, -p PATIENCE
                        빔 디코딩에 사용할 선택적 인내심 값. https://arxiv.org/abs/2204.05424 에서처럼,
                        기본값(1.0)은 기존 빔 검색과 동일합니다. (기본값: 2.0)
  --length_penalty LENGTH_PENALTY
                        https://arxiv.org/abs/1609.08144 에서와 같은 선택적 토큰 길이 패널티 계수(알파).
                        기본적으로 간단한 길이 정규화를 사용합니다. (기본값: 1.0)
  --repetition_penalty REPETITION_PENALTY
                        이전에 생성된 토큰의 점수에 적용되는 패널티 (> 1.0으로 설정하여 패널티 부여). (기본값: 1.0)
  --no_repeat_ngram_size NO_REPEAT_NGRAM_SIZE
                        이 크기의 ngram 반복을 방지합니다 (비활성화하려면 0으로 설정). (기본값: 0)
  --suppress_blank SUPPRESS_BLANK
                        샘플링 시작 시 빈 출력을 억제합니다. (기본값: True)
  --suppress_tokens SUPPRESS_TOKENS
                        샘플링 중에 억제할 토큰 ID의 쉼표로 구분된 목록. '-1'은 일반적인 구두점을 제외한 대부분의 특수 문자를 억제합니다. (기본값: -1)
  --initial_prompt INITIAL_PROMPT, -prompt INITIAL_PROMPT
                        첫 번째 창에 대한 프롬프트로 컨텍스트를 제공하는 선택적 텍스트. 비활성화하려면 'None'을 사용합니다.
                        참고: 'auto' 및 'default'는 실험적인 ~범용 프롬프트 사전 설정이며, --language가 설정된 경우 작동합니다. (기본값: auto)
  --prefix PREFIX       첫 번째 창에 대한 접두사로 제공할 선택적 텍스트 (기본값: 없음)
  --condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT, -condition CONDITION_ON_PREVIOUS_TEXT
                        True인 경우, 모델의 이전 출력을 다음 창에 대한 프롬프트로 제공합니다.
                        비활성화하면 창 간에 텍스트가 일관되지 않을 수 있지만 모델이 실패 루프에 갇히는 경향이 줄어듭니다.
                        비활성화된 경우 --reprompt도 비활성화할 수 있습니다. (기본값: True)
  --prompt_reset_on_temperature PROMPT_RESET_ON_TEMPERATURE
                        온도가 이 값보다 높으면 프롬프트를 재설정합니다. condition_on_previous_text가 True인 경우에만 효과가 있습니다. (기본값: 0.5)
  --without_timestamps WITHOUT_TIMESTAMPS
                        텍스트 토큰만 샘플링합니다. (기본값: False)
  --max_initial_timestamp MAX_INITIAL_TIMESTAMP
                        초기 타임스탬프는 이보다 늦을 수 없습니다. (기본값: 1.0)
  --temperature_increment_on_fallback TEMPERATURE_INCREMENT_ON_FALLBACK, -fallback TEMPERATURE_INCREMENT_ON_FALLBACK
                        디코딩이 아래 임계값 중 하나를 충족하지 못하여 폴백할 때 증가할 온도.
                        폴백을 비활성화하려면 'None'으로 설정합니다. (기본값: 0.2)
  --compression_ratio_threshold COMPRESSION_RATIO_THRESHOLD
                        gzip 압축률이 이 값보다 높으면 디코딩을 실패로 처리합니다. (기본값: 2.4)
  --logprob_threshold LOGPROB_THRESHOLD
                        평균 로그 확률이 이 값보다 낮으면 디코딩을 실패로 처리합니다. (기본값: -1.0)
  --no_speech_threshold NO_SPEECH_THRESHOLD
                        <|nospeech|> 토큰의 확률이 이 값보다 높고 'logprob_threshold'로 인해 디코딩이 실패한 경우
                        해당 세그먼트를 무음으로 간주합니다. (기본값: 0.6)
  --v3_offsets_off      'large-v3' 모델 사용 시 의사-vad 임계값의 기본값에 대한 사용자 지정 오프셋을 비활성화합니다.
                        참고: 'large-v3' 환각 현상을 방지하기 위해 오프셋이 만들어졌습니다. (기본값: False)
  --hallucination_silence_threshold HALLUCINATION_SILENCE_THRESHOLD, -hst HALLUCINATION_SILENCE_THRESHOLD
                        (실험적) word_timestamps가 True일 때, 가능한 환각이 감지되면 이 임계값(초)보다 긴
                        무음 구간을 건너뜁니다. 최적 값은 2-8초 사이입니다. None이면 비활성화됩니다. (기본값: 없음)
  --hallucination_silence_th_temp {0.0,0.2,0.5,0.8,1.0}, -hst_temp {0.0,0.2,0.5,0.8,1.0}
                        (실험적) '--hallucination_silence_threshold'에 대한 추가 휴리스틱. 온도가 이 임계값보다 높으면
                        hst 점수를 무시하고 세그먼트를 가능한 환각으로 간주합니다. 1.0이면 비활성화됩니다. (기본값: 1.0)
  --clip_timestamps CLIP_TIMESTAMPS
                        처리할 클립의 시작,끝,시작,끝,... 타임스탬프(초)를 쉼표로 구분한 목록.
                        마지막 끝 타임스탬프는 파일의 끝으로 기본 설정됩니다. VAD는 자동으로 비활성화됩니다. (기본값: 0)
  --no_speech_strict_lvl {0,1,2}
                        (실험적) no_speech_prob > 0.93일 때 더 엄격한 조치 수준. 이 옵션을 활성화하면 beam_size=5를 사용하세요.
                        옵션: 0 - 비활성화(아무것도 안 함), 1 - 프롬프트 재설정(condition_on_previous_text 참조),
                        2 - 캐시된 인코더 출력 무효화(no_speech_threshold가 None이 아닌 경우).
                        모델이 실패 루프에 갇히거나 무의미한 출력을 내는 경우를 방지하기 위한 인수입니다. (기본값: 0)
  --word_timestamps WORD_TIMESTAMPS, -wt WORD_TIMESTAMPS
                        단어 수준 타임스탬프를 추출하고 이를 기반으로 결과를 구체화합니다. (기본값: True)
  --highlight_words HIGHLIGHT_WORDS, -hw HIGHLIGHT_WORDS
                        srt 및 vtt 출력 형식에서 단어가 말해질 때마다 밑줄을 긋습니다(일명 가라오케). (기본값: False)
  --prepend_punctuations PREPEND_PUNCTUATIONS
                        word_timestamps가 True인 경우, 이러한 구두점을 다음 단어와 병합합니다. (기본값: "'“¿([{-)
  --append_punctuations APPEND_PUNCTUATIONS
                        word_timestamps가 True인 경우, 이러한 구두점을 이전 단어와 병합합니다. (기본값: "'.。,，!！?？:：”)]}、)
  --threads THREADS     CPU 추론에 사용되는 스레드 수. 기본적으로 실제 코어 수이지만 4개를 넘지 않습니다. (기본값: 0)
  --version             Faster-Whisper의 버전 번호를 표시합니다.
  --vad_filter VAD_FILTER, -vad VAD_FILTER
                        음성 활동 감지(VAD)를 활성화하여 음성이 없는 오디오 부분을 필터링합니다. (기본값: True)
  --vad_threshold VAD_THRESHOLD
                        이 값보다 높은 확률은 음성으로 간주됩니다. (기본값: 0.45)
  --vad_min_speech_duration_ms VAD_MIN_SPEECH_DURATION_MS
                        min_speech_duration_ms보다 짧은 최종 음성 청크는 버려집니다. (기본값: 350)
  --vad_max_speech_duration_s VAD_MAX_SPEECH_DURATION_S
                        음성 청크의 최대 지속 시간(초). 더 길면 마지막 무음의 타임스탬프에서 분할됩니다. (기본값: 없음)
  --vad_min_silence_duration_ms VAD_MIN_SILENCE_DURATION_MS
                        각 음성 청크의 끝에서 분리하기 전에 기다리는 시간. (기본값: 3000)
  --vad_speech_pad_ms VAD_SPEECH_PAD_MS
                        최종 음성 청크는 양쪽에 speech_pad_ms만큼 패딩됩니다. (기본값: 900)
  --vad_window_size_samples VAD_WINDOW_SIZE_SAMPLES
                        silero VAD 모델에 입력되는 오디오 청크의 크기. 512, 1024, 1536 이외의 값은
                        모델 성능에 영향을 줄 수 있습니다!!! (기본값: 1536)
  --vad_dump            검사를 위해 VAD 타이밍을 자막 파일로 덤프합니다. (기본값: False)
  --max_new_tokens MAX_NEW_TOKENS
                        청크당 생성할 최대 새 토큰 수. (기본값: 없음)
  --chunk_length CHUNK_LENGTH
                        오디오 세그먼트의 길이. None이 아닌 경우 FeatureExtractor의 기본 chunk_length를 덮어씁니다. (기본값: 없음)
  --compute_type {default,auto,int8,int8_float16,int8_float32,int8_bfloat16,int16,float16,float32,bfloat16}, -ct {default,auto,int8,int8_float16,int8_float32,int8_bfloat16,int16,float16,float32,bfloat16}
                        사용할 양자화 유형 (https://opennmt.net/CTranslate2/quantization.html 참조). (기본값: auto)
  --batch_recursive, -br
                        재귀적 일괄 처리를 활성화합니다. 참고: 설정하면 --output_dir의 기본값이 변경됩니다. (기본값: False)
  --beep_off            작업이 완료되었을 때 경고음 비활성화. (기본값: False)
  --skip                자막이 존재하면 미디어 파일을 건너뜁니다. 입력이 와일드카드나 디렉토리인 경우 작동합니다. (기본값: False)
  --checkcuda, -cc      CUDA 장치 수를 반환합니다. (Subtitle Edit 내부용)
  --print_progress, -pp
                        전사 대신 진행률 표시줄을 인쇄합니다. (기본값: False)
  --postfix             자막 파일 이름에 언어를 접미사로 추가합니다. (기본값: False)
  --check_files         전사를 위해 모든 파일을 전달하기 전에 입력 파일에 오류가 있는지 확인합니다. 입력이 와일드카드나 디렉토리인 경우 작동합니다. (기본값: False)
  --PR163_off           (개발 실험용) PR163을 비활성화합니다. (기본값: False)
  --hallucinations_list_off
                        (개발 실험용) hallucinations_list를 비활성화하고, 프롬프트에 환각을 추가할 수 있도록 허용합니다. (기본값: False)
  --one_word {0,1,2}    0) 비활성화. 1) 한 줄에 한 단어씩 srt 및 vtt 자막을 출력합니다. 2) '1'과 같고, 공백을 제거하고
                        자막 라인에 대해 >= 50ms를 보장합니다. 참고: VAD는 일부 라인의 타임스탬프 정확도를 약간 감소시킬 수 있습니다. (기본값: 0)
  --sentence            srt 및 vtt 자막에 대해 줄을 문장으로 분할하는 것을 활성화합니다. 모든 문장은 새 세그먼트에서 시작됩니다.
                        기본적으로 더 나은 번역을 위해 한 줄에 전체 문장을 출력하도록 되어 있지만, 이에 국한되지 않으며 '--max_...' 매개변수에 대해 읽어보세요.
                        참고: 'highlight_words'에는 영향을 미치지 않습니다. (기본값: False)
  --standard            표준 방식으로 줄을 분할하는 빠른 하드코딩된 사전 설정. max_comma_cent=70 및 --sentence가 있는 2줄당 42자가 자동으로 활성화됩니다. (기본값: False)
  --standard_asia       일부 아시아 언어에 대해 표준 방식으로 줄을 분할하는 빠른 하드코딩된 사전 설정. max_comma_cent=80 및 --sentence가 있는 2줄당 16자가 자동으로 활성화됩니다. (기본값: False)
  --max_comma MAX_COMMA
                        ( --sentence 필요) 이 줄 길이 이후에는 쉼표가 문장의 끝으로 처리됩니다.
                        참고: --max_line_width보다 크거나 같으면 비활성화됩니다. (기본값: 250)
  --max_comma_cent {50,60,70,80,90,100}
                        ( --sentence 필요) 쉼표 뒤에서 줄을 바꾸기 시작하는 --max_line_width의 백분율.
                        참고: 100 = 비활성화. (기본값: 100)
  --max_gap MAX_GAP     ( --sentence 필요) 초 단위의 간격 길이에 대한 임계값. 더 긴 간격은 마침표로 처리됩니다. (기본값: 3.0)
  --max_line_width MAX_LINE_WIDTH
                        줄을 바꾸기 전 한 줄의 최대 문자 수. (기본값: 1000)
  --max_line_count MAX_LINE_COUNT
                        하나의 자막 세그먼트에 있는 최대 줄 수. (기본값: 1)
  --min_dist_to_end {0,4,5,6,7,8,9,10,11,12}
                        ( --sentence 필요) 'the', 'Mr.' 등과 같은 단어에서 줄 끝까지의 거리가 설정된 값보다 작으면
                        새 줄에서 시작합니다. 참고: 0 = 비활성화. (기본값: 0)
  --prompt_max {16,32,64,128,223}
                        (실험적) 프롬프트의 최대 크기. (기본값: 223)
  --reprompt {0,1,2}    (실험적) 0) 비활성화. 1) 프롬프트가 재설정된 후 initial_prompt를 삽입합니다. 2) 모든 창/청크에 대한
                        프롬프트에 initial_prompt가 있는지 확인합니다. 참고: initial_prompt=None이면 자동으로 비활성화됩니다.
                        'hotwords' 기능과 유사합니다. (기본값: 2)
  --prompt_reset_on_no_end {0,1,2}
                        (실험적) 창/청크에 문장 끝이 없으면 프롬프트를 재설정합니다. 0 - 비활성화, 1 - 마침표 찾기,
                        2 - 마침표 또는 쉼표 찾기. 참고: reprompt=0이면 자동으로 비활성화됩니다. (기본값: 2)
  --ff_dump             필터에 의해 사전 처리된 오디오를 16000Hz 파일로 덤프하고 일부 중간 오디오 파일의 삭제를 방지합니다. (기본값: False)
  --ff_track {1,2,3,4,5,6}
                        오디오 트랙 선택기. 1 - 첫 번째 오디오 트랙을 선택합니다. (기본값: 1)
  --ff_fc               처리할 전면-중앙 채널(FC)만 선택합니다. (기본값: False)
  --ff_mp3              오디오 필터: MP3로 변환했다가 다시 변환합니다. (기본값: False)
  --ff_sync             오디오 필터: 초당 최대 3600 샘플 보상으로 주어진 타임스탬프에 샘플을 늘리거나 줄입니다.
                        입력 파일은 mp4, mkv와 같이 PTS 저장을 지원하는 컨테이너여야 합니다. (기본값: False)
  --ff_rnndn_sh         오디오 필터: 순환 신경망을 사용하여 GregorR의 SH 모델로 비음성을 억제합니다.
                        참고: Xiph보다 더 공격적이며 노래를 버립니다. (기본값: False)
  --ff_rnndn_xiph       오디오 필터: 순환 신경망을 사용하여 Xiph의 원본 모델로 비음성을 억제합니다. (기본값: False)
  --ff_fftdn [0 - 97]   오디오 필터: 고속 푸리에 변환을 사용한 일반 노이즈 제거. 참고: 12 - 보통 강도, 0 - 비활성화. (기본값: 0)
  --ff_tempo [0.5 - 2.0]
                        오디오 필터: 오디오 템포를 조정합니다. 1.0 미만의 값은 오디오를 느리게 하고, 초과하면 속도를 높입니다. 1.0 = 비활성화. (기본값: 1.0)
  --ff_gate             오디오 필터: 신호의 낮은 부분을 줄입니다. (기본값: False)
  --ff_speechnorm       오디오 필터: 극단적이고 빠른 음성 증폭. (기본값: False)
  --ff_loudnorm         오디오 필터: EBU R128 음량 정규화. (기본값: False)
  --ff_silence_suppress noise duration
                        오디오 필터: 오디오의 조용한 부분을 억제합니다. 두 개의 값을 사용합니다. 첫 번째 값 - 데시벨 단위의 노이즈 허용 오차 [-70 - 0] (0=비활성화),
                        두 번째 값 - 초 단위의 최소 무음 지속 시간 [0.1 - 10]. (기본값: [0, 3.0])
  --ff_lowhighpass      오디오 필터: 50Hz - 7800 대역을 통과시킵니다. sinc + afir. (기본값: False)
