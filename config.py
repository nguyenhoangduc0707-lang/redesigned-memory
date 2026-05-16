# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # nếu vẫn dùng .env sau khi đã xử lý bảo mật

DB_PATH = os.getenv('DB_PATH', 'affiliate.db')
MODEL_PATH = os.getenv('MODEL_PATH', 'models/sales_prediction_model.pkl')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
