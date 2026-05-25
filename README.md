# Coil Content Converter

A desktop app to download YouTube videos and playlists as MP3 or MP4, at any quality — built with Python and customtkinter.

---

## Download

**No Python or FFmpeg installation required.**

1. Go to the [Releases](../../releases) page
2. Download `CoilContentConverter.exe` under the latest release
3. Double-click to run — that's it

---

## What It Does

- Download any YouTube video or playlist by pasting its URL
- Right-click the URL field to paste directly
- Choose between MP3 (audio) or MP4 (video)
- Select your preferred quality (320kbps / 192kbps / 128kbps for MP3 — or 4K / 1080p / 720p / 480p / 360p for MP4)
- Choose exactly where to save your files using a folder browser
- Playlists automatically get saved into their own named folder
- Unavailable videos in a playlist are skipped automatically
- Files are named with their quality so multiple versions never overwrite each other
- A popup appears when done, letting you open the folder or start a new download
- Two visual themes: Default (dark red) and CoilWhiner (dark green) — switch anytime, even mid-download

---

## How to Use

1. Paste a YouTube video or playlist URL into the **YouTube URL** field (or right-click → Paste)
2. Choose a **Save Location** using the Browse button, or leave it as the default `downloads` folder
3. Select your **Format** — MP3 for audio, MP4 for video
4. Select your **Quality**
5. Click **DOWNLOAD**
6. A progress bar and status message will show the download in real time
7. When complete, a popup will appear with two options:
   - **View in Folder** — opens File Explorer directly to where the file was saved
   - **Download Next** — clears the URL field so you can start another download

---

## File Naming

Files are named using the video title plus the selected quality, for example:

```
Bohemian Rhapsody [320kbps].mp3
Bohemian Rhapsody [1080p].mp4
```

---

## Running from Source

If you'd prefer to run from source instead of using the exe:

### Requirements
- Python 3.x
- FFmpeg (install via `winget install ffmpeg`)

### Setup

```bash
# Clone the repo
git clone https://github.com/Che1ton6/coil-yttmp3-converter.git
cd coil-yttmp3-converter

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install customtkinter yt-dlp

# Run
python app.py
```

---

## Building the Exe Yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "CoilContentConverter" ^
  --add-binary "bin\ffmpeg.exe;bin" ^
  --add-binary "bin\ffprobe.exe;bin" ^
  --collect-data customtkinter ^
  --collect-all yt_dlp ^
  app.py
```

The exe will appear in the `dist/` folder.

---

## Keeping It Up to Date

YouTube occasionally changes how it works. If downloads start failing, update yt-dlp:

```bash
pip install --upgrade yt-dlp
```

---

## Legal Note

This tool is intended for personal use only. Downloading YouTube content may be subject to YouTube's Terms of Service. Only download content you have the right to download.
