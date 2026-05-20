# -*- coding: utf-8 -*-
import sys
import os
# Thêm đường dẫn thư mục gốc (chứa src)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import joblib
import pandas as pd
from src.database import get_db
...

print("=" * 60)
print("?? KI?M TRA SALES PREDICTION MODEL")
print("=" * 60)

# 1. Ki?m tra file model
model_path = "models/sales_prediction_model.pkl"
if os.path.exists(model_path):
    print(f"? Model file exists: {model_path}")
    size = os.path.getsize(model_path) / 1024
    print(f"   Size: {size:.2f} KB")
else:
    print(f"? Model file not found: {model_path}")
    print("   C?n train model m?i!")

# 2. Load model và ki?m tra
try:
    model = joblib.load(model_path)
    print(f"\n? Model loaded successfully")
    print(f"   Type: {type(model).__name__}")
except Exception as e:
    print(f"? Cannot load model: {e}")

# 3. Ki?m tra d? li?u trong database
print("\n?? KI?M TRA D? LI?U TRAINING")
with get_db() as conn:
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM campaigns")
    campaign_count = cur.fetchone()[0]
    print(f"   Campaigns: {campaign_count}")
    
    cur.execute("""
        SELECT COUNT(*) FROM campaigns 
        WHERE status='completed' AND budget IS NOT NULL
    """)
    completed = cur.fetchone()[0]
    print(f"   Completed campaigns: {completed}")
    
    if completed < 10:
        print(f"   ?? Not enough data ({completed}/10 needed)")

print("\n" + "=" * 60)



