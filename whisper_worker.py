import sys
import os
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: whisper_worker.py <audio_file>")
        sys.exit(1)
    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"Error: File {audio_file} not found")
        sys.exit(1)
    try:
        import whisper
        # Model small: cân bằng giữa chất lượng và tốc độ, dùng ~2.5GB RAM
        model = whisper.load_model("medium")
        result = model.transcribe(audio_file)
        print(result["text"])
        sys.exit(0)
    except ImportError:
        print("Whisper not installed. Please install: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Whisper error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()