import requests
import json
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:2b")

def ask_ollama(prompt):
    try:
        resp = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=60)
        if resp.status_code == 200:
            return resp.json().get("response", "")
        else:
            return f"Error: HTTP {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"

def generate_improved_versions(original_code: str) -> list:
    prompts = {
        "speed": f"Optimize the following Python code for maximum SPEED (reduce latency, batch calls, use efficient algorithms). Return only the optimized code:\n{original_code}",
        "security": f"Rewrite the following Python code to be SECURE against injection, token leaks, and add input sanitization. Return only the secure code:\n{original_code}",
        "accuracy": f"Improve the ACCURACY of the following Python code by enhancing prompts, adding few-shot examples, and better context handling. Return only the improved code:\n{original_code}"
    }
    versions = []
    for i, (key, prompt) in enumerate(prompts.items(), 1):
        response = ask_ollama(prompt)
        versions.append({
            "version": i,
            "type": key,
            "code": response if not response.startswith("Error") else f"# {response}\n{original_code}"
        })
    return versions
