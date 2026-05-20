#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
import os
import sys

sys.path.insert(0, os.getcwd())

# Import SEN Brain
try:
    from sen_brain import default_brain as brain
    BRAIN_READY = True
except Exception as e:
    BRAIN_READY = False
    print(f"⚠️ Lỗi SEN Brain: {e}")

# Import user manager with mock fallback
try:
    from src.user_manager import authenticate_user
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False
    class MockUser:
        def is_authenticated(self):
            return True
        id = "mock_user"
    authenticate_user = lambda u, p: MockUser()
    print("⚠️ Không có user_manager, sử dụng mock.")

try:
    from src.config import AI_IDENTITY, FOUNDER_INFO, DEDICATION
except ImportError:
    AI_IDENTITY = "SEN AI"
    FOUNDER_INFO = "Nguyễn Hoàng Đức"
    DEDICATION = "Innovation for Future"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:2b")

def ask_ollama(prompt):
    try:
        resp = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=120)
        if resp.status_code == 200:
            return resp.json().get("response", "Xin lỗi, tôi không có câu trả lời.")
        else:
            return f"Lỗi Ollama (HTTP {resp.status_code})"
    except Exception as e:
        return f"Lỗi kết nối Ollama: {e}"

# Các lớp LoginDialog, ChatWindow, main... (giữ nguyên phần còn lại của file)
# Lưu ý: Bạn cần bổ sung các lớp này nếu file hiện tại thiếu.
# Nếu đã có sẵn, hãy giữ nguyên phần cuối.

