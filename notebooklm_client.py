import requests
import json
import os

class NotebookLMClient:
    def __init__(self, server_url="http://localhost:8800"):
        self.server_url = server_url
        self.available = False
        try:
            # Kiểm tra server có phản hồi không
            r = requests.get(f"{server_url}/health", timeout=2)
            if r.status_code == 200:
                self.available = True
        except:
            pass

    def ask(self, question):
        if not self.available:
            # Fallback sang Ollama
            return self._ask_ollama(question)
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "ask",
                    "arguments": {"question": question}
                },
                "id": 1
            }
            resp = requests.post(f"{self.server_url}/jsonrpc", json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if "result" in data:
                    return {"answer": data["result"]["content"][0]["text"]}
                else:
                    return {"answer": "Không nhận được câu trả lời từ NotebookLM."}
            else:
                return self._ask_ollama(question)
        except Exception as e:
            return self._ask_ollama(question)

    def _ask_ollama(self, question):
        # Dùng Ollama làm fallback
        try:
            import requests
            resp = requests.post("http://localhost:11434/api/generate",
                                 json={"model": "gemma2:2b", "prompt": question, "stream": False}, timeout=30)
            return {"answer": resp.json().get("response", "Xin lỗi, tôi không có câu trả lời.")}
        except:
            return {"answer": "Lỗi kết nối. Vui lòng kiểm tra Ollama hoặc NotebookLM."}

default_client = NotebookLMClient()