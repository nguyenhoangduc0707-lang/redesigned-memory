#!/usr/bin/env python3
"""
Khởi tạo database cho CI.
Tự động phát hiện và gọi hàm init_db từ src.database nếu có.
"""

import sys
import os
import importlib

def main():
    # Thêm thư mục gốc vào path để import src
    sys.path.insert(0, os.getcwd())
    
    # Thử import module database
    try:
        db_module = importlib.import_module("src.database")
        if hasattr(db_module, "init_db"):
            print("📦 Gọi src.database.init_db()...")
            db_module.init_db()
        elif hasattr(db_module, "create_tables"):
            print("📦 Gọi src.database.create_tables()...")
            db_module.create_tables()
        else:
            print("⚠️ Không tìm thấy hàm init_db hoặc create_tables trong src.database")
            fallback_init()
    except ImportError:
        print("⚠️ Không thể import src.database, dùng fallback init...")
        fallback_init()

def fallback_init():
    """Tạo bảng tối thiểu nếu không có database module"""
    import sqlite3
    conn = sqlite3.connect("ai_os.db")
    cursor = conn.cursor()
    # Tạo các bảng cơ bản (bạn có thể bổ sung theo nhu cầu test)
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS campaigns (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    conn.close()
    print("✅ Fallback database created with basic tables.")

if __name__ == "__main__":
    main()