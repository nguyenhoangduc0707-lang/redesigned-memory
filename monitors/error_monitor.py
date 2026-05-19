# error_monitor.py
import os
import sys
import traceback
import datetime
import logging
from functools import wraps
from flask import request, jsonify

# ========== CẤU HÌNH LOGGING ==========
LOG_DIR = "error_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# File log chính
ERROR_LOG_FILE = os.path.join(LOG_DIR, f"errors_{datetime.datetime.now().strftime('%Y%m%d')}.log")
FULL_LOG_FILE = os.path.join(LOG_DIR, f"full_system_{datetime.datetime.now().strftime('%Y%m%d')}.log")

# Cấu hình logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s',
    handlers=[
        logging.FileHandler(FULL_LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# File riêng cho lỗi
error_logger = logging.getLogger('error_logger')
error_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
error_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

# ========== DECORATOR GHI LỖI ==========
def log_error(func):
    """Decorator tự động ghi lỗi cho function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            error_msg = f"""
{'='*60}
FUNCTION: {func.__name__}
FILE: {func.__code__.co_filename}
LINE: {func.__code__.co_firstlineno}
ERROR: {str(e)}
TRACEBACK:
{traceback.format_exc()}
ARGS: {args}
KWARGS: {kwargs}
{'='*60}
"""
            error_logger.error(error_msg)
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def log_route_error(func):
    """Decorator cho Flask routes - trả về JSON lỗi"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"""
{'='*60}
ROUTE: {request.path}
METHOD: {request.method}
IP: {request.remote_addr}
ERROR: {str(e)}
TRACEBACK:
{traceback.format_exc()}
{'='*60}
"""
            error_logger.error(error_msg)
            logger.error(f"Route {request.path} error: {str(e)}")
            return jsonify({
                "error": str(e),
                "path": request.path,
                "method": request.method,
                "timestamp": datetime.datetime.now().isoformat()
            }), 500
    return wrapper

# ========== CLASS QUẢN LÝ LỖI ==========
class ErrorManager:
    """Quản lý và theo dõi lỗi hệ thống"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {
            "total_errors": 0,
            "total_warnings": 0,
            "errors_by_type": {},
            "errors_by_route": {}
        }
    
    def add_error(self, error_type, message, details=None, route=None):
        """Thêm lỗi vào danh sách"""
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": error_type,
            "message": message,
            "details": details,
            "route": route
        }
        self.errors.append(error_entry)
        self.stats["total_errors"] += 1
        
        # Thống kê theo loại
        if error_type not in self.stats["errors_by_type"]:
            self.stats["errors_by_type"][error_type] = 0
        self.stats["errors_by_type"][error_type] += 1
        
        # Thống kê theo route
        if route:
            if route not in self.stats["errors_by_route"]:
                self.stats["errors_by_route"][route] = 0
            self.stats["errors_by_route"][route] += 1
        
        # Ghi vào file
        error_logger.error(f"[{error_type}] {message} | {details}")
    
    def add_warning(self, warning_type, message, details=None):
        """Thêm cảnh báo"""
        warning_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": warning_type,
            "message": message,
            "details": details
        }
        self.warnings.append(warning_entry)
        self.stats["total_warnings"] += 1
        logger.warning(f"[{warning_type}] {message}")
    
    def get_all_errors(self):
        """Lấy tất cả lỗi"""
        return self.errors
    
    def get_error_summary(self):
        """Lấy tóm tắt lỗi"""
        return {
            "total_errors": self.stats["total_errors"],
            "total_warnings": self.stats["total_warnings"],
            "errors_by_type": self.stats["errors_by_type"],
            "errors_by_route": self.stats["errors_by_route"],
            "recent_errors": self.errors[-10:] if self.errors else []
        }
    
    def clear_errors(self):
        """Xóa danh sách lỗi (giữ thống kê)"""
        self.errors = []
        self.warnings = []
    
    def export_report(self):
        """Xuất báo cáo lỗi ra file"""
        report_file = os.path.join(LOG_DIR, f"error_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        import json
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "stats": self.stats,
            "errors": self.errors[-50:],  # 50 lỗi gần nhất
            "warnings": self.warnings[-50:]
        }
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return report_file

