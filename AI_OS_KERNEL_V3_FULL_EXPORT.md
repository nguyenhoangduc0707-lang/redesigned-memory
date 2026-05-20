# AI_OS_KERNEL_V3 - Clean Export for NotebookLM
Exported: 2026-05-20 17:30:33

This export includes core code files with sensitive information removed.
## FILE: agents.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: ai_tools.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: ai_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: api_affiliate.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: benchmark.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: campaign_intelligence.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: check_compatibility.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: check_project_health.py

```python
import os
import subprocess
import sys

print("=== KIỂM TRA SỨC KHỎE DỰ ÁN ===")

# 1. Kiểm tra API keys
gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if not gemini_key or gemini_key == "AIzaSyYourActualKeyHere":
    print("[CẢNH BÁO] GEMINI_API_KEY chưa được set hoặc đang dùng key giả")
else:
    print("[OK] GEMINI_API_KEY đã được set")

if not openai_key or openai_key.startswith("sk-"):
    print("[CẢNH BÁO] OPENAI_API_KEY có vẻ không hợp lệ hoặc chưa set")
else:
    print("[OK] OPENAI_API_KEY đã được set")

# 2. Tìm các file Python sử dụng thư viện cũ
print("\n=== CÁC FILE DÙNG THƯ VIỆN DEPRECATED ===")
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "google.generativeai" in content:
                    print(f" - {path} (dùng generativeai cũ)")

# 3. Tìm các file rác phổ biến
print("\n=== FILE RÁC TIỀM NĂNG ===")
trash_extensions = [".pyc", ".log", ".tmp", ".bak", ".swp"]
for ext in trash_extensions:
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(ext):
                print(f" - {os.path.join(root, file)}")

print("\n=== HOÀN THÀNH ===")
```

## FILE: config.py

```python
import os
from dotenv import load_dotenv

# Tải cấu hình từ file .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Lỗi: Không tìm thấy GEMINI_API_KEY trong file .env. Vui lòng kiểm tra lại!")

# Cấu hình chung cho thuật toán nâng cấp
MODEL_NAME = "gemini-1.5-flash"
MAX_OUTPUT_TOKENS = 8192
TEMPERATURE = 0.2  # Giảm xuống một chút để đảm bảo sinh code HTML/CSS chuẩn xác, ít lỗi vặt

```

## FILE: create_user.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: dashboard_api.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: export_to_notebooklm.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: generate_all_html.py

```python
import os
import sys
import time
import google.generativeai as genai
from config import API_KEY, MODEL_NAME, TEMPERATURE, MAX_OUTPUT_TOKENS

# Cấu hình Google GenAI
genai.configure(api_key=API_KEY)

def generate_html_content(prompt_text, retries=3, delay=5):
    """
    Thuật toán nâng cấp: Tự động bắt lỗi API và thử lại nếu gặp sự cố nghẽn mạng
    """
    model = genai.GenerativeModel(MODEL_NAME)
    
    for attempt in range(retries):
        try:
            print(f"-> Đang gửi yêu cầu đến Gemini (Lần thử {attempt + 1}/{retries})...")
            response = model.generate_content(
                prompt_text,
                generation_config={
                    "temperature": TEMPERATURE,
                    "max_output_tokens": MAX_OUTPUT_TOKENS,
                }
            )
            
            if response and response.text:
                # Thuật toán làm sạch dữ liệu: Tự động bóc tách markdown ```html nếu có
                content = response.text.strip()
                if content.startswith("```html"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                return content.strip()
                
        except Exception as e:
            print( f"[Cảnh báo] Gặp lỗi khi gọi API: {e}")
            if attempt < retries - 1:
                print(f"Đang đợi {delay} giây trước khi thử lại...")
                time.sleep(delay)
            else:
                print("[Lỗi] Đã thử hết số lần nhưng không thành công.")
                return None

def main():
    print("=== CHƯƠNG TRÌNH TỰ ĐỘNG SINH CODE HTML NÂNG CẤP ===")
    
    # Giả sử bạn có danh sách các prompt cần sinh ở đây
    prompts = {
        "index.html": "Tạo một trang chủ landing page hiện đại, giao diện tối giản, có thanh điều hướng và responsive đầy đủ bằng HTML và Tailwind CSS.",
        "about.html": "Tạo một trang giới thiệu bản thân (About Me) chuyên nghiệp với bố cục grid, có phần kỹ năng và kinh nghiệm."
    }
    
    for filename, prompt in prompts.items():
        print(f"\n[Xử lý] Đang tiến hành tạo file: {filename}")
        html_code = generate_html_content(prompt)
        
        if html_code:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_code)
                print(f"[Thành công] Đã lưu file sạch tại: {filename}")
            except IOError as e:
                print(f"[Lỗi] Không thể ghi file {filename}: {e}")
        else:
            print(f"[Thất bại] Bỏ qua file {filename} do lỗi sinh nội dung.")

if __name__ == "__main__":
    # Xử lý lỗi hệ thống 'lost sys.stderr' bằng cách đảm bảo luồng chuẩn luôn tồn tại
    if sys.stderr is None:

        
    main()






```

## FILE: init_db.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: notebook_rag.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: notebooklm_analyst.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: notebooklm_client.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: orchestrator.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: policy_checker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: real_time_learning.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: record.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: reporter.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: run_agent_simple.py

```python
# run_agent_simple.py
import subprocess
import sys

