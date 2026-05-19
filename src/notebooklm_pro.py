import json
import os
import shutil
import subprocess
from pathlib import Path

from src.config import ROOT_DIR


class NotebookLMPro:
    def __init__(self, notebook_id=None, export_path=None):
        self.notebook_id = notebook_id or os.environ.get("NOTEBOOKLM_NOTEBOOK_ID")
        self.export_path = Path(export_path) if export_path else ROOT_DIR / "AI_OS_KERNEL_V3_FULL_EXPORT.md"
        self.cli_path = shutil.which("nlm")

    def status(self):
        return {
            "configured": bool(self.notebook_id),
            "cli_available": bool(self.cli_path),
            "notebook_id": self.notebook_id,
            "export_available": self.export_path.exists(),
            "export_path": str(self.export_path),
        }

    def ask(self, question, timeout=120):
        question = (question or "").strip()
        if not question:
            return {"answer": None, "error": "Missing question", "source": None}

        if self.notebook_id and self.cli_path:
            cli_result = self._ask_cli(question, timeout)
            if cli_result.get("answer"):
                return cli_result
            if not self.export_path.exists():
                return cli_result

        return self._ask_export(question)

    def _ask_cli(self, question, timeout):
        command = [
            self.cli_path,
            "notebook",
            "query",
            self.notebook_id,
            question,
            "--json",
            "--timeout",
            str(timeout),
        ]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout + 5,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                return {"answer": None, "error": result.stderr.strip(), "source": "notebooklm_cli"}

            payload = json.loads(result.stdout)
            if payload.get("status") == "error":
                return {"answer": None, "error": payload.get("error"), "source": "notebooklm_cli"}

            value = payload.get("value", {})
            return {
                "answer": value.get("answer", ""),
                "conversation_id": value.get("conversation_id"),
                "error": None,
                "source": "notebooklm_cli",
            }
        except Exception as exc:
            return {"answer": None, "error": str(exc), "source": "notebooklm_cli"}

    def _ask_export(self, question):
        if not self.export_path.exists():
            return {
                "answer": None,
                "error": "NotebookLM CLI is not configured and project export is missing",
                "source": "local_export",
            }

        content = self.export_path.read_text(encoding="utf-8", errors="replace")
        snippets = self._find_snippets(content, question)
        if not snippets:
            snippets = [content[:1800]]

        answer = "\n\n".join(snippets)
        return {
            "answer": answer,
            "error": None,
            "source": "local_export",
        }

    def _find_snippets(self, content, question):
        terms = [term.lower() for term in question.replace("_", " ").split() if len(term) >= 4]
        if not terms:
            return []

        lower_content = content.lower()
        snippets = []
        for term in terms[:8]:
            index = lower_content.find(term)
            if index < 0:
                continue
            start = max(0, index - 500)
            end = min(len(content), index + 1200)
            snippet = content[start:end].strip()
            if snippet and snippet not in snippets:
                snippets.append(snippet)
            if len(snippets) >= 3:
                break
        return snippets
