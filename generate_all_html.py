import os
import sys
import time
from google import genai
from config import API_KEY, MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS

def generate_html_content(prompt_text, retries=3, delay=5):
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY not set")
    client = genai.Client(api_key=API_KEY)
    for attempt in range(retries):
        try:
            print(f"-> Gửi yêu cầu (Lần {attempt+1}/{retries})...")
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt_text,
                config={
                    "temperature": TEMPERATURE,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                }
            )
            if response and response.text:
                content = response.text.strip()
                if content.startswith("```html"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                return content.strip()
        except Exception as e:
            print(f"Lỗi: {e}")
            if attempt < retries-1:
                time.sleep(delay)
            else:
                return None

def main():
    print("=== TỰ ĐỘNG SINH HTML ===")
    prompts = {
        "index.html": "Trang chủ landing page hiện đại, giao diện tối giản, thanh điều hướng, responsive, HTML và Tailwind CSS.",
        "about.html": "Trang giới thiệu bản thân chuyên nghiệp, bố cục grid, kỹ năng và kinh nghiệm."
    }
    for filename, prompt in prompts.items():
        print(f"\nXử lý {filename}...")
        html = generate_html_content(prompt)
        if html:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Đã lưu {filename}")
        else:
            print(f"Bỏ qua {filename}")

if __name__ == "__main__":
    main()