def run_campaign_update():
    # Gọi trực tiếp script generate_all_html.py trong cùng môi trường
    result = subprocess.run([sys.executable, "generate_all_html.py"], 
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode == 0:
        print("✅ Cập nhật thành công!")
        print(result.stdout)
    else:
        print("❌ Lỗi khi cập nhật:")
        print(result.stderr)

if __name__ == "__main__":
    run_campaign_update()

```

## FILE: run_agent.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: run_sen_tui_fixed.py

```python
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

```

## FILE: sandbox.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: semantic_validator.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: sen_brain.py

```python
# -*- coding: utf-8 -*-
import sys
import io
import joblib
import numpy as np

class SEN_Brain:
    def __init__(self, model_path='models/sales_prediction_model.pkl'):
        self.model = None
        # Tải model nếu có
        try:
            self.model = joblib.load(model_path)
        except:
            pass

    def check_affiliate_policy(self, user_id, context):
        # Đơn giản: luôn cho phép (hoặc bạn có thể thêm logic)
        return True

    def optimize_code(self, code):
        # Trả về code gốc hoặc thông báo
        return code

    def run_sandbox(self, code):
        # Thực thi code an toàn (tạm thời trả về kết quả)
        try:
            exec_globals = {}
            exec(code, exec_globals)
            return "Code executed successfully"
        except Exception as e:
            return f"Error: {e}"

default_brain = SEN_Brain()

```

## FILE: sen_langchain.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: sen_tui.py

```python
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


```

## FILE: streamlit_app.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: test_brain_full.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: test_brain.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: test_policy.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: test_workers.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: affiliate\accesstrade\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: affiliate\accesstrade\auth.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: affiliate\accesstrade\campaigns.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: affiliate\accesstrade\config.py

```python
# Accesstrade API configuration
API_KEY = "your_api_key_here"
SECRET_KEY = "your_secret_key_here"
BASE_URL = "https://api.accesstrade.vn/v1"

```

## FILE: affiliate\accesstrade\deeplink.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: affiliate\accesstrade\direct_link.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: affiliate\accesstrade\generate_all_html.py

```python
import sys
import os
sys.path.append(os.getcwd())
from affiliate.accesstrade.campaigns import get_campaigns
from affiliate.accesstrade.direct_link import get_direct_link_script

output_dir = "generated_sites"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Dang lay danh sach campaigns...")
campaigns = get_campaigns(approval="successful", limit=50)
print("Tim thay", len(campaigns), "campaigns")

for idx, camp in enumerate(campaigns, 1):
    camp_id = camp['id']
    camp_name = camp['name']
    print(f"[{idx}/{len(campaigns)}] Dang xu ly: {camp_name}")
    try:
        result = get_direct_link_script(camp_id)
        safe_name = "".join(c for c in camp_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        file_path = os.path.join(output_dir, f"{safe_name}_{camp_id}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result['embed_html'])
        print(f"   OK: {file_path}")
    except Exception as e:
        print(f"   LOI: {e}")

print("HOAN TAT.")
```

## FILE: affiliate\accesstrade\main.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: affiliate\accesstrade\reports.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: monitors\error_monitor.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\add_affiliate_tracking.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\audit_api_keys.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\cleanup.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\create_tables.py

```python
# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Báº£ng algorithm_params (quan trá»ng nháº¥t)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            param_name TEXT NOT NULL,
            param_value REAL NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    ''')
    
    # CÃ¡c báº£ng khÃ¡c cáº§n thiáº¿t
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            platform TEXT,
            start_date TEXT,
            end_date TEXT,
            budget REAL,
            goal TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaign_products (
            campaign_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaign_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            predicted_posts INTEGER,
            predicted_likes INTEGER,
            predicted_sales INTEGER,
            predicted_revenue REAL,
            prediction_date TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaign_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            actual_posts INTEGER,
            actual_likes INTEGER,
            actual_sales INTEGER,
            actual_revenue REAL,
            accuracy_percent REAL,
            result_date TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            adjustment_reason TEXT,
            old_params TEXT,
            new_params TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("âœ… All tables created successfully!")

if __name__ == "__main__":
    create_tables()


```

## FILE: scripts\credential_agent.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\devweb_f12_agent.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\init_db_full.py

```python
# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def init_all_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # T?o b?ng algorithm_params (quan tr?ng nh?t, dang thi?u)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            param_name TEXT NOT NULL,
            param_value REAL NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    ''')
    
    # T?o b?ng campaigns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            platform TEXT,
            start_date TEXT,
            end_date TEXT,
            budget REAL,
            goal TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # T?o b?ng campaign_products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_products (
            campaign_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    # T?o b?ng campaign_predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            predicted_posts INTEGER,
            predicted_likes INTEGER,
            predicted_sales INTEGER,
            predicted_revenue REAL,
            prediction_date TIMESTAMP
        )
    ''')
    
    # T?o b?ng campaign_results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            actual_posts INTEGER,
            actual_likes INTEGER,
            actual_sales INTEGER,
            actual_revenue REAL,
            accuracy_percent REAL,
            result_date TIMESTAMP
        )
    ''')
    
    # T?o b?ng algorithm_adjustments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            adjustment_reason TEXT,
            old_params TEXT,
            new_params TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("? All required tables created successfully!")

if __name__ == "__main__":
    init_all_tables()


```

## FILE: scripts\quantize_sklearn_model.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\retrain_model.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: scripts\validate.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: src\affiliate_manager.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\campaign_intelligence.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\cdc_listener.py

```python
# -*- coding: utf-8 -*-
import sqlite3
import time
import threading
from pathlib import Path
from datetime import datetime
import sys
import os

# Đảm bảo thư mục gốc được thêm vào sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.database import get_db
from src.learning.real_time_learning import RealTimeLearner
from src.config import DB_PATH

