import os
import yt_dlp
from pathlib import Path
import uuid

DATA_DIR = Path("data/raw_videos")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_video(url, output_dir=DATA_DIR):
    """
    Tải video từ URL (hỗ trợ YouTube, Facebook, TikTok, ...)
    Trả về đường dẫn file video đã tải.
    """
    output_template = str(output_dir / "%(title)s_%(id)s.%(ext)s")
    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            # Nếu có nhiều format, ưu tiên mp4
            if not os.path.exists(filepath) and 'entries' in info:
                # playlist case, lấy video đầu tiên
                filepath = ydl.prepare_filename(info['entries'][0])
            return filepath
    except Exception as e:
        print(f"Lỗi tải video: {e}")
        return None

def add_local_video(file_path, output_dir=DATA_DIR):
    """Copy video local vào thư mục raw"""
    import shutil
    dest = output_dir / Path(file_path).name
    shutil.copy2(file_path, dest)
    return str(dest)

if __name__ == "__main__":
    # Test thử
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    path = download_video(test_url)
    print(f"Đã tải: {path}")