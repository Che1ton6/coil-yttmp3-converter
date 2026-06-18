import customtkinter as ctk
from tkinter import filedialog
import yt_dlp
import os
import sys
import threading

def _bundled_ffmpeg():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "bin")
    return None

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "default": {
        "bg":           "#0f0f0f",
        "card":         "#141414",
        "border":       "#2a2a2a",
        "input_bg":     "#0a0a0a",
        "accent":       "#ff2d2d",
        "accent_hover": "#cc0000",
        "accent_text":  "#ffffff",
        "btn_secondary":"#1e1e1e",
        "btn_sec_hover":"#2a2a2a",
        "btn_sec_text": "#cccccc",
        "text":         "#ffffff",
        "text_muted":   "#666666",
        "text_label":   "#555555",
        "success":      "#22c55e",
        "font_family":  "Arial Black",
        "font_body":    "Arial",
        "title_text":   "COIL CONTENT CONVERTER",
        "title_size":   28,
    },
    "coilwhiner": {
        "bg":           "#0E1A14",
        "card":         "#1A2B1F",
        "border":       "#2D4A33",
        "input_bg":     "#243526",
        "accent":       "#B8FF00",
        "accent_hover": "#8ABF00",
        "accent_text":  "#0A1A08",
        "btn_secondary":"#1A2B1F",
        "btn_sec_hover":"#243526",
        "btn_sec_text": "#8FAF8F",
        "text":         "#D4EBD4",
        "text_muted":   "#5A7A5A",
        "text_label":   "#5A7A5A",
        "success":      "#B8FF00",
        "font_family":  "Courier New",
        "font_body":    "Courier New",
        "title_text":   "COIL CONTENT CONVERTER",
        "title_size":   28,
    },
    "eques": {
        "bg":           "#000000",
        "card":         "#0C0C10",
        "border":       "#3A1A5A",
        "input_bg":     "#080808",
        "accent":       "#00C8FF",
        "accent_hover": "#0099CC",
        "accent_text":  "#000000",
        "btn_secondary":"#140A22",
        "btn_sec_hover":"#1E0F33",
        "btn_sec_text": "#9966CC",
        "text":         "#FFFFFF",
        "text_muted":   "#7B5FAA",
        "text_label":   "#6A4F99",
        "success":      "#00C8FF",
        "font_family":  "Arial Black",
        "font_body":    "Arial",
        "title_text":   "COIL CONTENT CONVERTER",
        "title_size":   28,
    }
}

def sanitize(name):
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip()

def is_playlist(url):
    return "playlist" in url or "list=" in url

