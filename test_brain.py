# test_brain.py - Kiểm tra nhanh core system
import sys
print("1. Kiểm tra import các module chính...")
try:
    from src.config import ROOT_DIR, DEBUG
    print(f"   ✓ Config loaded, ROOT_DIR={ROOT_DIR}")
except Exception as e:
    print(f"   ✗ Config error: {e}")

try:
    from src.database import get_db_connection
    print("   ✓ Database module loaded")
except Exception as e:
    print(f"   ✗ Database error: {e}")

try:
    from src.agents import Agent
    print("   ✓ Agent module loaded")
except Exception as e:
    print(f"   ✗ Agent error: {e}")

try:
    from src.main import app  # nếu có Flask/FastAPI app
    print("   ✓ Main app loaded")
except:
    print("   ⚠ Không có main app (hoặc không import được)")

print("\n2. Kiểm tra database connection...")
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"   ✓ Database connected, tables: {[t[0] for t in tables]}")
    conn.close()
except Exception as e:
    print(f"   ✗ DB error: {e}")

print("\n3. Kiểm tra orchestrator...")
try:
    from src.orchestrator import Orchestrator  # nếu có
    print("   ✓ Orchestrator loaded")
except:
    print("   ⚠ Orchestrator not found or error")

print("\nHoàn tất kiểm tra não bộ.")