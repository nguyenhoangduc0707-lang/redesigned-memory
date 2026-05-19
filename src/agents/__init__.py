import os
import shlex
import subprocess

import requests

from src.config import (
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
    EXTERNAL_LLM_PROVIDER,
    LOCAL_LLM_COMMAND,
    LOCAL_LLM_TIMEOUT,
    OPENAI_MODEL,
)


class LocalLLMController:
    def __init__(self, command=LOCAL_LLM_COMMAND, timeout=LOCAL_LLM_TIMEOUT):
        self.command = command
        self.timeout = timeout

    def ask(self, prompt, system_prompt=None):
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        command = shlex.split(self.command) + [full_prompt]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                encoding="utf-8",
                errors="replace",
            )
            if result.returncode != 0:
                return {"ok": False, "source": "local", "error": result.stderr.strip(), "answer": None}
            return {"ok": True, "source": "local", "error": None, "answer": result.stdout.strip()}
        except Exception as exc:
            return {"ok": False, "source": "local", "error": str(exc), "answer": None}


class ExternalLLMFallback:
    def ask(self, prompt, system_prompt=None):
        provider = EXTERNAL_LLM_PROVIDER.lower()
        if provider == "openai":
            return self._ask_openai(prompt, system_prompt)
        return self._ask_deepseek(prompt, system_prompt)

    def _ask_deepseek(self, prompt, system_prompt=None):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            return {"ok": False, "source": "deepseek", "error": "Missing DEEPSEEK_API_KEY", "answer": None}
        return self._chat_completion(DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, api_key, prompt, system_prompt, "deepseek")

    def _ask_openai(self, prompt, system_prompt=None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"ok": False, "source": "openai", "error": "Missing OPENAI_API_KEY", "answer": None}
        return self._chat_completion("https://api.openai.com/v1", OPENAI_MODEL, api_key, prompt, system_prompt, "openai")

    def _chat_completion(self, base_url, model, api_key, prompt, system_prompt, source):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        try:
            response = requests.post(
                f"{base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "temperature": 0.2},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            return {"ok": True, "source": source, "error": None, "answer": answer}
        except Exception as exc:
            return {"ok": False, "source": source, "error": str(exc), "answer": None}


class Agent:
    def __init__(self, name, local_controller=None, fallback=None):
        self.name = name
        self.local_controller = local_controller or LocalLLMController()
        self.fallback = fallback or ExternalLLMFallback()

    def run(self, task):
        system = f"You are {self.name}, an AI_OS_KERNEL_V3 local-first worker."
        result = self.local_controller.ask(task, system_prompt=system)
        if result["ok"]:
            return {"status": "ok", "task": task, "source": result["source"], "answer": result["answer"]}

        fallback = self.fallback.ask(task, system_prompt=system)
        if fallback["ok"]:
            return {"status": "ok", "task": task, "source": fallback["source"], "answer": fallback["answer"]}

        return {
            "status": "error",
            "task": task,
            "source": "none",
            "error": {"local": result["error"], "fallback": fallback["error"]},
        }


def run_all_agents():
    agents = [Agent("LocalLogicController"), Agent("CampaignAssistant")]
    return [agent.run("default task") for agent in agents]


def get_agent(agent_name):
    return Agent(agent_name)
