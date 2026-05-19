#!/usr/bin/env python3
"""
Kiểm tra tính tương thích giữa dự án AI_OS_KERNEL_V3 và CI workflow.
Chạy lệnh: python check_compatibility.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Màu sắc cho console (tuỳ chọn)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")

def print_ok(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def safe_read_text(filepath, encoding_list=['utf-8', 'latin-1', 'cp1252']):
    """Thử đọc file với nhiều encoding, trả về nội dung hoặc None nếu lỗi"""
    for enc in encoding_list:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, IOError):
            continue
    return None

def check_file_exists(filepath, name):
    if Path(filepath).exists():
        print_ok(f"{name} tồn tại: {filepath}")
        return True
    else:
        print_error(f"{name} không tìm thấy: {filepath}")
        return False

def check_directory_exists(dirpath, name):
    if Path(dirpath).is_dir():
        print_ok(f"{name} tồn tại: {dirpath}")
        return True
    else:
        print_error(f"{name} không tồn tại: {dirpath}")
        return False

def check_requirements_txt():
    req_file = "requirements.txt"
    if not Path(req_file).exists():
        print_error("requirements.txt không tồn tại - workflow sẽ thất bại")
        return False
    
    content = safe_read_text(req_file)
    if content is None:
        print_error("Không thể đọc requirements.txt (lỗi encoding)")
        return False
        
    if not content.strip():
        print_warning("requirements.txt rỗng - hãy chạy 'pip freeze > requirements.txt'")
        return False
    
    # Các gói tối thiểu cần có
    required_packages = ['pytest', 'pytest-cov', 'requests']
    missing = []
    for pkg in required_packages:
        if pkg not in content:
            missing.append(pkg)
    if missing:
        print_warning(f"Thiếu gói đề xuất trong requirements.txt: {', '.join(missing)}")
    else:
        print_ok("requirements.txt có đầy đủ các gói cơ bản")
    
    return True

def check_pytest_installed():
    try:
        import pytest
        print_ok(f"pytest đã cài đặt (phiên bản {pytest.__version__})")
        return True
    except ImportError:
        print_error("pytest chưa được cài đặt trong môi trường hiện tại")
        return False

def check_test_directory():
    test_dir = "tests"
    if Path(test_dir).is_dir():
        test_files = list(Path(test_dir).glob("test_*.py")) + list(Path(test_dir).glob("*_test.py"))
        if test_files:
            print_ok(f"Thư mục tests/ chứa {len(test_files)} file test")
            return True
        else:
            print_warning("Thư mục tests/ tồn tại nhưng không có file test_*.py")
            return False
    else:
        print_error("Thư mục tests/ không tồn tại - workflow sẽ không kiểm tra được gì")
        return False

def check_env_file():
    if not Path(".env").exists():
        print_warning(".env file không tồn tại (có thể dùng GitHub Secrets)")
        return False
    
    content = safe_read_text(".env")
    if content is None:
        print_error("Không thể đọc .env file (lỗi encoding) - hãy kiểm tra định dạng hoặc xóa ký tự lạ")
        return False
    
    print_ok(".env file tồn tại (chú ý: không nên commit lên GitHub, dùng secrets)")
    # Kiểm tra các biến thường dùng
    if "OPENAI_API_KEY" in content:
        print_ok("  - OPENAI_API_KEY có trong .env")
    if "DATABASE_URL" in content:
        print_ok("  - DATABASE_URL có trong .env")
    return True

def check_database():
    db_files = ["ai_os.db", "affiliate.db"]
    for db in db_files:
        if Path(db).exists():
            print_ok(f"Database {db} tồn tại (local, sẽ không có trên CI)")
        else:
            print_warning(f"Database {db} không tồn tại (có thể cần init_db.py trên CI)")

def check_init_db_script():
    if Path("init_db.py").exists():
        print_ok("init_db.py có sẵn - có thể dùng để tạo database trên CI")
        return True
    else:
        print_warning("Không tìm thấy init_db.py - nếu dùng database, cần script khởi tạo")
        return False

def check_powershell_scripts():
    ps_scripts = list(Path(".").glob("*.ps1"))
    if ps_scripts:
        print_warning(f"Phát hiện {len(ps_scripts)} PowerShell scripts. Workflow trên Ubuntu không chạy được PS mặc định.")
        print("  → Nếu cần, hãy cài pwsh hoặc chuyển logic quan trọng sang Python.")
    else:
        print_ok("Không có PowerShell script nào - không lo về tương thích nền tảng.")

def suggest_workflow_improvements():
    print(f"\n{Colors.BOLD}>>> ĐỀ XUẤT CẢI THIỆN WORKFLOW <<<{Colors.RESET}")
    suggestions = []
    
    if not Path("requirements.txt").exists() or Path("requirements.txt").stat().st_size < 50:
        suggestions.append("Tạo lại requirements.txt bằng lệnh: pip freeze > requirements.txt")
    
    if not Path("tests").is_dir():
        suggestions.append("Tạo thư mục tests/ và viết ít nhất một test (ví dụ test_sample.py)")
    
    if Path(".env").exists():
        suggestions.append("Thêm các biến môi trường vào GitHub Secrets và dùng env: trong workflow")
    
    if Path("ai_os.db").exists() and not Path("init_db.py").exists():
        suggestions.append("Tạo script init_db.py để khởi tạo database trên CI (chạy trước khi test)")
    
    if suggestions:
        for i, sug in enumerate(suggestions, 1):
            print(f"  {i}. {sug}")
    else:
        print_ok("Dự án của bạn đã sẵn sàng cho CI cơ bản! 🎉")

def main():
    print_header("KIỂM TRA TƯƠNG THÍCH CI CHO AI_OS_KERNEL_V3")
    
    # 1. Cấu trúc cơ bản
    print_header("1. CẤU TRÚC THƯ MỤC & FILE")
    check_file_exists("requirements.txt", "requirements.txt")
    check_file_exists(".gitignore", ".gitignore (nên có)")
    check_directory_exists("tests", "Thư mục tests")
    check_directory_exists("src", "Thư mục src (module chính)")
    
    # 2. Môi trường Python và thư viện
    print_header("2. MÔI TRƯỜNG PYTHON & THƯ VIỆN")
    print(f"Python version: {sys.version}")
    check_requirements_txt()
    check_pytest_installed()
    
    # 3. Kiểm tra test
    print_header("3. KIỂM TRA BỘ TEST")
    has_tests = check_test_directory()
    if not has_tests:
        print_warning("Bạn nên tạo ít nhất một test để CI có ý nghĩa")
    
    # 4. Database và cấu hình
    print_header("4. DATABASE & MÔI TRƯỜNG")
    check_env_file()
    check_database()
    check_init_db_script()
    
    # 5. Các thành phần khác
    print_header("5. CÁC THÀNH PHẦN KHÁC")
    check_powershell_scripts()
    
    # 6. Đề xuất
    print_header("ĐỀ XUẤT CẢI THIỆN")
    suggest_workflow_improvements()
    
    # Kết luận
    print_header("KẾT LUẬN")
    print("Bạn có thể sử dụng workflow CI đã đề xuất, nhưng hãy chú ý các cảnh báo trên.")
    print("Để workflow chạy thành công, hãy đảm bảo các bước khởi tạo DB và cài đặt đủ thư viện.")

if __name__ == "__main__":
    main()