class CDCListener:
    def __init__(self, db_path=DB_PATH, poll_interval=2):
        self.db_path = db_path
        self.poll_interval = poll_interval
        self._ensure_change_table()
        self.last_id = self._get_max_change_id()
        self.running = False
        self.learner = RealTimeLearner()

    def _ensure_change_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS data_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name TEXT NOT NULL,
                    row_id INTEGER,
                    operation TEXT NOT NULL,
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def _get_max_change_id(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM data_changes")
            row = cur.fetchone()
            return row[0] if row and row[0] else 0

    def _process_changes(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, table_name, row_id, operation FROM data_changes WHERE id > ? ORDER BY id", (self.last_id,))
            changes = cur.fetchall()
            for change_id, table, row_id, op in changes:
                print(f"[CDC] {op} on {table} id={row_id}")
                # Giả sử row_id là campaign_id (cần kiểm tra table)
                if table == 'campaigns' and op in ('INSERT', 'UPDATE'):
                    self.learner.add_campaign_result(row_id)
                self.last_id = change_id

    def start(self):
        self.running = True
        print("[CDC] Listener started")
        while self.running:
            self._process_changes()
            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    listener = CDCListener()
    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()
        print("[CDC] Listener stopped")




```

## FILE: src\config.py

```python
# src/config.py
AI_IDENTITY = "SEN AI - Trợ lý thông minh của bạn"
FOUNDER_INFO = "Được phát triển bởi SEN Team"
DEDICATION = "Dự án AI_OS_KERNEL_V3"
DB_PATH = "ai_os.db"

# Các cấu hình khác nếu cần
OLLAMA_MODEL = "gemma2:2b"

```

## FILE: src\database.py

```python
# -*- coding: utf-8 -*-
import sqlite3
from src.config import DB_PATH

def get_db():
    return sqlite3.connect(DB_PATH)

def get_db_connection():
    return get_db()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS data_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                row_id INTEGER,
                operation TEXT NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("Database ready")

def save_post(product_id, platform, caption, link):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts (product_id, platform_target, caption, link) VALUES (?,?,?,?)",
            (product_id, platform, caption, link),
        )
        conn.commit()

def get_user_by_username(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, role FROM users WHERE username=?", (username,))
        return cur.fetchone()

def add_user(username, password, role="user"):
    from werkzeug.security import generate_password_hash
    with get_db() as conn:
        cur = conn.cursor()
        hash_pw = generate_password_hash(password)
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                (username, hash_pw, role),
            )
            user_id = cur.lastrowid
            cur.execute("INSERT INTO user_stats (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None

```

## FILE: src\devweb_agent.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\key_manager.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\main.py

```python
# -*- coding: utf-8 -*-
import sys, os, tempfile, secrets, uuid
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from src.database import get_db, init_db, save_post
from src.agents import run_all_agents
from src.campaign_intelligence import CampaignIntelligence
from src.user_manager import authenticate_user, get_user_by_id, add_user, list_users
from src.tts_engine import text_to_speech
from src.notebooklm_pro import NotebookLMPro
import requests
from src.affiliate_manager import (
    create_affiliate_link, get_random_ad, reward_user_for_ad, track_click,
    init_affiliate_tables, can_create_link
)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(int(user_id))

# Video processor
try:
    from src.media.video_processor import get_processor
    PROCESSOR_READY = True
    processor = get_processor()
except:
    PROCESSOR_READY = False
    processor = None

ci = CampaignIntelligence()
notebooklm_pro = NotebookLMPro()

def generate_caption(product_name, price, strategy):
    return f"Hot {product_name} chi {price:,}d! Uu dai. #{strategy} #affiliate"

def generate_content_for_all():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, price, url, strategy FROM products")
        products = cur.fetchall()
        platforms = ['tiktok', 'facebook', 'zalo', 'shopee']
        for pid, name, price, url, strategy in products:
            for platform in platforms:
                caption = generate_caption(name, price, strategy)
                save_post(pid, platform, caption, url)
    print("Da sinh noi dung")

def post_to_facebook(message):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT access_token FROM platform_tokens WHERE platform='facebook'")
        row = cur.fetchone()
        token = row[0] if row else os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    if not token:
        return "Khong co token"
    url = "https://graph.facebook.com/v18.0/me/feed"
    resp = requests.post(url, data={'message': message, 'access_token': token})
    return resp.json()

@app.route('/')
def home():
    return redirect(url_for('login') if not current_user.is_authenticated else url_for('dashboard'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        user = authenticate_user(u, p)
        if user:
            login_user(user)
            flash('Dang nhap thanh cong')
            return redirect(url_for('dashboard'))
        flash('Sai tai khoan hoac mat khau')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT platform_target, COUNT(*) FROM posts WHERE status='draft' GROUP BY platform_target")
        counts = {r[0]: r[1] for r in cur.fetchall()}
    return render_template('unified_dashboard.html', counts=counts, role=current_user.role)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Ban khong co quyen')
        return redirect(url_for('dashboard'))
    if request.args.get('format') == 'json':
        users = list_users()
        return jsonify([{'id': u[0], 'username': u[1], 'role': u[2], 'created_at': u[3]} for u in users])
    return render_template('admin_users.html', users=list_users())

@app.route('/admin/add_user', methods=['POST'])
@login_required
def add_user_route():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')
    user_id = add_user(username, password, role)
    if user_id:
        return jsonify({'success': True, 'user_id': user_id})
    return jsonify({'success': False, 'error': 'Username exists'}), 400

@app.route('/admin/tokens', methods=['GET'])
@login_required
def admin_tokens():
    if current_user.role != 'admin':
        flash('Ban khong co quyen')
        return redirect(url_for('dashboard'))
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT platform, access_token, api_key, updated_at FROM platform_tokens")
        tokens = cur.fetchall()
    return render_template('admin_tokens.html', tokens=tokens)

@app.route('/admin/update_token', methods=['POST'])
@login_required
def update_token():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    platform = data.get('platform')
    access_token = data.get('access_token', '')
    api_key = data.get('api_key', '')
    api_secret = data.get('api_secret', '')
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''UPDATE platform_tokens SET access_token=?, api_key=?, api_secret=?, updated_at=CURRENT_TIMESTAMP WHERE platform=?''',
                    (access_token, api_key, api_secret, platform))
        conn.commit()
    return jsonify({'success': True})

@app.route('/license')
def license_page():
    return render_template('license.html')

@app.route('/sen_license')
def sen_license():
    return render_template('sen_license.html')

@app.route('/chat')
@login_required
def chat_page():
    return render_template('chat.html')

@app.route('/notebooklm')
@login_required
def notebooklm_page():
    return render_template('notebooklm.html')

@app.route('/api/notebooklm/status')
@login_required
def notebooklm_status():
    return jsonify(notebooklm_pro.status())

@app.route('/api/notebooklm/ask', methods=['POST'])
@login_required
def notebooklm_ask():
    data = request.get_json() or {}
    question = data.get('question', '')
    timeout = int(data.get('timeout', 120))
    return jsonify(notebooklm_pro.ask(question, timeout=timeout))

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json()
    msg = data.get('message', '')
    if "notebook" in msg.lower():
        result = notebooklm_pro.ask(msg)
        response = result.get('answer') or result.get('error') or "NotebookLM khong co cau tra loi."
    elif "chay pipeline" in msg.lower():
        response = "Da chay pipeline thanh cong."
        run_all_agents()
    elif "thong ke" in msg.lower():
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM campaigns")
            count = cur.fetchone()[0]
            response = f"He thong co {count} chien dich."
    else:
        response = f"Ban noi: {msg}. Toi la tro ly AI."
    audio_file = text_to_speech(response, lang='vi')
    return jsonify({'text': response, 'audio_file': audio_file})

@app.route('/api/health')
def api_health():
    return jsonify({"status": "healthy"})

@app.route('/media')
@login_required
def media_page():
    return render_template('media.html')

@app.route('/review_station')
@login_required
def review_station():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, product_id, platform_target, caption, link, status FROM posts ORDER BY id DESC LIMIT 100")
        posts = cur.fetchall()
    return render_template('review_station.html', posts=posts)

# Campaign routes
@app.route('/campaigns')
@login_required
def campaigns_page():
    with get_db() as conn:
        cur = conn.cursor()
        if current_user.role == 'admin':
            cur.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        else:
            cur.execute("SELECT * FROM campaigns WHERE user_id=? ORDER BY created_at DESC", (current_user.id,))
        campaigns = cur.fetchall()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/new_campaign', methods=['GET','POST'])
@login_required
def new_campaign():
    if request.method == 'POST':
        name = request.form['name']
        platform = request.form['platform']
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO campaigns (user_id, name, platform, status) VALUES (?,?,?,?)",
                        (current_user.id, name, platform, 'active'))
            conn.commit()
            cur.execute("UPDATE user_stats SET campaign_count = campaign_count + 1 WHERE user_id=?", (current_user.id,))
            conn.commit()
        flash('Da tao chien dich!')
        return redirect(url_for('campaigns_page'))
    return render_template('new_campaign.html')

@app.route('/pipeline')
@login_required
def pipeline_page():
    return render_template('pipeline.html')

@app.route('/api/pipeline_logs')
@login_required
def api_pipeline_logs():
    with get_db() as conn:
        cur = conn.cursor()
        if current_user.role == 'admin':
            cur.execute("SELECT * FROM pipeline_logs ORDER BY created_at DESC LIMIT 100")
        else:
            cur.execute('''SELECT l.* FROM pipeline_logs l JOIN campaigns c ON l.campaign_id=c.id WHERE c.user_id=? ORDER BY l.created_at DESC LIMIT 100''', (current_user.id,))
        logs = cur.fetchall()
    result = [{'id':r[0],'campaign_id':r[1],'worker_name':r[2],'action':r[3],'status':r[4],'message':r[5],'created_at':r[6]} for r in logs]
    return jsonify(result)

@app.route('/api/campaigns')
@login_required
def api_campaigns():
    with get_db() as conn:
        cur = conn.cursor()
        if current_user.role == 'admin':
            cur.execute("SELECT id,name,platform,status,created_at FROM campaigns ORDER BY created_at DESC")
        else:
            cur.execute("SELECT id,name,platform,status,created_at FROM campaigns WHERE user_id=?", (current_user.id,))
        rows = cur.fetchall()
    return jsonify([{'id':r[0],'name':r[1],'platform':r[2],'status':r[3],'created_at':r[4]} for r in rows])

@app.route('/api/run_worker', methods=['POST'])
@login_required
def run_worker():
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    worker_name = data.get('worker_name')
    with get_db() as conn:
        conn.execute("INSERT INTO pipeline_logs (campaign_id, worker_name, action, status, message) VALUES (?,?,?,?,?)",
                     (campaign_id, worker_name, 'run', 'started', f'Worker {worker_name} started by {current_user.username}'))
        conn.commit()
    return jsonify({'status': 'started', 'message': f'Worker {worker_name} dang chay (gia lap)'})

@app.route('/api/me')
@login_required
def api_me():
    return jsonify({'id':current_user.id, 'username':current_user.username, 'role':current_user.role})

# Affiliate routes
@app.route('/my_links')
@login_required
def my_links():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT link_code, target_url, used_count, created_at FROM affiliate_links WHERE user_id=?", (current_user.id,))
        links = cur.fetchall()
    return render_template('my_links.html', links=links, role=current_user.role, daily_left=can_create_link(current_user.id))

@app.route('/api/create_link', methods=['POST'])
@login_required
def api_create_link():
    data = request.get_json()
    target_url = data.get('target_url')
    if not target_url:
        return jsonify({"error": "Missing target_url"}), 400
    code, err = create_affiliate_link(current_user.id, target_url)
    if err:
        return jsonify({"error": err}), 403
    return jsonify({"link_code": code, "link": f"http://localhost:5000/go/{code}"})

@app.route('/api/need_ad', methods=['GET'])
@login_required
def api_need_ad():
    if can_create_link(current_user.id):
        return jsonify({"can_create": True})
    ad = get_random_ad()
    if not ad:
        return jsonify({"can_create": False, "error": "No ad"})
    return jsonify({"can_create": False, "ad": ad})

@app.route('/api/watch_ad', methods=['POST'])
@login_required
def api_watch_ad():
    data = request.get_json()
    ad_id = data.get('ad_id')
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ads WHERE id=?", (ad_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Ad not found"}), 404
        ad = {"id":row[0],"title":row[1],"reward_type":row[4],"reward_value":row[5]}
        msg = reward_user_for_ad(current_user.id, ad)
        return jsonify({"success": True, "message": msg, "new_quota": can_create_link(current_user.id)})

@app.route('/go/<link_code>')
def redirect_link(link_code):
    ip = request.remote_addr
    track_click(link_code, ip)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT target_url FROM affiliate_links WHERE link_code=?", (link_code,))
        row = cur.fetchone()
        if not row:
            return "Link not found", 404
        return redirect(row[0])

# ========== WEBHOOK COMMISSION ==========
@app.route('/webhook/commission', methods=['POST'])
def webhook_commission():
    """
    Nhận dữ liệu bán hàng từ sàn TMĐT (Shopee, TikTok, ...)
    Dữ liệu mẫu: {"user_id": 1, "amount": 100000, "order_id": "123", "product": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400
    user_id = data.get('user_id')
    amount = data.get('amount')
    if not user_id or not amount:
        return jsonify({"error": "Missing user_id or amount"}), 400
    # Ghi nhận hoa hồng (40% user, 30% referrer, 30% admin)
    # Sử dụng hàm record_commission từ affiliate_manager
    try:
        from src.affiliate_manager import record_commission
        record_commission(amount, user_id, f"Order {data.get('order_id', 'unknown')}")
        return jsonify({"status": "success", "message": "Commission recorded"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/create_video_demo', methods=['POST'])
@login_required
def api_create_video_demo():
    """
    Demo: nhận danh sách đường dẫn ảnh (hoặc upload file) và text, tạo video.
    Ảnh có thể gửi dưới dạng list URLs hoặc upload files.
    """
    data = request.get_json()
    image_urls = data.get('image_urls', [])
    text = data.get('text', '')
    output_filename = f"output_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join('static', 'videos', output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Tạm thời giả lập: tạo video mẫu
    # Thực tế cần tải ảnh từ URL, lưu tạm, rồi gọi processor
    # Ở đây tôi chỉ tạo video trắng để demo
    from moviepy.editor import ColorClip, AudioFileClip
    from gtts import gTTS
    # Tạo audio từ text
    audio_path = f"audio_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text, lang='vi')
    tts.save(audio_path)
    # Tạo video trắng 5 giây
    clip = ColorClip(size=(1280,720), color=(255,255,255), duration=5)
    audio = AudioFileClip(audio_path)
    clip = clip.set_audio(audio)
    clip.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
    os.remove(audio_path)
    return jsonify({"video_url": f"/static/videos/{output_filename}"})

# ========== CREATE VIDEO ROUTE ==========
@app.route('/create_video', methods=['GET', 'POST'])
@login_required
def create_video():
    if request.method == 'POST':
        caption = request.form.get('caption', '')
        files = request.files.getlist('images')
        if not files or len(files) == 0:
            flash('Vui lòng upload ít nhất 1 ảnh')
            return redirect(url_for('create_video'))
        
        from werkzeug.utils import secure_filename
        import uuid
        image_paths = []
        for file in files:
            if file.filename:
                filename = secure_filename(file.filename)
                unique = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join('uploads', unique)
                os.makedirs('uploads', exist_ok=True)
                file.save(filepath)
                image_paths.append(filepath)
        
        audio_path = None
        if caption.strip():
            from src.tts_engine import text_to_speech
            audio_path = text_to_speech(caption, lang='vi', output_dir='audio')
        
        from src.media.video_processor import get_processor
        processor = get_processor()
        video_filename = f"video_{uuid.uuid4().hex}.mp4"
        video_output = os.path.join('static', 'videos', video_filename)
        os.makedirs('static/videos', exist_ok=True)
        
        processor.create_video_from_images(image_paths, audio_path, video_output, duration_per_image=3)
        
        for p in image_paths:
            try: os.remove(p)
            except: pass
        
        return render_template('video_result.html', video_url=f'/static/videos/{video_filename}', caption=caption)
    
    return render_template('create_video.html')

@app.route('/api/post_video_to_fb', methods=['POST'])
@login_required
def post_video_to_fb():
    data = request.get_json()
    video_path = data.get('video_url').replace('/static/', 'static/')
    caption = data.get('caption', '')
    from worker.executor import run_worker
    result = run_worker('facebook', None, caption, video_path, 'video')
    return jsonify({"message": "Đã gửi yêu cầu đăng bài", "result": result})

if __name__ == '__main__':
    init_db()
    init_affiliate_tables()
    if '--run-pipeline' in sys.argv:
        run_all_agents()
        generate_content_for_all()
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)

```

## FILE: src\notebooklm_pro.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\orchestrator.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\security.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\tts_engine.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\user_manager.py

```python
import sqlite3

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import get_db


class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


def get_db_connection():
    return get_db()


def add_user(username, password, role="user"):
    with get_db_connection() as conn:
        cur = conn.cursor()
        hash_pw = generate_password_hash(password)
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                (username, hash_pw, role),
            )
            user_id = cur.lastrowid
            cur.execute("INSERT INTO user_stats (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None


def authenticate_user(username, password):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, role FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row[2], password):
            return User(row[0], row[1], row[3])
    return None


def get_user_by_id(user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if row:
            return User(row[0], row[1], row[2])
    return None


def list_users():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, role, created_at FROM users")
        return cur.fetchall()

```

## FILE: src\agents\__init__.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\agents\crm_bot.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\crawlers\crawl_competitors.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import sqlite3
import requests
import time
import json

def get_shopee_similar(product_name):
    url = f"https://shopee.vn/api/v4/search/search_items?keyword={product_name}&limit=5"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get('items', [])
            result = []
            for item in items:
                name = item.get('name', '')
                price = item.get('price', 0) / 100000
                sold = item.get('historical_sold', 0)
                result.append({
                    'name': name[:50],
                    'price': int(price),
                    'sales': sold,
                    'platform': 'shopee'
                })
            return result
    except Exception as e:
        print(f"Error: {e}")
    return []

def update_competitors(product_id, product_name):
    competitors = get_shopee_similar(product_name)
    conn = sqlite3.connect('affiliate.db')
    cur = conn.cursor()
    for comp in competitors:
        cur.execute('''
            INSERT INTO competitors (product_id, competitor_name, price, sales, platform)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, comp['name'], comp['price'], comp['sales'], comp['platform']))
    conn.commit()
    conn.close()
    print(f"Added {len(competitors)} competitors for product {product_id}")

# Láº¥y danh sÃ¡ch sáº£n pháº©m tá»« database
conn = sqlite3.connect('affiliate.db')
cur = conn.cursor()
cur.execute("SELECT id, name FROM products LIMIT 10")
rows = cur.fetchall()
conn.close()

for pid, pname in rows:
    update_competitors(pid, pname)
    time.sleep(1)




```

## FILE: src\dev\SEN_AST_Analyzer.py

```python
# [Empty or unreadable file]
```

## FILE: src\dev\SEN_Config_Quantum.py

```python
# [Empty or unreadable file]
```

## FILE: src\dev\SEN_Dev_Orchestrator.py

```python
# [Empty or unreadable file]
```

## FILE: src\dev\SEN_Quantum_Planner.py

```python
# [Empty or unreadable file]
```

## FILE: src\dev\SEN_Quantum_Simulator.py

```python
# [Empty or unreadable file]
```

## FILE: src\dev\SEN_Skills_Versioned.py

```python
# [Empty or unreadable file]
```

## FILE: src\dev\SEN_Validator.py

```python
# [Empty or unreadable file]
```

## FILE: src\execution\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: src\execution\sandbox.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\learning\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: src\learning\real_time_learning.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import joblib
import pandas as pd
import numpy as np
from src.database import get_db
from collections import deque
import datetime
import subprocess
import os

class RealTimeLearner:
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.recent_data = deque(maxlen=max_history)
        self.model = None
        self.load_model()
    
    def load_model(self):
        try:
            if os.path.exists('models/sales_prediction_model.pkl'):
                self.model = joblib.load('models/sales_prediction_model.pkl')
                print("? Real-time learner loaded")
            else:
                print("?? No model found, will collect data first")
        except Exception as e:
            print(f"?? Cannot load model: {e}")
    
    def add_campaign_result(self, campaign_id):
         # -*- coding: utf-8 -*-
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.budget, c.platform, c.goal,
                       cr.actual_posts, cr.actual_sales, cr.actual_revenue
                FROM campaigns c
                LEFT JOIN campaign_results cr ON c.id = cr.campaign_id
                WHERE c.id = ? AND c.status = 'completed'
            """, (campaign_id,))
            row = cur.fetchone()
            
            if row:
                self.recent_data.append({
                    'timestamp': datetime.datetime.now(),
                    'budget': row[0],
                    'platform': row[1],
                    'goal': row[2],
                    'actual_posts': row[3],
                    'actual_sales': row[4],
                    'actual_revenue': row[5]
                })
                print(f"? Added campaign {campaign_id} to learning queue")
                
                if len(self.recent_data) >= 10:
                    self.auto_retrain()
    
    def auto_retrain(self):
        """T? d?ng retrain model v?i d? li?u m?i"""
        print("?? Auto-retraining with new data...")
        try:
            subprocess.run(["python", "retrain_model.py"], capture_output=True)
            self.load_model()
        except Exception as e:
            print(f"?? Auto-retrain failed: {e}")
    
    def predict_sales(self, budget, platform, goal):
        """D? do�n doanh số"""
        if self.model is None:
            return {"error": "Model not ready", "predicted_sales": 0}
        
        try:
            # M� h�a platform v� goal
            platform_map = {'facebook':0, 'tiktok':1, 'zalo':2, 'shopee':3, 'lazada':4}
            goal_map = {'sales':0, 'traffic':1, 'awareness':2}
            
            platform_encoded = platform_map.get(platform, 0)
            goal_encoded = goal_map.get(goal, 0)
            
            features = [[budget, platform_encoded, goal_encoded]]
            predicted_sales = self.model.predict(features)[0]
            
            return {
                "predicted_sales": int(predicted_sales),
                "confidence": min(100, len(self.recent_data) * 5),
                "samples_used": len(self.recent_data)
            }
        except Exception as e:
            return {"error": str(e), "predicted_sales": 0}

# Kh?i t?o global instance
learner = RealTimeLearner()

if __name__ == "__main__":
    print("Real-time learning system ready")
    print(f"Collected samples: {len(learner.recent_data)}")



```

## FILE: src\learning\sentiment_analyzer.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\learning\trend_detection.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from src.database import get_db
from datetime import datetime, timedelta

class TrendDetector:
    def __init__(self):
        self.trends = {}
    
    def analyze_hot_products(self, days=30):
        """Phân lo?i s?n ph?m hot"""
        with get_db() as conn:
            query = f"""
            SELECT 
                p.id,
                p.name,
                p.price,
                p.strategy,
                COUNT(po.id) as post_count,
                SUM(CASE WHEN po.status='published' THEN 1 ELSE 0 END) as published_count
            FROM products p
            LEFT JOIN posts po ON p.id = po.product_id
            GROUP BY p.id
            ORDER BY published_count DESC
            LIMIT 10
            """
            df = pd.read_sql_query(query, conn)
        
        if df.empty:
            return []
        
        hot_products = []
        for _, row in df.iterrows():
            if row['published_count'] > 5:
                level = "??????"
            elif row['published_count'] > 2:
                level = "????"
            elif row['published_count'] > 0:
                level = "??"
            else:
                level = "?"
            
            hot_products.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'strategy': row['strategy'],
                'hot_level': level,
                'posts': row['post_count'],
                'published': row['published_count']
            })
        
        return hot_products
    
    def detect_platform_trends(self):
        """Phát hi?n xu hu?ng n?n t?ng"""
        with get_db() as conn:
            query = """
            SELECT 
                platform_target,
                COUNT(*) as total_posts,
                SUM(CASE WHEN status='published' THEN 1 ELSE 0 END) as published
            FROM posts
            GROUP BY platform_target
            """
            df = pd.read_sql_query(query, conn)
        
        if df.empty:
            return []
        
        total = df['total_posts'].sum()
        trends = []
        for _, row in df.iterrows():
            trends.append({
                'platform': row['platform_target'],
                'total_posts': row['total_posts'],
                'percentage': round(row['total_posts'] / total * 100, 1) if total > 0 else 0,
                'published_rate': round(row['published'] / row['total_posts'] * 100, 1) if row['total_posts'] > 0 else 0
            })
        
        return sorted(trends, key=lambda x: x['percentage'], reverse=True)
    
    def get_recommendations(self):
        """Ð? xu?t chi?n lu?c"""
        hot_products = self.analyze_hot_products()
        platform_trends = self.detect_platform_trends()
        
        recommendations = []
        
        if hot_products and hot_products[0]['hot_level'] != "?":
            recommendations.append({
                'type': 'product',
                'title': '?? S?N PH?M HOT',
                'content': f"Nên uu tiên {hot_products[0]['name']} - dã có {hot_products[0]['published']} bài dang thành công"
            })
        
        if platform_trends and platform_trends[0]['percentage'] > 30:
            recommendations.append({
                'type': 'platform',
                'title': '?? XU HU?NG N?N T?NG',
                'content': f"{platform_trends[0]['platform']} dang d?n d?u v?i {platform_trends[0]['percentage']}% bài dang"
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'info',
                'title': '?? G?I Ý',
                'content': 'T?o thêm chi?n d?ch d? có d? li?u phân tích xu hu?ng'
            })
        
        return recommendations

