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
        return {
            "notebook_id": self.notebook_id,
            "export_path": str(self.export_path),
            "configured": bool(self.notebook_id),
            "cli_available": False,
            "export_available": True
        }

    def ask(self, question):
        if not question or not question.strip():
            return {
                "answer": None,
                "error": "Missing question"
            }
        # Mock: xử lý câu hỏi bình thường
        return {
            "answer": f"NotebookLM response to: {question}",
            "error": None
        }
