import os
import tempfile
import uuid

from gtts import gTTS


def text_to_speech(text, lang="vi", output_dir="audio", save_path=None):
    if save_path:
        filepath = save_path
        parent = os.path.dirname(filepath)
        if parent:
            os.makedirs(parent, exist_ok=True)
    elif output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, f"{uuid.uuid4().hex}.mp3")
    else:
        filepath = tempfile.mktemp(suffix=".mp3")

    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        return filepath
    except Exception as exc:
        print(f"TTS error: {exc}")
        return None


def speak(text, lang="vi"):
    audio_file = text_to_speech(text, lang=lang, output_dir=None)
    if not audio_file:
        return None

    try:
        import pygame

        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
    except Exception as exc:
        print(f"Error playing audio: {exc}")
    finally:
        try:
            os.remove(audio_file)
        except OSError:
            pass
    return audio_file
