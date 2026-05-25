# YT Downloader

A desktop app to download YouTube videos and playlists as MP3 or MP4, at any quality — built with Python.

---

## What It Does

- Download any YouTube video or playlist by pasting its URL
- Choose between MP3 (audio) or MP4 (video)
- Select your preferred quality (320kbps / 192kbps / 128kbps for MP3 — or 4K / 1080p / 720p / 480p / 360p for MP4)
- Choose exactly where to save your files using a folder browser
- Playlists automatically get saved into their own named folder
- Files are named with their quality so multiple versions never overwrite each other
- A popup appears when done, letting you open the folder or start a new download

---

## Requirements

Before running the app, make sure you have the following installed on your computer:

### 1. Python 3.x
Download from: https://python.org/downloads

> During installation, tick **"Add Python to PATH"** — this is important!

Verify it's installed by opening a terminal and typing:
```
python --version
```

### 2. ffmpeg
Required for MP3 conversion. Install it via Windows terminal:
```
winget install ffmpeg
```

Verify it's installed:
```
ffmpeg -version
```

### 3. VS Code (recommended)
Download from: https://code.visualstudio.com

---

## Setup Instructions

### Step 1 — Open the project folder in VS Code
Go to **File → Open Folder** and select the `YtMp3 Converter` folder.

### Step 2 — Open the terminal
Press **Ctrl + `** (backtick key, top-left under Escape).

### Step 3 — Activate the virtual environment
```
venv\Scripts\activate
```

You should see `(venv)` appear at the start of the terminal line.

> If you get a permissions error, run this first:
> ```
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> ```
> Then try activating again.

### Step 4 — Install the required packages (first time only)
```
pip install customtkinter yt-dlp
```

### Step 5 — Run the app
```
python app.py
```

A desktop window will open and the app is ready to use.

---

## How to Use

1. Paste a YouTube video or playlist URL into the **YouTube URL** field
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

This means you can download the same video at different qualities without them overwriting each other.

---

## Playlist Downloads

If you paste a playlist URL, the app will:
1. Automatically detect it's a playlist
2. Create a folder named after the playlist inside your save location
3. Download every video in the playlist into that folder

---

## Project Structure

```
YtMp3 Converter/
├── app.py              ← Main application code
├── downloads/          ← Default folder for downloaded files
├── templates/          ← (Unused in desktop version)
└── venv/               ← Python virtual environment
```

---

## Keeping It Up to Date

YouTube occasionally changes how it works, which can cause downloads to fail. If that happens, update yt-dlp by running:
```
pip install --upgrade yt-dlp
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `No module named 'flask'` or `customtkinter` | Activate venv first: `venv\Scripts\activate`, then `pip install customtkinter yt-dlp` |
| `ffmpeg not recognized` | Restart VS Code after installing ffmpeg |
| Download fails or errors | Run `pip install --upgrade yt-dlp` |
| App window doesn't open | Make sure you're running `python app.py` with venv active |

---

## Legal Note

This tool is intended for personal use only. Downloading YouTube content may be subject to YouTube's Terms of Service. Only download content you have the right to download.
