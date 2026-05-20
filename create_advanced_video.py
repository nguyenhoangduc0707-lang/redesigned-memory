import os
from moviepy import *
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import uuid

# ---------------------------
# 1. Tạo nhiều ảnh với văn bản khác nhau
# ---------------------------
def create_title_image(text, bg_color=(20, 30, 50), text_color=(255, 255, 255), size=(1280, 720)):
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    out_path = f"static/generated/title_{uuid.uuid4().hex}.png"
    img.save(out_path)
    return out_path

def create_slide(content, bg_color=(40, 40, 60), accent_color=(13, 148, 136), size=(1280, 720)):
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    draw.rectangle([50, 50, size[0]-50, size[1]-50], outline=accent_color, width=5)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    lines = [content[i:i+40] for i in range(0, len(content), 40)]
    y = 200
    for line in lines:
        draw.text((100, y), line, font=font, fill=(255,255,255))
        y += 60
    out_path = f"static/generated/slide_{uuid.uuid4().hex}.png"
    img.save(out_path)
    return out_path

# ---------------------------
# 2. Tạo âm thanh lồng tiếng
# ---------------------------
def create_voiceover(text, filename=None):
    if filename is None:
        filename = f"audio/voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang='vi', slow=False)
    tts.save(filename)
    return filename

# ---------------------------
# 3. Tạo video từ danh sách ảnh và âm thanh (không dùng hiệu ứng fade)
# ---------------------------
def create_video_from_assets(image_paths, audio_path, output_path, durations=None):
    if durations is None:
        durations = [3] * len(image_paths)
    clips = []
    for i, path in enumerate(image_paths):
        clip = ImageClip(path, duration=durations[i])
        clips.append(clip)
    video = concatenate_videoclips(clips, method="compose")
    if audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        video = video.with_audio(audio)
    video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    return output_path

# ---------------------------
# 4. Hàm chính
# ---------------------------
def main():
    print("🎬 Tạo video nâng cao (tương thích moviepy 2.x)...")
    
    slide1 = create_title_image("SEN AI - Báo cáo chiến dịch")
    slide2 = create_slide("Doanh số tháng 5 tăng 32% nhờ tối ưu AI.")
    slide3 = create_slide("Kênh Facebook đạt 15.000 lượt tiếp cận, ROAS 2.5x")
    slide4 = create_slide("TikTok Shop: 1.200 đơn hàng, tăng 47% so với tháng trước")
    slide5 = create_title_image("Cảm ơn Sếp Đức đã tin tưởng!")
    
    script = ("Xin chào Sếp Đức. Đây là báo cáo chiến dịch tự động từ SEN AI. "
              "Doanh số tháng Năm tăng 32 phần trăm nhờ tối ưu AI. "
              "Kênh Facebook đạt 15 nghìn lượt tiếp cận, tỷ suất hoàn vốn quảng cáo đạt hai phẩy năm lần. "
              "TikTok Shop có một nghìn hai trăm đơn hàng, tăng 47 phần trăm so với tháng trước. "
              "Cảm ơn Sếp đã đồng hành cùng SEN.")
    audio = create_voiceover(script)
    
    images = [slide1, slide2, slide3, slide4, slide5]
    durations = [4, 5, 5, 5, 3]
    output_video = "sen_advanced_report.mp4"
    
    create_video_from_assets(images, audio, output_video, durations)
    print(f"✅ Video đã tạo: {output_video}")
    import subprocess
    subprocess.Popen(f'explorer /select,"{os.path.abspath(output_video)}"')

if __name__ == "__main__":
    main()