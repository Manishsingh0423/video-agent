import yt_dlp
import os
import shutil
from pydub import AudioSegment

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

def chunks_audio(wav_path:str, chunk_lenght_minutes: int = 10)-> list:


    audio = AudioSegment.from_wav(wav_path)
    chunk_length_ms = chunk_lenght_minutes * 60 * 1000
    chunks = []
    for i, start in enumerate(range(0, len(audio), chunk_length_ms)):
        chunk = audio[start: start + chunk_length_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks 





if __name__ == "__main__":
    data = download_youtube_audio("https://www.youtube.com/watch?v=mtiOK2QG9Q0")
    data_final = convert_to_wav(data)
    print(chunks_audio(data_final))