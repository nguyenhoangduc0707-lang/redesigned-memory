import os
import json
import requests
from pathlib import Path
from src.config import ROOT_DIR

class NotebookLMPro:
    def __init__(self, notebook_id=None, export_path=None):
        self.notebook_id = notebook_id or os.environ.get("NOTEBOOKLM_NOTEBOOK_ID")
        if export_path:
            self.export_path = Path(export_path)
        else:
            root = Path(ROOT_DIR) if not isinstance(ROOT_DIR, Path) else ROOT_DIR
            self.export_path = root / "AI_OS_KERNEL_V3_FULL_EXPORT.md"

    def status(self):
        """Trả về trạng thái notebook (mock)"""
        return {
            "notebook_id": self.notebook_id,
            "export_path": str(self.export_path),
            "configured": self.notebook_id is not None,
            "cli_available": False,   # mock value
            "export_available": self.export_path.exists() if hasattr(self.export_path, "exists") else False
        }

    def ask(self, question):
        """Gửi câu hỏi đến notebook (mock)"""
        if not question:
            return {"answer": None, "error": "Missing question"}
        return {"answer": f"NotebookLM response to: {question}", "error": None}
