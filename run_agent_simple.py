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
