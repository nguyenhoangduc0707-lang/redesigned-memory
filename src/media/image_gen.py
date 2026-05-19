from pathlib import Path
from textwrap import shorten
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from src.config import ROOT_DIR


OUTPUT_DIR = ROOT_DIR / "static" / "generated"


def _font(size):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def create_thumbnail(title, subtitle="", output_dir=OUTPUT_DIR, size=(1280, 720), accent=(13, 148, 136)):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.new("RGB", size, color=(18, 24, 38))
    draw = ImageDraw.Draw(image)
    width, height = size

    draw.rectangle([0, 0, width, height], fill=(18, 24, 38))
    draw.rectangle([0, height - 140, width, height], fill=accent)
    draw.rectangle([48, 48, width - 48, height - 48], outline=(255, 255, 255), width=3)

    title_text = shorten(title or "AI_OS Campaign", width=56, placeholder="...")
    subtitle_text = shorten(subtitle or "Affiliate automation", width=88, placeholder="...")

    draw.text((88, 160), title_text, font=_font(64), fill=(255, 255, 255))
    draw.text((92, 260), subtitle_text, font=_font(34), fill=(210, 226, 235))
    draw.text((92, height - 95), "AI_OS_KERNEL_V3", font=_font(42), fill=(255, 255, 255))

    output_path = output_dir / f"thumb_{uuid4().hex}.png"
    image.save(output_path)
    return str(output_path)


def create_banner(title, subtitle="", output_dir=OUTPUT_DIR):
    return create_thumbnail(title, subtitle, output_dir=output_dir, size=(1600, 500), accent=(79, 70, 229))


if __name__ == "__main__":
    print(create_thumbnail("AI_OS Campaign", "Auto generated thumbnail"))