detector = TrendDetector()

if __name__ == "__main__":
    print("=" * 50)
    print("?? TREND DETECTION SYSTEM")
    print("=" * 50)
    
    hot = detector.analyze_hot_products()
    print(f"\n?? Hot products: {len(hot)}")
    for p in hot[:3]:
        print(f"   {p['hot_level']} {p['name']}: {p['published']} posts")
    
    trends = detector.detect_platform_trends()
    print(f"\n?? Platform trends:")
    for t in trends:
        print(f"   {t['platform']}: {t['percentage']}%")
    
    recs = detector.get_recommendations()
    print(f"\n?? Recommendations:")
    for r in recs:
        print(f"   {r['title']}: {r['content']}")




```

## FILE: src\media\image_gen.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\media\post_process.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\media\video_analyzer.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\media\video_processor.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\ml\algo_simulator.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\ml\check_model.py

```python
# -*- coding: utf-8 -*-
import sys
import os
# Thêm đường dẫn thư mục gốc (chứa src)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import joblib
import pandas as pd
from src.database import get_db
...

print("=" * 60)
print("?? KI?M TRA SALES PREDICTION MODEL")
print("=" * 60)

# 1. Ki?m tra file model
model_path = "models/sales_prediction_model.pkl"
if os.path.exists(model_path):
    print(f"? Model file exists: {model_path}")
    size = os.path.getsize(model_path) / 1024
    print(f"   Size: {size:.2f} KB")
