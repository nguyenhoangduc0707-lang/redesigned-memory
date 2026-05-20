import os
import whisper
from pathlib import Path

# Tương thích moviepy 1.x và 2.x
try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
except ImportError:
    try:
        from moviepy import VideoFileClip
    except ImportError:
        raise ImportError("Không thể import VideoFileClip từ moviepy. Hãy cài moviepy==1.0.3")

AUDIO_DIR = Path("data/extracted_audio")
TRANSCRIPT_DIR = Path("data/transcripts")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

# Tải model Whisper (base cho tiếng Việt, có thể đổi thành "small" nếu RAM nhiều)
model = whisper.load_model("base")

def extract_audio(video_path, output_dir=AUDIO_DIR):
    """Trích xuất audio từ video, lưu file WAV"""
    video = VideoFileClip(video_path)
    audio_path = output_dir / f"{Path(video_path).stem}.wav"
    video.audio.write_audiofile(str(audio_path), fps=16000, verbose=False, logger=None)
    video.close()
    return str(audio_path)

def transcribe_audio(audio_path, language="vi"):
    """Dùng Whisper để transcribe, trả về text"""
    result = model.transcribe(audio_path, language=language)
    return result["text"]

def process_video(video_path, save_transcript=True):
    """Pipeline hoàn chỉnh: audio -> transcript"""
    print(f"Đang xử lý: {video_path}")
    audio_path = extract_audio(video_path)
    transcript = transcribe_audio(audio_path)
    if save_transcript:
        transcript_file = TRANSCRIPT_DIR / f"{Path(video_path).stem}.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        print(f"Đã lưu transcript: {transcript_file}")
    return transcript