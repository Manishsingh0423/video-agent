import yt_dlp
import os
import shutil

Download_DIR = "./downloads"
os.makedirs(Download_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(Download_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_filename = ydl.prepare_filename(info_dict)
        filename = os.path.splitext(downloaded_filename)[0] + ".mp3"
        return filename


def convert_to_wav(input_file: str) -> str:
    """convert input audio file to wav formate using pydub """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Audio file not found: {os.path.abspath(input_file)}")

    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise RuntimeError("FFmpeg is required to convert audio. Install ffmpeg and make sure ffmpeg and ffprobe are on PATH.")

    from pydub import AudioSegment

    output_file = os.path.splitext(input_file)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_file, format="wav")
    return output_file


if __name__ == "__main__":
    data = download_youtube_audio("https://www.youtube.com/watch?v=IVGjBxqygmI")
    print(convert_to_wav(data))