else:
    print(f"? Model file not found: {model_path}")
    print("   C?n train model m?i!")

# 2. Load model và ki?m tra
try:
    model = joblib.load(model_path)
    print(f"\n? Model loaded successfully")
    print(f"   Type: {type(model).__name__}")
except Exception as e:
    print(f"? Cannot load model: {e}")

# 3. Ki?m tra d? li?u trong database
print("\n?? KI?M TRA D? LI?U TRAINING")
with get_db() as conn:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM campaigns")
    campaign_count = cur.fetchone()[0]
    print(f"   Campaigns: {campaign_count}")
    
    cur.execute("""
        SELECT COUNT(*) FROM campaigns 
        WHERE status='completed' AND budget IS NOT NULL
    """)
    completed = cur.fetchone()[0]
    print(f"   Completed campaigns: {completed}")
    
    if completed < 10:
        print(f"   ?? Not enough data ({completed}/10 needed)")

print("\n" + "=" * 60)




```

## FILE: src\ml\quantize_model.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\ml\train_prediction_model.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

conn = sqlite3.connect('affiliate.db')
query = '''
SELECT c.budget, c.platform, cp.predicted_posts, cp.predicted_sales, cr.actual_sales
FROM campaigns c
JOIN campaign_predictions cp ON c.id = cp.campaign_id
JOIN campaign_results cr ON c.id = cr.campaign_id
WHERE c.status = 'completed'
'''
df = pd.read_sql_query(query, conn)
df = pd.get_dummies(df, columns=['platform'])
X = df.drop('actual_sales', axis=1)
y = df['actual_sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
joblib.dump(model, 'sales_prediction_model.pkl')
print('Model trained and saved.')




```

