import os
import time
import threading
from pathlib import Path

# Sử dụng file lock đơn giản (cross-process)
RESOURCE_LOCK_FILE = Path("data/resource.lock")

class ResourceManager:
    def __init__(self, timeout=300):
        self.timeout = timeout  # chờ tối đa 5 phút
        self.lock_file = RESOURCE_LOCK_FILE

    def acquire(self, task_type):
        """Yêu cầu chiếm tài nguyên (whisper, ollama, ...)"""
        start = time.time()
        while True:
            try:
                # Tạo file lock nếu chưa có
                if not self.lock_file.exists():
                    with open(self.lock_file, 'w') as f:
                        f.write(f"{task_type}\n{os.getpid()}\n{time.time()}")
                    return True
                else:
                    # Đọc xem ai đang giữ lock
                    with open(self.lock_file, 'r') as f:
                        owner = f.readline().strip()
                        pid = int(f.readline().strip())
                        # Nếu process cũ đã chết, xóa lock
                        try:
                            os.kill(pid, 0)
                        except OSError:
                            self.lock_file.unlink()
                            continue
                        # Nếu cùng loại task, cho phép? (tuỳ chỉnh)
                        if owner == task_type:
                            # Cùng loại: tăng thời gian nhưng không chờ?
                            return True
                        # Khác loại: chờ
                        if time.time() - start > self.timeout:
                            raise TimeoutError(f"Không thể chiếm tài nguyên sau {self.timeout}s")
                        time.sleep(2)
            except Exception as e:
                print(f"Lỗi lock: {e}")
                time.sleep(1)

    def release(self):
        """Giải phóng tài nguyên"""
        if self.lock_file.exists():
            self.lock_file.unlink()