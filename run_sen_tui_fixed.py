#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
import os
import sys

sys.path.insert(0, os.getcwd())

# --- Mock user manager ---
class MockUser:
    def is_authenticated(self):
        return True
    id = "mock_user"
authenticate_user = lambda u, p: MockUser()

# --- SEN Brain Mock (nếu không có) ---
try:
    from sen_brain import default_brain as brain
except ImportError:
    class MockBrain:
        def ask(self, query):
            return f"Xin chào, tôi là SEN AI (mock). Bạn hỏi: {query}"
    brain = MockBrain()

# --- Config ---
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

class LoginDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Đăng nhập SEN AI")
        tk.Label(self.dialog, text="Username:").grid(row=0, column=0)
        self.user_entry = tk.Entry(self.dialog)
        self.user_entry.grid(row=0, column=1)
        tk.Label(self.dialog, text="Password:").grid(row=1, column=0)
        self.pwd_entry = tk.Entry(self.dialog, show="*")
        self.pwd_entry.grid(row=1, column=1)
        tk.Button(self.dialog, text="OK", command=self.ok).grid(row=2, column=0)
        tk.Button(self.dialog, text="Cancel", command=self.cancel).grid(row=2, column=1)
        self.result = None
        parent.wait_window(self.dialog)

    def ok(self):
        self.result = authenticate_user(self.user_entry.get(), self.pwd_entry.get())
        self.dialog.destroy()

    def cancel(self):
        self.result = None
        self.dialog.destroy()

class ChatWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        root.title(f"SEN AI - {AI_IDENTITY}")
        root.geometry("600x500")
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='normal')
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X, padx=5, pady=5)
        self.entry.bind("<Return>", self.send)
        self.send_button = tk.Button(root, text="Gửi", command=self.send)
        self.send_button.pack(pady=5)

    def send(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        self.text_area.insert(tk.END, f"👤 {self.user.id}: {msg}\n")
        self.entry.delete(0, tk.END)
        self.text_area.insert(tk.END, "🤖 SEN AI: Đang suy nghĩ...\n")
        self.root.update()
        # Gọi Ollama hoặc brain
        reply = ask_ollama(msg)
        self.text_area.insert(tk.END, f"🤖 SEN AI: {reply}\n\n")
        self.text_area.see(tk.END)

def main():
    root = tk.Tk()
    root.withdraw()
    login = LoginDialog(root)
    if login.result is None:
        return
    root.deiconify()
    app = ChatWindow(root, login.result)
    root.mainloop()

if __name__ == "__main__":
    main()