def get_playlist_title(url):
    with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return sanitize(info.get("title", "Playlist"))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Coil Content Converter")
        self.geometry("680x760")
        self.resizable(False, False)
        self.current_theme = "default"
        self.t = THEMES["default"]
        self.selected_format = ctk.StringVar(value="mp3")
        self.selected_quality = ctk.StringVar(value="320")
        self.save_path = ctk.StringVar(value=DOWNLOAD_FOLDER)
        self._progress = 0.0
        self._status_text = ""
        self._status_color = None
        self.configure(fg_color=self.t["bg"])
        self.build_ui()

    # ── Build UI ───────────────────────────────────────────────────────────────
    def build_ui(self):
        t = self.t

        # Top bar (title + theme toggle)
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(padx=24, pady=(28, 0), fill="x")

        self.title_label = ctk.CTkLabel(
            top, text=t["title_text"],
            font=ctk.CTkFont(family=t["font_family"], size=t["title_size"], weight="bold"),
            text_color=t["accent"])
        self.title_label.pack(side="left")

        _display = {"default": "Default", "coilwhiner": "CoilWhiner", "eques": "Eques"}
        self.theme_menu = ctk.CTkOptionMenu(
            top,
            values=["Default", "CoilWhiner", "Eques"],
            command=self.set_theme,
            width=130, height=32, corner_radius=5,
            fg_color=t["btn_secondary"], button_color=t["btn_sec_hover"],
            button_hover_color=t["accent"], text_color=t["btn_sec_text"],
            dropdown_fg_color=t["card"], dropdown_hover_color=t["btn_sec_hover"],
            dropdown_text_color=t["text"],
            font=ctk.CTkFont(family=t["font_body"], size=12))
        self.theme_menu.set(_display[self.current_theme])
        self.theme_menu.pack(side="right")

        self.subtitle_label = ctk.CTkLabel(
            self, text="YouTube Edition",
            font=ctk.CTkFont(family=t["font_body"], size=13),
            text_color=t["text_muted"])
        self.subtitle_label.pack(pady=(4, 20))

        # Card
        self.card = ctk.CTkFrame(self, fg_color=t["card"], corner_radius=8,
                                  border_width=1, border_color=t["border"])
        self.card.pack(padx=24, fill="x")

        # URL
        self._label(self.card, "YOUTUBE URL")
        self.url_entry = ctk.CTkEntry(
            self.card, placeholder_text="https://www.youtube.com/watch?v=...",
            height=42, corner_radius=6, fg_color=t["input_bg"],
            border_color=t["border"], text_color=t["text"],
            font=ctk.CTkFont(family=t["font_body"], size=13))
        self.url_entry.pack(padx=24, fill="x")
        self.url_entry.bind("<Button-3>", self._show_url_context_menu)

        # Save location
        self._label(self.card, "SAVE LOCATION", top=18)
        path_row = ctk.CTkFrame(self.card, fg_color="transparent")
        path_row.pack(padx=24, fill="x")
        self.path_entry = ctk.CTkEntry(
            path_row, textvariable=self.save_path,
            height=42, corner_radius=6, fg_color=t["input_bg"],
            border_color=t["border"], text_color=t["text"],
            font=ctk.CTkFont(family=t["font_body"], size=12))
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.browse_btn = ctk.CTkButton(
            path_row, text="📂 Browse", width=100, height=42, corner_radius=6,
            fg_color=t["btn_secondary"], hover_color=t["btn_sec_hover"],
            text_color=t["btn_sec_text"],
            font=ctk.CTkFont(family=t["font_body"], size=13),
            command=self.browse_folder)
        self.browse_btn.pack(side="right")

        # Format
        self._label(self.card, "FORMAT", top=18)
        fmt_row = ctk.CTkFrame(self.card, fg_color="transparent")
        fmt_row.pack(padx=24, fill="x")
        self.rb_mp3 = ctk.CTkRadioButton(
            fmt_row, text="🎵  MP3 — Audio",
            variable=self.selected_format, value="mp3",
            command=self.update_qualities,
            font=ctk.CTkFont(family=t["font_body"], size=14),
            fg_color=t["accent"], text_color=t["text"])
        self.rb_mp3.pack(side="left", padx=(0, 24))
        self.rb_mp4 = ctk.CTkRadioButton(
            fmt_row, text="🎥  MP4 — Video",
            variable=self.selected_format, value="mp4",
            command=self.update_qualities,
            font=ctk.CTkFont(family=t["font_body"], size=14),
            fg_color=t["accent"], text_color=t["text"])
        self.rb_mp4.pack(side="left")

        # Quality
        self._label(self.card, "QUALITY", top=18)
        self.quality_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.quality_frame.pack(padx=24, fill="x", pady=(0, 24))
        self.render_qualities()

        # Download button
        self.dl_btn = ctk.CTkButton(
            self, text="DOWNLOAD", height=52, corner_radius=6,
            fg_color=t["accent"], hover_color=t["accent_hover"],
            text_color=t["accent_text"],
            font=ctk.CTkFont(family=t["font_family"], size=20, weight="bold"),
            command=self.start_download)
        self.dl_btn.pack(padx=24, pady=20, fill="x")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self, height=8, corner_radius=99,
            progress_color=t["accent"], fg_color="#222")
        self.progress_bar.pack(padx=24, fill="x")
        self.progress_bar.set(0)

        # Status
        self.status_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(family=t["font_body"], size=13),
            text_color=t["text_muted"])
        self.status_label.pack(pady=(10, 0))

    def _label(self, parent, text, top=24):
        t = self.t
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(family=t["font_body"], size=11, weight="bold"),
            text_color=t["text_label"]
        ).pack(anchor="w", padx=24, pady=(top, 6))

    # ── URL context menu ───────────────────────────────────────────────────────
    def _show_url_context_menu(self, event):
        t = self.t
        import tkinter as tk
        menu = tk.Menu(self, tearoff=0,
                       bg=t["card"], fg=t["text"],
                       activebackground=t["accent"], activeforeground=t["accent_text"],
                       bd=0, relief="flat")
        menu.add_command(label="Paste", command=self._paste_url)
        menu.tk_popup(event.x_root, event.y_root)

    def _paste_url(self):
        try:
            text = self.clipboard_get()
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, text)
        except Exception:
            pass

    # ── Theme select ───────────────────────────────────────────────────────────
    def set_theme(self, selection):
        _key = {"Default": "default", "CoilWhiner": "coilwhiner", "Eques": "eques"}
        chosen = _key.get(selection, "default")
        if chosen == self.current_theme:
            return

        url = self.url_entry.get()
        downloading = str(self.dl_btn.cget("state")) == "disabled"

        self.current_theme = chosen
        self.t = THEMES[self.current_theme]
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(fg_color=self.t["bg"])
        self.build_ui()

        if url:
            self.url_entry.insert(0, url)
        self.progress_bar.set(self._progress)
        if self._status_text:
            self.status_label.configure(text=self._status_text, text_color=self._status_color)
        if downloading:
            self.dl_btn.configure(state="disabled")

    # ── Qualities ──────────────────────────────────────────────────────────────
    def render_qualities(self):
        t = self.t
        for w in self.quality_frame.winfo_children():
            w.destroy()
        if self.selected_format.get() == "mp3":
            options = [("320 kbps", "320"), ("192 kbps", "192"), ("128 kbps", "128")]
        else:
            options = [("4K 2160p", "2160"), ("1080p HD", "1080"), ("720p HD", "720"),
                       ("480p", "480"), ("360p", "360")]
        self.selected_quality.set(options[0][1])
        for label, val in options:
            ctk.CTkRadioButton(
                self.quality_frame, text=label,
                variable=self.selected_quality, value=val,
                font=ctk.CTkFont(family=t["font_body"], size=13),
                fg_color=t["accent"], text_color=t["text"]
            ).pack(side="left", padx=(0, 20))

    def update_qualities(self):
        self.render_qualities()

    # ── Folder browse ──────────────────────────────────────────────────────────
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Download Folder")
        if folder:
            self.save_path.set(folder)

    # ── Status ─────────────────────────────────────────────────────────────────
    def set_status(self, text, color=None):
        self._status_text = text
        self._status_color = color or self.t["text_muted"]
        self.status_label.configure(text=text, text_color=self._status_color)

    # ── Download ───────────────────────────────────────────────────────────────
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.set_status("⚠️  Please enter a URL!", self.t["accent"])
            return
        self.dl_btn.configure(state="disabled")
        self._progress = 0.0
        self.progress_bar.set(0)
        self.set_status("⏳  Starting download...")
        threading.Thread(target=self.download_task, args=(url,), daemon=True).start()

    def download_task(self, url):
        fmt = self.selected_format.get()
        quality = self.selected_quality.get()
        base_folder = self.save_path.get() or DOWNLOAD_FOLDER

        if is_playlist(url):
            self.after(0, lambda: self.set_status("🔍  Fetching playlist info..."))
            title = get_playlist_title(url)
            output_folder = os.path.join(base_folder, title)
            os.makedirs(output_folder, exist_ok=True)
        else:
            output_folder = base_folder

        def progress_hook(d):
            if d["status"] == "downloading":
                pct = d.get("_percent_str", "0%").strip().replace("%", "")
                try:
                    val = float(pct) / 100
                    self._progress = val
                    self.after(0, lambda p=val: self.progress_bar.set(p))
                except:
                    pass
                filename = os.path.basename(d.get("filename", ""))
                self.after(0, lambda s=f"⬇️  Downloading {d.get('_percent_str','').strip()}  —  {filename[:50]}":
                           self.set_status(s))
            elif d["status"] == "finished":
                self._progress = 0.95
                self.after(0, lambda: self.set_status("⚙️  Converting file..."))
                self.after(0, lambda: self.progress_bar.set(0.95))

        ffmpeg_path = _bundled_ffmpeg()
        if fmt == "mp3":
            ydl_opts = {
                "format": "bestaudio",
                "outtmpl": os.path.join(output_folder, f"%(title)s [{quality}kbps].%(ext)s"),
                "postprocessors": [{"key": "FFmpegExtractAudio",
                                    "preferredcodec": "mp3",
                                    "preferredquality": quality}],
                "progress_hooks": [progress_hook],
                "ignoreerrors": True,
            }
        else:
            quality_map = {
                "2160": "bestvideo[height<=2160]+bestaudio",
                "1080": "bestvideo[height<=1080]+bestaudio",
                "720":  "bestvideo[height<=720]+bestaudio",
                "480":  "bestvideo[height<=480]+bestaudio",
                "360":  "bestvideo[height<=360]+bestaudio",
            }
            ydl_opts = {
                "format": quality_map.get(quality, "bestvideo+bestaudio"),
                "outtmpl": os.path.join(output_folder, f"%(title)s [{quality}p].%(ext)s"),
                "merge_output_format": "mp4",
                "progress_hooks": [progress_hook],
                "ignoreerrors": True,
            }
        if ffmpeg_path:
            ydl_opts["ffmpeg_location"] = ffmpeg_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self._progress = 1.0
            self.after(0, lambda: self.progress_bar.set(1.0))
            self.after(0, lambda: self.set_status(f"✅  Done! Saved to: {output_folder}", self.t["success"]))
            self.after(0, lambda: self.show_complete_dialog(output_folder))
        except Exception as e:
            self.after(0, lambda err=str(e): self.set_status(f"❌  Error: {err}", "#ff6060"))
        finally:
            self.after(0, lambda: self.dl_btn.configure(state="normal"))

    # ── Complete dialog ────────────────────────────────────────────────────────
    def show_complete_dialog(self, folder):
        t = self.t
        dialog = ctk.CTkToplevel(self)
        dialog.title("Download Complete")
        dialog.geometry("400x220")
        dialog.resizable(False, False)
        dialog.configure(fg_color=t["card"])
        dialog.grab_set()
        dialog.focus_force()

        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - 200
        y = self.winfo_y() + (self.winfo_height() // 2) - 110
        dialog.geometry(f"400x220+{x}+{y}")

        ctk.CTkLabel(
            dialog, text="✅  Download Complete!",
            font=ctk.CTkFont(family=t["font_family"], size=20, weight="bold"),
            text_color=t["success"]).pack(pady=(32, 8))

        ctk.CTkLabel(
            dialog, text=f"Saved to:\n{folder}",
            font=ctk.CTkFont(family=t["font_body"], size=12),
            text_color=t["text_muted"],
            wraplength=340, justify="center").pack(pady=(0, 24))

        btn_row = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_row.pack(padx=24, fill="x")

        def view_in_folder():
            os.startfile(folder)
            dialog.destroy()

        def download_next():
            self.url_entry.delete(0, "end")
            self._progress = 0.0
            self.progress_bar.set(0)
            self.set_status("")
            dialog.destroy()

        ctk.CTkButton(
            btn_row, text="📂  View in Folder", height=44, corner_radius=6,
            fg_color=t["btn_secondary"], hover_color=t["btn_sec_hover"],
            text_color=t["btn_sec_text"],
            font=ctk.CTkFont(family=t["font_body"], size=14),
            command=view_in_folder).pack(side="left", expand=True, padx=(0, 8))

        ctk.CTkButton(
            btn_row, text="⬇️  Download Next", height=44, corner_radius=6,
            fg_color=t["accent"], hover_color=t["accent_hover"],
            text_color=t["accent_text"],
            font=ctk.CTkFont(family=t["font_body"], size=14),
            command=download_next).pack(side="right", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()