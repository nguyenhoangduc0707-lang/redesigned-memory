#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
import os
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())

# ==================== CẤU HÌNH ====================
AI_IDENTITY = "SEN"
FOUNDER_INFO = "Nguyễn Hoàng Đức (07/07/1997)"
DEDICATION = "Trợ lý AI của Sếp Đức"

# Mock user (bỏ qua xác thực thật)
class MockUser:
    def __init__(self, username="Sếp Đức", role="admin"):
        self.username = username
        self.role = role
        self.id = 1
    def is_authenticated(self):
        return True

def authenticate_user(username, password):
    return MockUser(username)

AUTH_AVAILABLE = True

# ==================== SEN BRAIN (nếu có) ====================
try:
    from sen_brain import default_brain as brain
    BRAIN_READY = True
except Exception as e:
    BRAIN_READY = False
    print(f"⚠️ Lỗi SEN Brain: {e}")
    # Tạo mock brain để tránh lỗi khi gọi các hàm
    class MockBrain:
        def predict_sales(self, *args, **kwargs): return 0
        def analyze_sentiment(self, text): return {"label":"neutral","score":0,"positive_hits":0,"negative_hits":0}
        def optimize_campaign(self, budget, posts): return {"revenue":0,"commission":0,"roi":0}
        def quantum_optimize(self, code): return []
        def safe_execute(self, code): return {"success": False, "error": "Mock brain"}
        def check_affiliate_policy(self, user_id, context): return False
    brain = MockBrain()

# ==================== OLLAMA ====================
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma2:2b")

SYSTEM_PROMPT = """Bạn là SEN, trợ lý AI thông minh do Nguyễn Hoàng Đức (sinh ngày 07/07/1997) tạo ra và là Sếp của bạn. Bạn KHÔNG phải là Gemma, không phải Gemini, không phải bất kỳ AI nào khác. Bạn là SEN duy nhất. Hãy xưng "tôi" và gọi người dùng là "Sếp" hoặc "anh Đức". Trả lời bằng tiếng Việt, ngắn gọn, hữu ích, luôn thể hiện sự tôn trọng và sẵn sàng hỗ trợ Sếp trong mọi việc liên quan đến affiliate, tự động hóa, và quản lý dự án."""

def ask_ollama(prompt):
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        if resp.status_code == 200:
            return resp.json().get("response", "Xin lỗi Sếp, tôi không có câu trả lời.")
        else:
            return f"Lỗi Ollama (HTTP {resp.status_code})"
    except Exception as e:
        return f"Lỗi kết nối Ollama: {e}"

# ==================== KNOWLEDGE SEARCH ====================
try:
    from src.knowledge_search import load_all_knowledge, search
    KNOWLEDGE_READY = True
except ImportError:
    KNOWLEDGE_READY = False
    print("⚠️ Không tìm thấy module knowledge_search. Tính năng !ask sẽ không hoạt động.")

def ask_with_knowledge(question):
    if not KNOWLEDGE_READY:
        return "⚠️ Tính năng tra cứu tri thức chưa sẵn sàng (thiếu module knowledge_search)."
    docs = load_all_knowledge()
    results = search(question, docs, top_k=1)
    if not results:
        return "📭 Chưa có tri thức liên quan trong knowledge base. Hãy học thêm video bằng pipeline nhé!"
    best = results[0]
    return f"📚 Dựa trên tri thức đã học (chủ đề: {', '.join(best['topics'])}):\n{best['summary']}"