## FILE: src\quantum\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: src\quantum\planner.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\quantum\semantic_validator.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\security\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: src\security\firewall.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\security\policy_checker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: src\training\auto_train_campaigns.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import sqlite3
import random
import datetime
import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

DB_PATH = 'affiliate.db'

def get_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products LIMIT 5")  # Chá»n 5 sáº£n pháº©m Ä‘áº§u
    products = cur.fetchall()
    conn.close()
    return products

def create_campaign(name, platform, budget, goal, product_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    start = datetime.date.today()
    end = start + datetime.timedelta(days=7)
    cur.execute("""
        INSERT INTO campaigns (name, platform, start_date, end_date, budget, goal, status)
        VALUES (?,?,?,?,?,?,'running')
    """, (name, platform, start, end, budget, goal))
    camp_id = cur.lastrowid
    cur.execute("INSERT INTO campaign_products (campaign_id, product_id) VALUES (?,?)", (camp_id, product_id))
    conn.commit()
    conn.close()
    return camp_id

def predict_campaign(camp_id):
    # Gá»i hÃ m dá»± Ä‘oÃ¡n trong campaign_intelligence (cáº§n import)
    from src.campaign_intelligence import CampaignIntelligence
    ci = CampaignIntelligence()
    return ci.predict_campaign(camp_id)

def evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue):
    from src.campaign_intelligence import CampaignIntelligence
    ci = CampaignIntelligence()
    return ci.evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue)

