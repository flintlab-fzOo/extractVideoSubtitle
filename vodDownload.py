"""
VOD Downloader - SOOP VOD 및 YouTube 영상 다운로더
GUI 프로그램 (tkinter 기반)
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from datetime import datetime
import re
import webbrowser
import shutil

class ToolTip:
    """위젯에 툴팁을 표시하는 클래스"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 27
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#FFFFE0", relief=tk.SOLID, borderwidth=1,
                      font=("맑은 고딕", "9", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


# yt-dlp 라이브러리 임포트
try:
    import yt_dlp
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp


class VODDownloader:
    VERSION = "v1.0"
    # 색상 테마 (블루톤)
    COLORS = {
        'primary': '#2196F3',       # 메인 블루
        'primary_dark': '#1976D2',  # 다크 블루
        'primary_light': '#BBDEFB', # 라이트 블루
        'accent': '#03A9F4',        # 액센트 블루
        'background': '#F5F5F5',    # 배경
        'surface': '#FFFFFF',       # 서피스
        'text': '#212121',          # 텍스트
        'text_secondary': '#757575', # 보조 텍스트
        'success': '#4CAF50',       # 성공 (녹색)
        'error': '#F44336',         # 에러 (빨강)
    }

    def __init__(self, root):
        self.root = root
        self.root.title("📥 VOD Downloader")
        self.root.geometry("750x650")
        self.root.minsize(650, 500)
        self.root.configure(bg=self.COLORS['background'])

        # 다운로드 중 플래그
        self.is_downloading = False
        self.stop_requested = False
        self.download_thread = None
        self.current_quality = "720p"

        # 다운로드 폴더 설정
        self.download_folder = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        # 쿠키 파일 경로
        self.cookie_file = None

        # 상세 옵션 표시 여부
        self.show_advanced = False

        # FFmpeg 경로 설정
        self.ffmpeg_path = None

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """스타일 설정"""
        style = ttk.Style()
        style.theme_use('clam')

        # 프레임 스타일
        style.configure('TFrame', background=self.COLORS['background'])
        style.configure('Card.TFrame', background=self.COLORS['surface'])
        style.configure('TLabelframe', background=self.COLORS['surface'])
        style.configure('TLabelframe.Label',
                       background=self.COLORS['surface'],
                       foreground=self.COLORS['primary_dark'],
                       font=('맑은 고딕', 10, 'bold'))

        # 라벨 스타일
        style.configure('TLabel',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text'],
                       font=('맑은 고딕', 9))
        style.configure('Header.TLabel',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['primary_dark'],
                       font=('맑은 고딕', 12, 'bold'))
        style.configure('Status.TLabel',
                       background=self.COLORS['background'],
                       foreground=self.COLORS['text_secondary'],
                       font=('맑은 고딕', 9))

        # 버튼 스타일
        style.configure('TButton',
                       font=('맑은 고딕', 9),
                       padding=(10, 5))

        # 프로그래스바 스타일 (블루톤)
        style.configure('Blue.Horizontal.TProgressbar',
                       troughcolor=self.COLORS['primary_light'],
                       background=self.COLORS['primary'],
                       lightcolor=self.COLORS['accent'],
                       darkcolor=self.COLORS['primary_dark'],
                       bordercolor=self.COLORS['primary_light'],
                       thickness=20)

        # Entry 스타일
        style.configure('TEntry', padding=5)

        # Combobox 스타일
        style.configure('TCombobox', padding=5)

    def _create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 헤더
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # 좌측 타이틀 그룹 (수직 중앙 정렬을 위해 anchor 사용)
        title_container = ttk.Frame(header_frame)
        title_container.pack(side=tk.LEFT)

        header_label = ttk.Label(title_container,
                                text="📥 VOD Downloader",
                                style='Header.TLabel')
        header_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(title_container,
                                  text="SOOP · YouTube · 기타 사이트",
                                  style='Status.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0), pady=(3, 0)) # 베이스라인 맞춤

        # 버전 표시 (우측 끝, 수직 중앙 정렬)
        version_label = ttk.Label(header_frame,
                                 text=self.VERSION,
                                 style='Status.TLabel')
        version_label.pack(side=tk.RIGHT, pady=(3, 0))

        # URL 입력 영역
        url_frame = ttk.LabelFrame(main_frame, text="🔗 영상 URL", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 10))

        url_inner_frame = ttk.Frame(url_frame)
        url_inner_frame.pack(fill=tk.X)

        self.url_entry = ttk.Entry(url_inner_frame, font=("맑은 고딕", 10))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.url_entry.bind("<Return>", lambda e: self._start_download())

        # 다운로드 버튼 (높이 조정)
        self.download_btn = tk.Button(
            url_inner_frame,
            text="⬇ 다운로드",
            font=("맑은 고딕", 10, "bold"),
            bg=self.COLORS['primary'],
            fg='white',
            activebackground=self.COLORS['primary_dark'],
            activeforeground='white',
            relief=tk.FLAT,
            padx=15,
            pady=1,
            cursor='hand2',
            command=self._toggle_download
        )
        self.download_btn.pack(side=tk.RIGHT)

        # 옵션 영역
        option_frame = ttk.LabelFrame(main_frame, text="⚙ 설정", padding="15")
        option_frame.pack(fill=tk.X, pady=(0, 10))
        option_frame.columnconfigure(1, weight=1)

        # 1. 저장 경로 행
        ttk.Label(option_frame, text="📂 저장 경로:").grid(row=0, column=0, sticky=tk.W, pady=3)
        self.folder_var = tk.StringVar(value=self.download_folder)
        folder_entry = ttk.Entry(option_frame, textvariable=self.folder_var)
        folder_entry.grid(row=0, column=1, sticky=tk.EW, padx=(5, 5), pady=3)

        folder_btn = tk.Button(option_frame, text="...",
                              font=("맑은 고딕", 9),
                              bg=self.COLORS['surface'],
                              relief=tk.GROOVE,
                              padx=8, pady=2,
                              cursor='hand2',
                              command=self._select_folder)
        folder_btn.grid(row=0, column=2, sticky=tk.E, pady=3)

        # 2. 화질 및 상세 토글 행
        quality_row = ttk.Frame(option_frame)
        quality_row.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=(3, 0))

        ttk.Label(quality_row, text="📺 영상 화질:").pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="720p")
        quality_combo = ttk.Combobox(quality_row, textvariable=self.quality_var,
                                      values=["best", "1080p", "720p", "480p", "360p"],
                                      state="readonly", width=10)
        quality_combo.pack(side=tk.LEFT, padx=(5, 10))

        self.advanced_btn = tk.Button(quality_row, text="⚙",
                                     font=("맑은 고딕", 9),
                                     bg=self.COLORS['surface'],
                                     relief=tk.GROOVE,
                                     padx=10, pady=2,
                                     cursor='hand2',
                                     command=self._toggle_advanced)
        self.advanced_btn.pack(side=tk.RIGHT)

        # 상세 설정 영역 (기본 숨김)
        self.advanced_frame = ttk.Frame(option_frame)
        self.advanced_frame.columnconfigure(1, weight=1)

        # 3. 쿠키 설정 행
        ttk.Label(self.advanced_frame, text="🍪 쿠키 설정:").grid(row=0, column=0, sticky=tk.W, pady=5)

        cookie_ctrl = ttk.Frame(self.advanced_frame)
        cookie_ctrl.grid(row=0, column=1, columnspan=2, sticky=tk.W, pady=5)

        self.browser_var = tk.StringVar(value="없음")
        browser_combo = ttk.Combobox(cookie_ctrl, textvariable=self.browser_var,
                                      values=["없음", "파일", "firefox", "edge", "chrome", "brave"],
                                      state="readonly", width=10)
        browser_combo.pack(side=tk.LEFT, padx=(5, 10))

        cookie_btn = tk.Button(cookie_ctrl, text="📁 쿠키 선택",
                              font=("맑은 고딕", 9),
                              bg=self.COLORS['surface'],
                              relief=tk.GROOVE,
                              padx=8, pady=2,
                              cursor='hand2',
                              command=self._select_cookie_file)
        cookie_btn.pack(side=tk.LEFT)

        self.cookie_status_label = ttk.Label(cookie_ctrl, text="", style='Status.TLabel')
        self.cookie_status_label.pack(side=tk.LEFT, padx=(10, 0))

        # 4. FFmpeg 설정 행
        ttk.Label(self.advanced_frame, text="🛠 FFmpeg 설정:").grid(row=1, column=0, sticky=tk.W, pady=10)

        ffmpeg_ctrl = ttk.Frame(self.advanced_frame)
        ffmpeg_ctrl.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=10)

        ffmpeg_down_btn = tk.Button(ffmpeg_ctrl, text="📥 다운로드",width=11,
                                   font=("맑은 고딕", 9),
                                   bg=self.COLORS['surface'],
                                   fg=self.COLORS['primary'],
                                   relief=tk.GROOVE,
                                   padx=8, pady=2,
                                   cursor='hand2',
                                   command=self._open_ffmpeg_download)
        ffmpeg_down_btn.pack(side=tk.LEFT, padx=(5, 10))

        ffmpeg_path_btn = tk.Button(ffmpeg_ctrl, text="⚙ 파일 설정",
                                   font=("맑은 고딕", 9),
                                   bg=self.COLORS['surface'],
                                   relief=tk.GROOVE,
                                   padx=8, pady=2,
                                   cursor='hand2',
                                   command=self._select_ffmpeg_path)
        ffmpeg_path_btn.pack(side=tk.LEFT)

        self.ffmpeg_path_label = ttk.Label(ffmpeg_ctrl, text="", style='Status.TLabel')
        self.ffmpeg_path_label.pack(side=tk.LEFT, padx=(10, 0))

        # 진행률 표시
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            style='Blue.Horizontal.TProgressbar'
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        self.progress_label = ttk.Label(progress_frame, text="⏸ 대기 중...", style='Status.TLabel')
        self.progress_label.pack(anchor=tk.W)

        # 하단 버튼
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        clear_btn = tk.Button(bottom_frame, text="🗑",
                             font=("맑은 고딕", 9),
                             bg=self.COLORS['surface'],
                             relief=tk.GROOVE,
                             padx=10, pady=3,
                             cursor='hand2',
                             command=self._clear_console)
        clear_btn.pack(side=tk.LEFT)
        ToolTip(clear_btn, "로그 초기화")

        # FFmpeg 상태 표시 영역
        ffmpeg_status_frame = ttk.Frame(bottom_frame)
        ffmpeg_status_frame.pack(side=tk.LEFT, padx=(15, 0))

        ttk.Label(ffmpeg_status_frame, text="FFmpeg:", font=("맑은 고딕", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))

        self.ffmpeg_status_var = tk.StringVar(value="확인 중...")
        ffmpeg_label = ttk.Label(ffmpeg_status_frame, textvariable=self.ffmpeg_status_var, style='Status.TLabel')
        ffmpeg_label.pack(side=tk.LEFT)

        open_folder_btn = tk.Button(bottom_frame, text="📂 다운로드 폴더 열기",
                                   font=("맑은 고딕", 9),
                                   bg=self.COLORS['surface'],
                                   relief=tk.GROOVE,
                                   padx=10, pady=3,
                                   cursor='hand2',
                                   command=self._open_download_folder)
        open_folder_btn.pack(side=tk.RIGHT)

        # 상태 콘솔 출력
        console_frame = ttk.LabelFrame(main_frame, text="📋 로그", padding="5")
        console_frame.pack(fill=tk.BOTH, expand=True)

        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=8,
            font=("Consolas", 9),
            state=tk.DISABLED,
            wrap=tk.WORD,
            bg='#1E1E1E',
            fg='#D4D4D4',
            insertbackground='white',
            selectbackground=self.COLORS['primary'],
            relief=tk.FLAT
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        # 초기 메시지
        self._log("VOD Downloader 시작됨", "info")
        # self._log("지원: SOOP(afreecaTV), YouTube, yt-dlp 지원 사이트", "info")
        # self._log("─" * 45, "info")
        # self._log("💡 YouTube 다운로드 시 쿠키 파일이 필요합니다", "warning")
        # self._log("   [⚙ 상세] 버튼 클릭 → 쿠키 설정", "info")

        # FFmpeg 상태 확인
        self._update_ffmpeg_status()

    def _toggle_advanced(self):
        """상세 옵션 토글"""
        self.show_advanced = not self.show_advanced
        if self.show_advanced:
            self.advanced_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=(10, 0))
            self.advanced_btn.config(text="상세 설정 ▲", bg=self.COLORS['primary_light'])
        else:
            self.advanced_frame.grid_forget()
            self.advanced_btn.config(text="상세 설정 ⚙", bg=self.COLORS['surface'])

    def _log(self, message, level="info"):
        """콘솔에 로그 출력"""
        def update():
            self.console.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime("%H:%M:%S")

            # 레벨에 따른 색상 태그
            if level == "error":
                prefix = "❌"
            elif level == "success":
                prefix = "✅"
            elif level == "warning":
                prefix = "⚠️"
            else:
                prefix = "▸"

            self.console.insert(tk.END, f"[{timestamp}] {prefix} {message}\n")
            self.console.see(tk.END)
            self.console.config(state=tk.DISABLED)
        self.root.after(0, update)

    def _clear_console(self):
        """콘솔 내용 지우기"""
        self.console.config(state=tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.config(state=tk.DISABLED)

    def _select_folder(self):
        """다운로드 폴더 선택"""
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.download_folder = folder
            self.folder_var.set(folder)
            self._log(f"저장 폴더 변경: {folder}", "info")

    def _select_cookie_file(self):
        """쿠키 파일 선택"""
        file = filedialog.askopenfilename(
            title="쿠키 파일 선택",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file:
            self.cookie_file = file
            self.browser_var.set("파일")
            filename = os.path.basename(file)
            self.cookie_status_label.config(text=f"✓ {filename[:20]}...")
            self._log(f"쿠키 파일 선택됨: {filename}", "success")

    def _open_download_folder(self):
        """다운로드 폴더 열기"""
        folder = self.folder_var.get()
        if os.path.exists(folder):
            os.startfile(folder)
        else:
            messagebox.showwarning("경고", "폴더가 존재하지 않습니다.")

    def _update_ffmpeg_status(self):
        """ffmpeg 설치 여부 확인 및 UI 업데이트"""
        installed = False
        if self.ffmpeg_path:
            if os.path.isfile(self.ffmpeg_path) and ("ffmpeg" in os.path.basename(self.ffmpeg_path).lower()):
                installed = True
            elif os.path.isdir(self.ffmpeg_path):
                if shutil.which("ffmpeg", path=self.ffmpeg_path):
                    installed = True

        if not installed:
            installed = shutil.which("ffmpeg") is not None

        if installed:
            self.ffmpeg_status_var.set("✅ 설치됨")
        else:
            self.ffmpeg_status_var.set("❌ 미설치")

    def _open_ffmpeg_download(self):
        """ffmpeg 다운로드 페이지 열기"""
        webbrowser.open("https://github.com/BtbN/FFmpeg-Builds/releases/tag/latest")

    def _select_ffmpeg_path(self):
        """ffmpeg 경로 설정"""
        path = filedialog.askopenfilename(
            title="ffmpeg.exe 파일 선택",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.ffmpeg_path = path
            self._update_ffmpeg_status()
            self._log(f"FFmpeg 경로 설정됨: {path}", "success")

            # 경로 표시 라벨 업데이트 (길면 생략)
            display_path = path if len(path) <= 40 else f"...{path[-37:]}"
            self.ffmpeg_path_label.config(text=f"📍 {display_path}")

    def _progress_hook(self, d):
        """yt-dlp 다운로드 진행 상황 훅"""
        # 정지 요청 확인
        if self.stop_requested:
            raise yt_dlp.utils.DownloadCancelled("사용자가 다운로드를 중단했습니다.")

        if d['status'] == 'downloading':
            # 진행률 계산 - 여러 방법 시도
            percent = 0

            # 방법 1: downloaded_bytes / total_bytes
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total and total > 0:
                percent = (downloaded / total) * 100

            # 방법 2: _percent_str 파싱 (백업)
            if percent == 0:
                percent_str = d.get('_percent_str', '0%')
                # ANSI 코드 제거
                clean_percent = re.sub(r'\x1b\[[0-9;]*m', '', percent_str).strip()
                try:
                    percent = float(clean_percent.replace('%', '').strip())
                except:
                    pass

            # UI 업데이트
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')

            # ANSI 코드 제거
            if speed:
                speed = re.sub(r'\x1b\[[0-9;]*m', '', speed).strip()
            if eta:
                eta = re.sub(r'\x1b\[[0-9;]*m', '', eta).strip()

            def update_ui(p=percent, s=speed, e=eta):
                self.progress_var.set(p)
                self.progress_label.config(
                    text=f"⬇ 다운로드 중: {p:.1f}% | 속도: {s} | 남은 시간: {e}"
                )
            self.root.after(0, update_ui)

        elif d['status'] == 'finished':
            filename = os.path.basename(d.get('filename', 'N/A'))
            self._log(f"파일 완료: {filename}", "info")
            self._log("🔄 후처리 중...", "info")

            def update_finished():
                self.progress_var.set(100)
                self.progress_label.config(text="🔄 후처리 중...")
            self.root.after(0, update_finished)

    def _get_format_string(self, quality):
        """화질에 따른 포맷 문자열 반환"""
        if quality == "best":
            return 'bv*+ba/b'
        else:
            height = quality[:-1]  # "720p" -> "720"
            return f'bv*[height<={height}]+ba/b[height<={height}]/b'

    def _detect_site(self, url):
        """URL에서 사이트 감지"""
        if "sooplive.co.kr" in url or "afreecatv.com" in url:
            return "SOOP"
        elif "youtube.com" in url or "youtu.be" in url:
            return "YouTube"
        else:
            return "기타"

    def _sanitize_filename(self, filename):
        """파일명에서 특수문자 제거"""
        # Windows에서 허용되지 않는 문자 제거
        return re.sub(r'[<>:"/\\|?*]', '', filename)

    def _rename_with_quality(self, filepath, quality):
        """파일명에 화질 정보 추가"""
        if not os.path.exists(filepath):
            return filepath

        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)

        # 이미 화질 정보가 있는지 확인
        quality_pattern = r'\.(best|1080p|720p|480p|360p)$'
        if re.search(quality_pattern, name):
            return filepath

        # 새 파일명 생성
        new_name = f"{name}.{quality}{ext}"
        new_path = os.path.join(directory, new_name)

        try:
            os.rename(filepath, new_path)
            return new_path
        except Exception as e:
            self._log(f"파일명 변경 실패: {e}", "warning")
            return filepath

    def _check_existing_part_file(self, download_folder, title):
        """기존 .part 파일 확인"""
        import glob
        # 파일명에서 특수문자 제거
        safe_title = self._sanitize_filename(title)
        # .part 파일 패턴 검색
        part_patterns = [
            os.path.join(download_folder, f"{safe_title}*.part"),
            os.path.join(download_folder, f"{safe_title}*.part-Frag*"),
        ]

        part_files = []
        for pattern in part_patterns:
            part_files.extend(glob.glob(pattern))

        return part_files

    def _ask_resume_or_restart(self, part_files):
        """이어받기/새로받기 선택 다이얼로그"""
        result = [None]  # 스레드 간 결과 전달용
        event = threading.Event()

        def ask():
            answer = messagebox.askyesnocancel(
                "다운로드 파일 발견",
                "이전에 다운로드 중이던 파일이 있습니다.\n\n"
                "• 예(Y): 이어받기\n"
                "• 아니오(N): 새로 받기 (기존 파일 삭제)\n"
                "• 취소: 다운로드 취소"
            )
            result[0] = answer
            event.set()

        self.root.after(0, ask)
        event.wait()
        return result[0]

    def _delete_part_files(self, part_files):
        """part 파일 삭제"""
        for f in part_files:
            try:
                os.remove(f)
                self._log(f"🗑 삭제됨: {os.path.basename(f)}", "info")
            except Exception as e:
                self._log(f"파일 삭제 실패: {e}", "warning")

    def _download(self, url, quality, browser):
        """실제 다운로드 수행 (별도 스레드)"""
        try:
            site = self._detect_site(url)
            self._log(f"🌐 사이트: {site}", "info")
            self._log(f"🔗 URL: {url[:50]}...", "info")
            self._log(f"📺 화질: {quality}", "info")

            # 다운로드 폴더 확인
            download_folder = self.folder_var.get()
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            format_string = self._get_format_string(quality)
            self.current_quality = quality

            ydl_opts = {
                'format': format_string,
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [self._progress_hook],
                'merge_output_format': 'mp4',
                'verbose': False,
                'no_warnings': False,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            }

            # FFmpeg 경로 설정 적용
            if self.ffmpeg_path:
                # 파일이 선택된 경우 디렉토리 경로 추출
                if os.path.isfile(self.ffmpeg_path):
                    ydl_opts['ffmpeg_location'] = os.path.dirname(self.ffmpeg_path)
                else:
                    ydl_opts['ffmpeg_location'] = self.ffmpeg_path

            # 브라우저 쿠키 사용
            if browser == "파일":
                if self.cookie_file and os.path.exists(self.cookie_file):
                    ydl_opts['cookiefile'] = self.cookie_file
                    self._log(f"🍪 쿠키 파일 사용", "info")
                else:
                    self._log("쿠키 파일이 선택되지 않았습니다", "warning")
            elif browser != "없음":
                ydl_opts['cookiesfrombrowser'] = (browser,)
                self._log(f"🍪 {browser} 브라우저 쿠키 사용", "info")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 먼저 정보 추출
                self._log("📡 영상 정보 추출 중...", "info")
                info = ydl.extract_info(url, download=False)
                title = info.get('title', '알 수 없음')
                duration = info.get('duration', 0)
                uploader = info.get('uploader', '알 수 없음')

                duration_str = f"{duration // 60}분 {duration % 60}초" if duration else "알 수 없음"

                self._log(f"📝 제목: {title[:40]}...", "info")
                self._log(f"👤 업로더: {uploader}", "info")
                self._log(f"⏱ 길이: {duration_str}", "info")

                # 기존 .part 파일 확인
                part_files = self._check_existing_part_file(download_folder, title)
                if part_files:
                    self._log(f"📦 기존 다운로드 파일 발견 ({len(part_files)}개)", "warning")

                    # 사용자에게 물어봄
                    choice = self._ask_resume_or_restart(part_files)

                    if choice is None:  # 취소
                        self._log("다운로드가 취소되었습니다.", "warning")
                        return
                    elif choice is False:  # 새로 받기
                        self._log("새로 다운로드를 시작합니다...", "info")
                        self._delete_part_files(part_files)
                    else:  # 이어받기
                        self._log("이어받기를 시작합니다...", "info")

                self._log("─" * 35, "info")
                self._log("⬇ 다운로드 시작...", "info")

                # 다운로드 실행
                ydl.download([url])

                # 다운로드된 파일 경로 가져오기
                downloaded_file = ydl.prepare_filename(info)
                # mp4로 병합된 경우 확장자 변경
                if not downloaded_file.endswith('.mp4'):
                    downloaded_file = os.path.splitext(downloaded_file)[0] + '.mp4'

                # 파일명에 화질 추가
                final_file = self._rename_with_quality(downloaded_file, quality)
                final_filename = os.path.basename(final_file)

                # 완료
                self._log("─" * 35, "info")
                self._log(f"저장됨: {final_filename}", "success")
                self._log("다운로드가 완료되었습니다!", "success")

                def update_ui():
                    self.progress_var.set(100)
                    self.progress_label.config(text="✅ 완료!")
                    messagebox.showinfo("완료", f"다운로드 완료!\n\n{final_filename}")
                self.root.after(0, update_ui)

        except yt_dlp.utils.DownloadCancelled:
            self._log("다운로드가 중단되었습니다.", "warning")
            self._log("💡 같은 URL로 다시 다운로드하면 이어받기됩니다.", "info")
            def update_ui_cancelled():
                self.progress_label.config(text="⏹ 중단됨 (이어받기 가능)")
            self.root.after(0, update_ui_cancelled)
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            # 사용자 취소로 인한 에러인지 확인
            if self.stop_requested:
                self._log("다운로드가 중단되었습니다.", "warning")
                self._log("💡 같은 URL로 다시 다운로드하면 이어받기됩니다.", "info")
                def update_ui_stopped():
                    self.progress_label.config(text="⏹ 중단됨 (이어받기 가능)")
                self.root.after(0, update_ui_stopped)
            else:
                self._log(f"다운로드 오류: {error_msg[:100]}", "error")
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("오류", f"다운로드 실패:\n{msg[:200]}"))
        except Exception as e:
            error_msg = str(e)
            if self.stop_requested:
                self._log("다운로드가 중단되었습니다.", "warning")
                self._log("💡 같은 URL로 다시 다운로드하면 이어받기됩니다.", "info")
            else:
                self._log(f"예상치 못한 오류: {error_msg}", "error")
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("오류", f"오류 발생:\n{msg}"))
        finally:
            self.is_downloading = False
            self.stop_requested = False
            def reset_ui():
                self.download_btn.config(
                    text="⬇ 다운로드",
                    state=tk.NORMAL,
                    bg=self.COLORS['primary'],
                    activebackground=self.COLORS['primary_dark']
                )
                self.url_entry.config(state=tk.NORMAL)
            self.root.after(0, reset_ui)

    def _toggle_download(self):
        """다운로드 시작/정지 토글"""
        if self.is_downloading:
            self._stop_download()
        else:
            self._start_download()

    def _stop_download(self):
        """다운로드 정지"""
        if not self.is_downloading:
            return

        self.stop_requested = True
        self._log("⏹ 다운로드 정지 요청...", "warning")
        self.progress_label.config(text="⏹ 정지 중...")
        self.download_btn.config(state=tk.DISABLED, bg=self.COLORS['text_secondary'])

    def _start_download(self):
        """다운로드 시작"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("경고", "URL을 입력해주세요.")
            return

        # 로그 초기화
        self._clear_console()

        # 플래그 초기화
        self.is_downloading = True
        self.stop_requested = False

        # UI 업데이트 - 정지 버튼으로 변경
        self.download_btn.config(
            text="⏹ 정지",
            bg=self.COLORS['error'],
            activebackground='#D32F2F'
        )
        self.url_entry.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress_label.config(text="⏳ 준비 중...")

        self._log("🚀 새 다운로드 시작", "info")
        self._log("═" * 40, "info")

        # 별도 스레드에서 다운로드
        quality = self.quality_var.get()
        browser = self.browser_var.get()
        self.download_thread = threading.Thread(
            target=self._download,
            args=(url, quality, browser),
            daemon=True
        )
        self.download_thread.start()


def main():
    root = tk.Tk()

    # 윈도우 아이콘 설정 (시스템 기본 아이콘 사용)
    try:
        root.iconbitmap(default='')
    except:
        pass

    app = VODDownloader(root)
    root.mainloop()


if __name__ == "__main__":
    main()