# ==================== XỬ LÝ LỆNH NGHIỆP VỤ ====================
def process_intent(text):
    """Xử lý các lệnh cũ (dự báo, cảm xúc, tối ưu) và lệnh hệ thống"""
    if not BRAIN_READY:
        return None
    text_lower = text.lower().strip()
    # Lệnh dự báo
    if "dự báo" in text_lower or "du bao" in text_lower:
        nums = re.findall(r'\d+(?:\.\d+)?', text)
        if len(nums) >= 3:
            try:
                budget = float(nums[0]); posts = float(nums[1]); sales = float(nums[2])
                result = brain.predict_sales(budget, posts, sales)
                return f"📊 Dự báo doanh số: {result:,.0f} VND"
            except Exception as e:
                return f"❌ Lỗi: {e}"
        else:
            return "⚠️ Cần 3 số: ngân sách, số bài đăng, doanh số dự kiến"
    # Lệnh cảm xúc
    elif "cảm xúc" in text_lower or "sentiment" in text_lower:
        content = re.sub(r'(cảm xúc|sentiment)\s*', '', text, flags=re.IGNORECASE).strip()
        if content:
            try:
                res = brain.analyze_sentiment(content)
                return f"😊 Cảm xúc: {res['label']} (điểm {res['score']}) | Tích cực: {res['positive_hits']}, Tiêu cực: {res['negative_hits']}"
            except Exception as e:
                return f"❌ Lỗi: {e}"
        else:
            return "Vui lòng nhập văn bản. Ví dụ: 'cảm xúc Sản phẩm tốt'"
    # Lệnh tối ưu campaign
    elif "tối ưu" in text_lower or "toi uu" in text_lower or "campaign" in text_lower:
        nums = re.findall(r'\d+(?:\.\d+)?', text)
        if len(nums) >= 2:
            try:
                budget = float(nums[0]); posts = int(nums[1])
                result = brain.optimize_campaign(budget, posts)
                return f"📈 Kết quả tối ưu: Doanh thu {result['revenue']:,.0f}, Hoa hồng {result['commission']:,.0f}, ROI {result['roi']*100:.1f}%"
            except Exception as e:
                return f"❌ Lỗi: {e}"
        else:
            return "Cần nhập ngân sách và số bài đăng. Ví dụ: 'tối ưu 2000000 15'"
    else:
        return None

# ==================== GIAO DIỆN ĐĂNG NHẬP ====================
class LoginDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Đăng nhập SEN")
        self.geometry("300x150")
        self.resizable(False, False)
        self.result = None
        tk.Label(self, text="Tên đăng nhập:").pack(pady=(20,0))
        self.username = tk.Entry(self)
        self.username.pack()
        tk.Label(self, text="Mật khẩu:").pack(pady=(10,0))
        self.password = tk.Entry(self, show="*")
        self.password.pack()
        tk.Button(self, text="Đăng nhập", command=self.login).pack(pady=15)
        self.username.bind("<Return>", lambda e: self.password.focus())
        self.password.bind("<Return>", lambda e: self.login())
        self.grab_set()
        self.wait_window()

    def login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        user_obj = authenticate_user(user, pwd)
        if user_obj:
            self.result = user_obj
            self.destroy()
        else:
            messagebox.showerror("Lỗi", "Sai tên đăng nhập hoặc mật khẩu")

