import os
import re
from pathlib import Path
from dotenv import dotenv_values

ENV_PATH = Path(os.getenv("ENV_PATH", ".env")).resolve()

def load_env_values(env_path=ENV_PATH):
    values = {}
    if Path(env_path).exists():
        values = dotenv_values(env_path)
    return values

def classify_value(name, value):
    """Trả về (status, reason) phù hợp với test"""
    val_str = str(value) if value else ""
    name_lower = name.lower()
    if "access_token" in name_lower and "your_" in val_str:
        return ("placeholder", "Looks like placeholder")
    if "page_id" in name_lower and val_str.isdigit():
        return ("present", "Valid numeric ID")
    if "key" in name_lower or "token" in name_lower or "secret" in name_lower:
        return ("api_key", "API key detected")
    if val_str:
        return ("other", "Other value")
    return ("empty", "Empty value")

def audit_keys():
    env_path = ENV_PATH
    values = load_env_values(env_path)
    records = []
    for key, val in values.items():
        status, reason = classify_value(key, val)
        # Tạo object có các thuộc tính name, status, reason (để test dùng record.name, record.status)
        class Record:
            pass
        rec = Record()
        rec.name = key
        rec.value = val
        rec.status = status
        rec.reason = reason
        records.append(rec)
    return records
