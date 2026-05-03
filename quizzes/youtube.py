import os
import time

import yt_dlp


def extract_video_id(url):
    """
    Extracts the YouTube video ID from a supported URL.

    Args:
        url (str): YouTube URL.

    Returns:
        str | None: Extracted video ID or None if invalid.
    """
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None


def download_audio(url):
    """
    Downloads the audio of a YouTube video as an MP3 file.

    The YouTube URL is normalized and stored in the media folder
    with a unique filename.

    Args:
        url (str): YouTube video URL.

    Returns:
        str: Path to the downloaded MP3 file.

    Raises:
        ValueError: If the provided URL is not a valid YouTube URL.
    """
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    os.makedirs("media", exist_ok=True)

    unique_name = f"{video_id}_{int(time.time())}"
    clean_url = f"https://www.youtube.com/watch?v={video_id}"
    output_template = f"media/{unique_name}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([clean_url])

    return f"media/{unique_name}.mp3"