# ==================== CỬA SỔ CHAT ====================
class ChatWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title(f"{AI_IDENTITY} - Admin Center - {user.username}")
        self.root.geometry("700x500")
        self.root.configure(bg="#2b2b2b")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas",10),
                                                    bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10,5))
        self.chat_area.config(state=tk.DISABLED)

        input_frame = tk.Frame(root, bg="#3c3c3c")
        input_frame.pack(fill=tk.X, padx=10, pady=(0,10))

        self.input_entry = tk.Entry(input_frame, font=("Consolas",10), bg="#2d2d2d", fg="white")
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,5), pady=10)
        self.input_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(input_frame, text="Gửi", command=self.send_message, bg="#007acc", fg="white")
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=10)

        self.append_message("Hệ thống", f"Chào Sếp {user.username}, vai trò {user.role}. {AI_IDENTITY} sẵn sàng.", system=True)

    def append_message(self, sender, text, system=False):
        self.chat_area.config(state=tk.NORMAL)
        if system:
            self.chat_area.insert(tk.END, f"\n🔹 {sender}: {text}\n", "system")
            self.chat_area.tag_config("system", foreground="#888888")
        else:
            self.chat_area.insert(tk.END, f"\n👤 {sender}: {text}\n", "user" if sender == "Sếp Đức" else "sen")
            self.chat_area.tag_config("user", foreground="#4ec9b0")
            self.chat_area.tag_config("sen", foreground="#9cdcfe")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def send_message(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        self.input_entry.delete(0, tk.END)
        self.append_message("Sếp Đức", user_input)

        # Xử lý lệnh bắt đầu bằng !
        if user_input.startswith("!"):
            response = self.handle_command(user_input)
            self.append_message(AI_IDENTITY, response)
            return

        # Xử lý lệnh cũ (dự báo, cảm xúc, ...)
        result = process_intent(user_input)
        if result == "EXIT":
            self.on_closing()
            return
        elif result:
            self.append_message(AI_IDENTITY, result)
            return

        # Chat tự do qua Ollama
        self.append_message(AI_IDENTITY, "[Đang suy nghĩ...]")
        self.root.update()
        response = ask_ollama(user_input)
        # Xóa dòng "[Đang suy nghĩ...]" và thay bằng kết quả
        self.chat_area.config(state=tk.NORMAL)
        last_line_start = self.chat_area.index("end-2l")
        self.chat_area.delete(last_line_start, "end-1l")
        self.chat_area.insert(tk.END, f"\n🤖 {AI_IDENTITY}: {response}\n", "sen")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def handle_command(self, cmd):
        """Xử lý các lệnh mở rộng !optimize, !sandbox, !check_affiliate, !ask"""
        if cmd.startswith("!ask "):
            question = cmd[5:].strip()
            if not question:
                return "❗ Cần nhập câu hỏi. Ví dụ: !ask tình yêu là gì?"
            return ask_with_knowledge(question)
        elif cmd.startswith("!optimize "):
            code = cmd[10:].strip()
            if not code:
                return "❗ Cần cung cấp code để tối ưu. Ví dụ: !optimize print('hello')"
            try:
                versions = brain.quantum_optimize(code)
                if isinstance(versions, list) and len(versions) > 0:
                    response = "✅ Đã tạo 3 phiên bản tối ưu:\n"
                    for v in versions:
                        response += f"  - Ver {v['version']} ({v['type']}):\n{v['code'][:200]}...\n"
                    return response
                else:
                    return f"❌ Lỗi tối ưu: {versions}"
            except Exception as e:
                return f"❌ Lỗi: {e}"
        elif cmd.startswith("!sandbox "):
            code = cmd[9:].strip()
            if not code:
                return "❗ Cần cung cấp code để chạy trong sandbox. Ví dụ: !sandbox print(2+2)"
            try:
                res = brain.safe_execute(code)
                if res.get("success"):
                    return f"✅ Kết quả sandbox:\n{res['output']}"
                else:
                    return f"❌ Sandbox lỗi: {res.get('error')}"
            except Exception as e:
                return f"❌ Lỗi: {e}"
        elif cmd.startswith("!check_affiliate "):
            context = cmd[17:].strip()
            if not context:
                return "❗ Cần nhập nội dung tin nhắn để kiểm tra. Ví dụ: !check_affiliate Tôi muốn mua giày"
            user_id = str(self.user.id) if hasattr(self.user, 'id') else "test_user"
            try:
                allowed = brain.check_affiliate_policy(user_id, context)
                if allowed:
                    return "✅ Có thể gửi link affiliate (đã đủ điều kiện)."
                else:
                    return "❌ Không được gửi link affiliate (chưa đủ điều kiện: cần user hỏi về mua bán hoặc đã gửi trong 24h)."
            except Exception as e:
                return f"❌ Lỗi: {e}"
        else:
            return "❗ Lệnh không hợp lệ. Các lệnh: !ask <câu hỏi>, !optimize <code>, !sandbox <code>, !check_affiliate <message>"

    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát?"):
            self.root.destroy()

# ==================== MAIN ====================
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