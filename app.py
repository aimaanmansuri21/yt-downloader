
import streamlit as st
import os
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

# 🔧 Force yt-dlp to use bundled ffmpeg binary
os.environ["PATH"] = os.path.abspath("bin") + os.pathsep + os.environ["PATH"]

st.title("YouTube Video Downloader (Self-Contained)")

url = st.text_input("Enter YouTube Video URL:")

quality = st.selectbox("Choose Quality:", ["Best Available (Auto)", "4K (if available)", "1080p", "Audio Only"])

format_map = {
    "Best Available (Auto)": "bestvideo+bestaudio/best",
    "4K (if available)": "bestvideo[height<=2160]+bestaudio/best[height<=2160]",
    "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "Audio Only": "bestaudio"
}

def download_hook(d):
    if d['status'] == 'downloading':
        progress = d.get('_percent_str', '0.0%').strip()
        st.session_state.progress_text.text(f"Downloading... {progress}")
    elif d['status'] == 'finished':
        st.session_state.progress_text.text("Download complete!")

if 'progress_text' not in st.session_state:
    st.session_state.progress_text = st.empty()

if st.button("Download"):
    if url:
        output_path = "downloads"
        os.makedirs(output_path, exist_ok=True)
        selected_format = format_map[quality]
        merge_format = "mp3" if quality == "Audio Only" else "mp4"
        ydl_opts = {
            'format': selected_format,
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'merge_output_format': merge_format,
            'progress_hooks': [download_hook]
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except DownloadError as e:
            st.error(f"Download failed: {e}")
    else:
        st.warning("Please enter a valid URL.")
