import sys
import os   # <--- THÊM DÒNG NÀY
sys.path.insert(0, '.')

from src.video_ingestor import download_video, add_local_video
from src.video_transcriber import process_video
import argparse

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="URL video để tải")
    group.add_argument("--file", help="Đường dẫn video local")
    parser.add_argument("--save-transcript", action="store_true", default=True)
    args = parser.parse_args()

    if args.url:
        video_path = download_video(args.url)
    else:
        video_path = add_local_video(args.file)

    if not video_path or not os.path.exists(video_path):
        print("Không thể lấy video.")
        return

    transcript = process_video(video_path, save_transcript=args.save_transcript)
    print("\n=== TRANSCRIPT ===")
    print(transcript)

if __name__ == "__main__":
    main()