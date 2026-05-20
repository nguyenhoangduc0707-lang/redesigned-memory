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