# ========== KIỂM TRA HỆ THỐNG ==========
def system_check():
    """Kiểm tra toàn bộ hệ thống, trả về danh sách lỗi"""
    issues = []
    
    # 1. Kiểm tra file cấu hình
    if not os.path.exists(".env"):
        issues.append("[WARN] Missing .env file")
    else:
        # Kiểm tra các biến bắt buộc
        import dotenv
        dotenv.load_dotenv()
        if not os.getenv("SECRET_KEY") or os.getenv("SECRET_KEY") == "default-dev-key-change-me-in-production" or len(os.getenv("SECRET_KEY")) < 10:
            issues.append("[ERROR] SECRET_KEY not set properly in .env")
    
    # 2. Kiểm tra database
    try:
        from src.database import get_db
        with get_db() as conn:
            conn.execute("SELECT 1")
    except Exception as e:
        issues.append(f"[ERROR] Database connection failed: {e}")
    
    # 3. Kiểm tra thư viện bắt buộc
    required_libs = ["flask", "requests", "sqlite3"]
    for lib in required_libs:
        try:
            __import__(lib)
        except ImportError:
            issues.append(f"[ERROR] Missing required library: {lib}")
    
    # 4. Kiểm tra thư mục
    required_dirs = ["src/templates", "logs", "models"]
    for d in required_dirs:
        if not os.path.exists(d):
            issues.append(f"[WARN] Missing directory: {d}")
    
    # 5. Kiểm tra cấu hình Flask
    try:
        from src.main import app
        if not app.secret_key or app.secret_key == "default-dev-key-change-me":
            issues.append("[WARN] Using default secret key")
        if app.debug:
            issues.append("[WARN] Debug mode is ON (should be OFF in production)")
    except Exception as e:
        issues.append(f"[ERROR] Flask app initialization failed: {e}")
    
    return issues

# ========== HÀM TIỆN ÍCH ==========
def get_error_report_html():
    """Tạo báo cáo lỗi dạng HTML"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Error Report - AI_OS_KERNEL_V3</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .error { background-color: #ffebee; border-left: 4px solid #f44336; padding: 10px; margin: 10px 0; }
            .warning { background-color: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 10px 0; }
            .info { background-color: #e3f2fd; border-left: 4px solid #2196f3; padding: 10px; margin: 10px 0; }
            pre { background: #f5f5f5; padding: 10px; overflow-x: auto; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
        </style>
    </head>
    <body>
        <h1>📋 Error Report - AI_OS_KERNEL_V3</h1>
        <p>Generated: {timestamp}</p>
    """
    
    # Thêm thống kê
    html += f"""
    <h2>📊 Statistics</h2>
    <table>
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Total Errors</td><td>{error_manager.stats['total_errors']}</td></tr>
        <tr><td>Total Warnings</td><td>{error_manager.stats['total_warnings']}</td></tr>
    </table>
    """
    
    # Thêm lỗi theo loại
    if error_manager.stats['errors_by_type']:
        html += "<h2>🔴 Errors by Type</h2><ul>"
        for err_type, count in error_manager.stats['errors_by_type'].items():
            html += f"<li>{err_type}: {count}</li>"
        html += "</ul>"
    
    # Thêm danh sách lỗi gần đây
    if error_manager.errors:
        html += "<h2>🟡 Recent Errors</h2>"
        for err in error_manager.errors[-20:]:
            html += f"""
            <div class="error">
                <strong>{err['timestamp']}</strong><br>
                <strong>Type:</strong> {err['type']}<br>
                <strong>Message:</strong> {err['message']}<br>
                <strong>Route:</strong> {err.get('route', 'N/A')}<br>
                <details><summary>Details</summary><pre>{err.get('details', 'No details')}</pre></details>
            </div>
            """
    
    html += "</body></html>"
    return html

# ========== KHỞI TẠO ==========
error_manager = ErrorManager()

# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🔍 ERROR MONITOR - AI_OS_KERNEL_V3")
    print("=" * 60)
    
    # Kiểm tra hệ thống
    print("\n📋 Running system check...")
    issues = system_check()
    
    if issues:
        print("\n⚠️ ISSUES FOUND:")
        for issue in issues:
            if "[ERROR]" in issue:
                error_manager.add_error("SystemCheck", issue, "System initialization")
                print(f"  🔴 {issue}")
            else:
                error_manager.add_warning("SystemCheck", issue)
                print(f"  🟡 {issue}")
    else:
        print("✅ No issues found")
    
    # Xuất báo cáo
    report_file = error_manager.export_report()
    print(f"\n📄 Report exported: {report_file}")
    
    print("\n📊 Summary:")
    print(f"   Total errors: {error_manager.stats['total_errors']}")
    print(f"   Total warnings: {error_manager.stats['total_warnings']}")
