import os
import sys
from pathlib import Path
import subprocess
from add_user_table import init_user_table

print("🤖 AIWorker v3.3 - Siêu cá nhân hóa theo ý bạn")
print("Hỗ trợ lệnh kết hợp +f và -f\n")

init_user_table()

def show_help():
    print("\n📋 Cú pháp cá nhân hóa:")
    print("   +f <thư_mục>                    → Tạo thư mục")
    print("   +f <thư_mục>/-f <tên_file>      → Tạo thư mục + file")
    print("   -f <tên_file>                   → Chỉ tạo file")
    print("   help                            → Trợ giúp")
    print("   exit                            → Thoát")
    print("\nVí dụ:")
    print("   +f/devcodeai/-fmain")
    print("   +f modules/auth/-f login.py")
    print("   -f test.py")

while True:
    try:
        cmd = input("\nAIWorker> ").strip()
        
        if cmd.lower() in ['exit', 'quit']:
            print("👋 AIWorker đã dừng.")
            break

        elif cmd == "help":
            show_help()

        # ==================== XỬ LÝ LỆNH KẾT HỢP +f và -f ====================
        elif "+f" in cmd or "-f" in cmd:
            # Parse đường dẫn
            parts = cmd.replace("+f", " +f ").replace("-f", " -f ").split()
            current_path = Path(".")
            
            folder_path = None
            filename = None

            i = 0
            while i < len(parts):
                if parts[i] == "+f" and i+1 < len(parts):
                    folder_path = parts[i+1].strip("/")
                    current_path = current_path / folder_path
                    i += 2
                elif parts[i] == "-f" and i+1 < len(parts):
                    filename = parts[i+1]
                    i += 2
                else:
                    i += 1

            if folder_path:
                try:
                    current_path.mkdir(parents=True, exist_ok=True)
                    print(f"✅ Đã tạo thư mục: {current_path}")
                except Exception as e:
                    print(f"❌ Lỗi tạo thư mục: {e}")

            if filename:
                file_path = current_path / filename
                print(f"\n📍 Đường dẫn đầy đủ: {file_path.absolute()}")
                
                # Tạo file và nhập code
                print("📝 Mời bạn nhập code (gõ END trên dòng riêng để kết thúc):")
                code_lines = []
                while True:
                    line = input()
                    if line.strip() == "END":
                        break
                    code_lines.append(line)
                
                code = "\n".join(code_lines)
                
                if not code.strip():
                    print("Không có code.")
                    continue

                # === DEBUG CODE ===
                print("\n🔍 Đang debug code...")
                try:
                    # Kiểm tra syntax Python
                    compile(code, "<string>", "exec")
                    print("✅ Debug syntax: Thành công (không lỗi cú pháp)")
                except SyntaxError as e:
                    print(f"❌ Lỗi syntax: {e}")
                    print("Bạn có muốn sửa lại code không? (y/n)")
                    if input().strip().lower() == 'y':
                        continue

                # Preview
                print("\n" + "="*70)
                print("PREVIEW CODE:")
                print("="*70)
                print(code[:800] + "..." if len(code) > 800 else code)
                print("="*70)

                # Chọn extension
                print("\nChọn định dạng file:")
                print("1. .py     2. .js     3. .html     4. .md     5. .txt     6. Khác")
                ext_choice = input("Nhập số (Enter = .py): ").strip()
                
                extensions = { "1":".py", "2":".js", "3":".html", "4":".md", "5":".txt", "6":"" }
                chosen_ext = extensions.get(ext_choice, ".py")
                
                if chosen_ext == "" and "." not in filename:
                    chosen_ext = input("Nhập extension (ví dụ: .java): ").strip()
                
                if "." not in filename:
                    final_path = file_path.with_suffix(chosen_ext)
                else:
                    final_path = file_path

                print(f"\nFile sẽ được lưu với tên: {final_path.name}")
                print("Bạn muốn lưu file? (y/n)")
                
                if input().strip().lower() == 'y':
                    try:
                        with open(final_path, "w", encoding="utf-8") as f:
                            f.write(code)
                        print(f"\n✅ SAVE OK! File đã được lưu thành công.")
                        print(f"   Đường dẫn: {final_path.absolute()}")
                    except Exception as e:
                        print(f"❌ Lỗi lưu file: {e}")
                else:
                    print("❌ Đã hủy lưu file.")

        else:
            print("🤖 Lệnh không nhận diện.")
            print("Gõ 'help' để xem hướng dẫn.")

    except Exception as e:
        print(f"Lỗi: {e}")
