# notebook_rag.py
import os
import google.generativeai as genai
from pathlib import Path

PROJECT_ROOT = Path("C:/AI_OS_KERNEL_V3")
EXPORT_FILE = PROJECT_ROOT / "AI_OS_KERNEL_V3_FULL_EXPORT.md"
GEMINI_MODEL = "gemini-1.5-flash"  # hoặc gemini-1.5-pro

class NotebookRAG:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.context = self._load_context()

    def _load_context(self):
        if not EXPORT_FILE.exists():
            print(f"⚠️ Export file not found: {EXPORT_FILE}")
            return ""
        with open(EXPORT_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        # Giới hạn context (Gemini 1.5 hỗ trợ 1M tokens, an toàn)
        return content

    def ask(self, question):
        if not self.context:
            return "Chưa có dữ liệu dự án. Hãy chạy export_to_notebooklm.py trước."
        prompt = f"""
Dựa vào nội dung dự án AI_OS_KERNEL_V3 dưới đây, hãy trả lời câu hỏi của người dùng bằng tiếng Việt, ngắn gọn và chính xác.

NỘI DUNG DỰ ÁN:
{self.context[:500000]}  # Giới hạn 500k ký tự

CÂU HỎI: {question}

TRẢ LỜI:
"""
        response = self.model.generate_content(prompt)
        return response.text

# Ví dụ sử dụng
if __name__ == "__main__":
    rag = NotebookRAG()
    while True:
        q = input("Hỏi về dự án: ")
        if q.lower() in ("exit", "quit"):
            break
        print("SEN: ", rag.ask(q))