def simulate_results(predicted_sales):
    """MÃ´ phá»ng káº¿t quáº£ thá»±c táº¿ xoay quanh dá»± Ä‘oÃ¡n vá»›i sai sá»‘ ngáº«u nhiÃªn"""
    actual_sales = max(0, int(predicted_sales * random.uniform(0.5, 1.5)))
    actual_revenue = actual_sales * random.randint(50000, 200000)
    actual_posts = max(1, int(actual_sales * random.uniform(2, 5)))
    actual_likes = actual_posts * random.randint(20, 200)
    return actual_posts, actual_likes, actual_sales, actual_revenue

def main():
    products = get_products()
    if not products:
        print("KhÃ´ng cÃ³ sáº£n pháº©m. HÃ£y cháº¡y main.py --run-pipeline trÆ°á»›c.")
        return

    platforms = ['facebook', 'tiktok', 'shopee', 'lazada']
    budgets = [50000, 100000, 200000, 500000]
    goals = ['engagement', 'sales', 'reach']

    # Táº¡o 30 chiáº¿n dá»‹ch má»›i
    for i in range(30):
        product = random.choice(products)
        product_id, product_name, product_price = product
        platform = random.choice(platforms)
        budget = random.choice(budgets)
        goal = random.choice(goals)
        name = f"AutoCampaign_{i+1}_{platform}_{int(time.time())}"
        camp_id = create_campaign(name, platform, budget, goal, product_id)
        print(f"ÄÃ£ táº¡o campaign {camp_id}: {name}")

        # Dá»± Ä‘oÃ¡n
        pred = predict_campaign(camp_id)
        if not pred:
            print(f"  Dá»± Ä‘oÃ¡n tháº¥t báº¡i cho campaign {camp_id}")
            continue
        predicted_sales = pred.get('predicted_sales', 1)
        print(f"  Dá»± Ä‘oÃ¡n: {predicted_sales} sales")

        # MÃ´ phá»ng káº¿t quáº£ thá»±c táº¿
        actual_posts, actual_likes, actual_sales, actual_revenue = simulate_results(predicted_sales)
        print(f"  MÃ´ phá»ng: {actual_sales} sales (posts={actual_posts}, likes={actual_likes}, rev={actual_revenue})")

        # ÄÃ¡nh giÃ¡ vÃ  tá»‘i Æ°u
        result = evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue)
        acc = result.get('accuracy_percent', 0)
        print(f"  Äá»™ chÃ­nh xÃ¡c: {acc:.2f}% - {'ÄÃ£ tá»‘i Æ°u' if acc < 90 else 'Táº¡m á»•n'}")

        # Chá» má»™t chÃºt Ä‘á»ƒ trÃ¡nh quÃ¡ táº£i database
        time.sleep(0.5)

    print("\n=== HOÃ€N Táº¤T ===")
    print("ÄÃ£ táº¡o vÃ  Ä‘Ã¡nh giÃ¡ 30 chiáº¿n dá»‹ch. Thuáº­t toÃ¡n Ä‘Ã£ Ä‘Æ°á»£c tá»‘i Æ°u liÃªn tá»¥c.")
    print("Báº¡n cÃ³ thá»ƒ cháº¡y láº¡i script nÃ y nhiá»u láº§n Ä‘á»ƒ tÄƒng Ä‘á»™ chÃ­nh xÃ¡c.")

if __name__ == "__main__":
    main()




```

## FILE: src\training\generate_sample_campaign_data.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import sqlite3
import random
import datetime

conn = sqlite3.connect('affiliate.db')
cur = conn.cursor()
platforms = ['facebook','tiktok','shopee','lazada']
for i in range(10):
    name = f"Test Campaign {i+1}"
    platform = random.choice(platforms)
    start = datetime.date.today() - datetime.timedelta(days=random.randint(1,30))
    end = start + datetime.timedelta(days=7)
    budget = random.randint(50000,500000)
    goal = random.choice(['engagement','sales','reach'])
    cur.execute("INSERT INTO campaigns (name, platform, start_date, end_date, budget, goal, status) VALUES (?,?,?,?,?,?,'completed')",
                (name, platform, start, end, budget, goal))
    camp_id = cur.lastrowid
    predicted_posts = random.randint(5,20)
    predicted_likes = predicted_posts * random.randint(50,200)
    predicted_sales = random.randint(1,10)
    predicted_revenue = predicted_sales * random.randint(50000,200000)
    cur.execute("INSERT INTO campaign_predictions (campaign_id, predicted_posts, predicted_likes, predicted_sales, predicted_revenue, prediction_date) VALUES (?,?,?,?,?,?)",
                (camp_id, predicted_posts, predicted_likes, predicted_sales, predicted_revenue, datetime.datetime.now()))
    actual_posts = int(predicted_posts * random.uniform(0.7,1.3))
    actual_likes = int(predicted_likes * random.uniform(0.6,1.4))
    actual_sales = int(predicted_sales * random.uniform(0.5,1.5))
    actual_revenue = predicted_revenue * random.uniform(0.5,1.5)
    accuracy = random.uniform(50,95)
    cur.execute("INSERT INTO campaign_results (campaign_id, actual_posts, actual_likes, actual_sales, actual_revenue, accuracy_percent, result_date) VALUES (?,?,?,?,?,?,?)",
                (camp_id, actual_posts, actual_likes, actual_sales, actual_revenue, accuracy, datetime.datetime.now()))
conn.commit()
conn.close()
print("Created 10 sample campaigns")




```

