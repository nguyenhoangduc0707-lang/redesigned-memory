# orchestrator.py
import os
import subprocess
import json
from langchain.llms import OpenAI  # Dùng cho DeepSeek (compatible)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.router import RouterChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt import MultiPromptChain

# Cấu hình DeepSeek (dùng OpenAI endpoint)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"  # hoặc endpoint tương tự
deepseek_llm = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    model="deepseek-chat",
    temperature=0.2
)

# NotebookLM client (dùng CLI)
class NotebookLMClient:
    def __init__(self, notebook_id=None):
        self.notebook_id = notebook_id or os.environ.get("NOTEBOOKLM_NOTEBOOK_ID")
        if not self.notebook_id:
            raise ValueError("Missing NOTEBOOKLM_NOTEBOOK_ID")
    def ask(self, question):
        cmd = ['nlm', 'notebook', 'query', self.notebook_id, question, '--json']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            return f"Lỗi NotebookLM: {result.stderr}"
        data = json.loads(result.stdout)
        return data.get("value", {}).get("answer", "Không có câu trả lời")

# Định nghĩa các prompt template cho từng loại
deepseek_prompt = PromptTemplate(
    input_variables=["input"],
    template="Bạn là chuyên gia kỹ thuật. Hãy xử lý yêu cầu sau bằng cách sinh code, lệnh PowerShell, hoặc phân tích dữ liệu cụ thể. Chỉ trả lời chính xác, có thể kèm code.\n\nYêu cầu: {input}\n\nTrả lời:"
)

notebook_prompt = PromptTemplate(
    input_variables=["input"],
    template="Bạn là trợ lý phân tích tài liệu. Dựa vào nội dung dự án AI_OS_KERNEL_V3, hãy diễn giải, tóm tắt, hoặc đưa ra insight cho câu hỏi sau:\n\n{input}\n\nTrả lời (bằng tiếng Việt, rõ ràng):"
)

# Các chain con
deepseek_chain = LLMChain(llm=deepseek_llm, prompt=deepseek_prompt)
notebook_chain = LLMChain(llm=NotebookLMClient().ask, prompt=notebook_prompt)  # Chú ý: cần wrapper

# Router: dùng LLM để phân loại câu hỏi
router_template = """Phân loại câu hỏi sau đây vào một trong hai loại: "deepseek" (nếu yêu cầu về code, lệnh, dữ liệu, tự động hóa) hoặc "notebook" (nếu yêu cầu về tài liệu, báo cáo, insight, giải thích dự án).

Câu hỏi: {input}

Chỉ trả lời duy nhất một từ: "deepseek" hoặc "notebook".
"""

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"]
)
router_chain = LLMChain(llm=deepseek_llm, prompt=router_prompt, output_parser=RouterOutputParser())

# Chain tổng hợp
class Orchestrator:
    def __init__(self):
        self.router = router_chain
        self.deepseek = deepseek_chain
        self.notebook = NotebookLMClient()

    def route(self, question):
        decision = self.router.run(question).strip().lower()
        if "deepseek" in decision:
            return self.deepseek.run(question)
        else:
            return self.notebook.ask(question)

# Sử dụng
if __name__ == "__main__":
    orch = Orchestrator()
    while True:
        q = input("Hỏi SEN: ")
        if q.lower() in ('exit','quit'): break
        print("SEN:", orch.route(q))