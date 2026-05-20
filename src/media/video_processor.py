import os
import tempfile
import requests
from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips

class VideoProcessor:
    def __init__(self, model_size="base", load_whisper=False):
        self.model_size = model_size
        self.whisper_model = None
        if load_whisper:
            self._load_whisper()
        print("VideoProcessor ready")

    def _load_whisper(self):
        if self.whisper_model is None:
            import whisper
            self.whisper_model = whisper.load_model(self.model_size)
        return self.whisper_model

    def create_video_from_images(self, image_paths, audio_path, output_path=None, duration_per_image=3, output=None):
        output_path = output_path or output
        if not output_path:
            raise ValueError("output_path is required")

        clips = []
        for img_path in image_paths:
            clip = ImageClip(img_path, duration=duration_per_image).resized(height=720)
            clips.append(clip)
        if not clips:
            raise ValueError("image_paths must contain at least one image")

        video = concatenate_videoclips(clips, method="compose")
        if audio_path and os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            video = video.with_audio(audio)
        video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        return output_path

    def extract_audio(self, video_path):
        import ffmpeg
        audio_path = tempfile.mktemp(suffix=".wav")
        try:
            ffmpeg.input(video_path).output(
                audio_path,
                acodec="pcm_s16le",
                ac=1,
                ar="16000",
            ).run(overwrite_output=True, quiet=True)
            return audio_path
        except Exception as exc:
            print(f"FFmpeg error: {exc}")
            return None

    def transcribe(self, audio_path, language="vi"):
        model = self._load_whisper()
        result = model.transcribe(audio_path, language=language)
        return result["text"]

    def process_video(self, source, is_url=False, language="vi"):
        temp_video = None
        video_path = source
        if is_url:
            response = requests.get(source, stream=True, timeout=30)
            response.raise_for_status()
            temp_video = tempfile.mktemp(suffix=".mp4")
            with open(temp_video, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            video_path = temp_video

        audio_path = self.extract_audio(video_path)
        if not audio_path:
            return {"error": "Failed to extract audio"}

        try:
            text = self.transcribe(audio_path, language)
            return {"transcript": text, "text": text, "language": language}
        finally:
            for path in (audio_path, temp_video):
                if path:
                    try:
                        os.remove(path)
                    except OSError:
                        pass

def get_processor(load_whisper=False):
    return VideoProcessor(load_whisper=load_whisper)