## FILE: src\voice\voice_commander.py

```python
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import speech_recognition as sr
import pyttsx3
from agentscope.agents import DialogAgent, UserAgent
from agentscope.msgs import Msg

# ThÃªm Ä‘Æ°á»ng dáº«n Ä‘á»ƒ import module cá»§a báº¡n
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import get_db
from src.agents import run_all_agents
from src.learning.real_time_learning import RealTimeLearner

class AIOSVoiceCommander:
    """Voice Agent Ä‘iá»u khiá»ƒn toÃ n bá»™ AI_OS_KERNEL_V3"""
    
    def __init__(self):
        # Khá»Ÿi táº¡o speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Khá»Ÿi táº¡o text-to-speech
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 170)
        self.tts.setProperty('volume', 0.9)
        
        # Khá»Ÿi táº¡o cÃ¡c thÃ nh pháº§n core
        self.learner = RealTimeLearner()
        
        # AgentScope agent
        self.agent = DialogAgent(name="AIOS_Commander", sys_prompt=self._get_system_prompt())
    
    def _get_system_prompt(self):
        return """Báº¡n lÃ  trá»£ lÃ½ Ä‘iá»u khiá»ƒn há»‡ thá»‘ng AI_OS_KERNEL_V3.
        Báº¡n cÃ³ thá»ƒ thá»±c hiá»‡n cÃ¡c lá»‡nh: cháº¡y pipeline, huáº¥n luyá»‡n model, 
        crawl dá»¯ liá»‡u, xem thá»‘ng kÃª chiáº¿n dá»‹ch. HÃ£y pháº£n há»“i ngáº¯n gá»n."""
    
    def speak(self, text):
        """PhÃ¡t Ã¢m thanh pháº£n há»“i"""
        print(f"[AIOS] {text}")
        self.tts.say(text)
        self.tts.runAndWait()
    
    def listen(self):
        """Láº¯ng nghe vÃ  nháº­n diá»‡n giá»ng nÃ³i"""
        with self.microphone as source:
            print("ðŸŽ¤ Äang nghe...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        
        try:
            command = self.recognizer.recognize_google(audio, language="vi-VN")
            print(f"ðŸ“ Nháº­n lá»‡nh: {command}")
            return command.lower()
        except sr.UnknownValueError:
            self.speak("Xin lá»—i, tÃ´i khÃ´ng nghe rÃµ.")
            return None
        except sr.RequestError:
            self.speak("Lá»—i káº¿t ná»‘i dá»‹ch vá»¥ nháº­n diá»‡n.")
            return None
    
    def execute_command(self, command):
        """Thá»±c thi lá»‡nh tá»« giá»ng nÃ³i"""
        if not command:
            return
        
        # Äiá»u khiá»ƒn pipeline
        if "cháº¡y pipeline" in command or "run pipeline" in command:
            self.speak("Äang cháº¡y pipeline...")
            run_all_agents()
            self.speak("Pipeline hoÃ n táº¥t.")
        
        # Huáº¥n luyá»‡n model
        elif "huáº¥n luyá»‡n" in command or "train" in command:
            self.speak("Äang huáº¥n luyá»‡n model dá»± Ä‘oÃ¡n...")
            subprocess.run(["python", "src/ml/train_prediction_model.py"])
            self.speak("Huáº¥n luyá»‡n hoÃ n táº¥t.")
        
        # Crawl dá»¯ liá»‡u
        elif "crawl" in command or "thu tháº­p" in command:
            self.speak("Äang crawl dá»¯ liá»‡u Ä‘á»‘i thá»§...")
            subprocess.run(["python", "src/crawlers/crawl_competitors.py"])
            self.speak("Crawl hoÃ n táº¥t.")
        
        # Xem thá»‘ng kÃª
        elif "thá»‘ng kÃª" in command or "campaign" in command:
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM campaigns")
                count = cur.fetchone()[0]
                self.speak(f"Há»‡ thá»‘ng cÃ³ {count} chiáº¿n dá»‹ch.")
        
        # Khá»Ÿi Ä‘á»™ng web
        elif "web" in command or "dashboard" in command:
            self.speak("Äang khá»Ÿi Ä‘á»™ng web dashboard...")
            subprocess.Popen([sys.executable, "-m", "src.main"])
            self.speak("Dashboard Ä‘Ã£ sáºµn sÃ ng táº¡i cá»•ng 5000.")
        
        # Dá»«ng há»‡ thá»‘ng
        elif "táº¡m dá»«ng" in command or "pause" in command:
            self.speak("Táº¡m dá»«ng há»‡ thá»‘ng.")
            # ThÃªm logic pause
        
        # Lá»‡nh khÃ´ng xÃ¡c Ä‘á»‹nh
        else:
            self.speak("Lá»‡nh khÃ´ng Ä‘Æ°á»£c há»— trá»£. Vui lÃ²ng thá»­ láº¡i.")
    
    def run(self):
        """VÃ²ng láº·p chÃ­nh cá»§a Voice Agent"""
        self.speak("Xin chÃ o! AIOS Voice Commander Ä‘Ã£ sáºµn sÃ ng.")
        self.speak("HÃ£y nÃ³i lá»‡nh cá»§a báº¡n.")
        
        while True:
            command = self.listen()
            if command:
                if "thoÃ¡t" in command or "exit" in command or "táº¡m biá»‡t" in command:
                    self.speak("Táº¡m biá»‡t!")
                    break
                self.execute_command(command)

if __name__ == "__main__":
    commander = AIOSVoiceCommander()
    commander.run()


```

## FILE: tests\test_database.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: tests\test_devweb_agent.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: tests\test_key_manager.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: tests\test_notebooklm_pro.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: tests\test_quick_full_build.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: utils\logger.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\amazon_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\base_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\executor.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\facebook_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\fb_executor.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\lazada_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\pool.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\shopee_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\tiktok_shop_api.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\tiktok_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: worker\zalo_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: workers\__init__.py

```python
# [Empty or unreadable file]
```

## FILE: workers\facebook_worker.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: workers\worker_facebook.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: workers\worker_tiktok.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

## FILE: workers\worker_zalo.py

```python
# -*- coding: utf-8 -*-
import sys, io


```

--- End of Export ---
