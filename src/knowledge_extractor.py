import json
import requests
import os
from pathlib import Path

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:2b")

def extract_knowledge(text, max_length=4000):
    """
    Gửi transcript đến Ollama, yêu cầu trả về JSON có cấu trúc.
    """
    # Cắt ngắn text nếu quá dài
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    prompt = f"""Bạn là SEN, trợ lý AI. Hãy phân tích văn bản sau và trả về JSON có cấu trúc:

{{
  "summary": "tóm tắt 3-5 câu bằng tiếng Việt",
  "key_points": ["điểm 1", "điểm 2", "điểm 3"],
  "entities": {{"person": [], "org": [], "concept": []}},
  "topics": ["chủ đề 1", "chủ đề 2"]
}}

Chỉ trả về JSON, không thêm text khác. Văn bản:
{text}
"""
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        if resp.status_code == 200:
            result = resp.json().get("response", "")
            # Tìm và parse JSON từ response (có thể có text thừa)
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"error": "No JSON found", "raw": result}
        else:
            return {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def process_transcript_file(transcript_path, output_dir="data/knowledge"):
    """
    Đọc transcript từ file, gọi extract, lưu kết quả JSON.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read()
    knowledge = extract_knowledge(text)
    output_file = output_dir / f"{Path(transcript_path).stem}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(knowledge, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu knowledge: {output_file}")
    return knowledge

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        transcript_file = sys.argv[1]
        process_transcript_file(transcript_file)
    else:
        print("Usage: python src/knowledge_extractor.py <transcript_file>")