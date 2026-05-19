#!/usr/bin/env python3
"""
Kiểm tra toàn diện core system của AI_OS Kernel V3.
Chạy lệnh: python test_brain_full.py
"""

import sys
import os
import traceback

# Thêm thư mục gốc vào path
sys.path.insert(0, os.getcwd())

print("="*60)
print(" KIỂM TRA NÃO BỘ AI_OS KERNEL V3")
print("="*60)

# 1. IMPORT CORE MODULES
print("\n1. IMPORT CÁC MODULE CHÍNH...")
modules_to_test = [
    ("src.config", ["ROOT_DIR", "DEBUG", "DB_PATH"]),
    ("src.database", ["get_db_connection", "init_db"]),
    ("src.agents", ["Agent"]),
    ("src.orchestrator", ["Orchestrator"]),
    ("src.main", ["app"]),
    ("src.key_manager", ["audit_keys", "classify_value"]),
    ("src.devweb_agent", ["redact_headers"]),
    ("src.notebooklm_pro", ["NotebookLMPro"]),
]

failed_imports = []
for module_name, attrs in modules_to_test:
    try:
        mod = __import__(module_name, fromlist=attrs)
        for attr in attrs:
            if hasattr(mod, attr):
                print(f"   ✓ {module_name}.{attr}")
            else:
                print(f"   ⚠ {module_name} missing attribute {attr}")
    except Exception as e:
        print(f"   ✗ {module_name} import error: {e}")
        failed_imports.append(module_name)

if failed_imports:
    print(f"\n⚠ Có {len(failed_imports)} module import lỗi: {failed_imports}")
else:
    print("\n✓ Tất cả module chính import thành công.")

# 2. KIỂM TRA DATABASE
print("\n2. KIỂM TRA DATABASE...")
try:
    from src.database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"   ✓ Kết nối thành công. Các bảng: {[t[0] for t in tables]}")
    conn.close()
except Exception as e:
    print(f"   ✗ Lỗi database: {e}")
    traceback.print_exc()

# 3. KIỂM TRA AGENT CƠ BẢN
print("\n3. KIỂM TRA AGENT CƠ BẢN...")
try:
    from src.agents import Agent
    agent = Agent("test_agent")
    print(f"   ✓ Khởi tạo Agent thành công: {agent}")
except Exception as e:
    print(f"   ✗ Lỗi Agent: {e}")
    traceback.print_exc()

# 4. KIỂM TRA ORCHESTRATOR (nếu có)
print("\n4. KIỂM TRA ORCHESTRATOR...")
try:
    from src.orchestrator import Orchestrator
    orch = Orchestrator()
    print(f"   ✓ Orchestrator khởi tạo thành công")
except Exception as e:
    print(f"   ✗ Lỗi Orchestrator: {e}")

# 5. KIỂM TRA SENSOR BRAIN (sen_brain.py)
print("\n5. KIỂM TRA SEN_BRAIN...")
try:
    import sen_brain
    print("   ✓ sen_brain module loaded")
except Exception as e:
    print(f"   ✗ Lỗi sen_brain: {e}")

# 6. THỬ CHẠY MỘT HÀNH ĐỘNG NHỎ (nếu có)
print("\n6. THỬ CHẠY MỘT LUỒNG NGẮN...")
try:
    # Ví dụ: gọi một hàm xử lý dữ liệu mẫu
    from src.database import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'test_user')")
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE name='test_user'")
    row = cursor.fetchone()
    if row:
        print(f"   ✓ Ghi và đọc database thành công: {row}")
    else:
        print("   ⚠ Không thể ghi dữ liệu vào database (có thể thiếu bảng users)")
    conn.close()
except Exception as e:
    print(f"   ✗ Lỗi thực thi luồng: {e}")

print("\n" + "="*60)
print(" KẾT THÚC KIỂM TRA NÃO BỘ")
print("="*60)