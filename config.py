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
