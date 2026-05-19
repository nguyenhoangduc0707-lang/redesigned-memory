
import re

def correct_affiliate_terms(text):
    # Thay thế các từ hay bị sai
    corrections = {
        r'\bsale\b': 'sale',
        r'\bgiam gia\b': 'giảm giá',
        r'\bmua ngay\b': 'mua ngay',
        r'\bfreeship\b': 'free ship',
        # Thêm các cặp (pattern, replacement) theo nhu cầu
    }
    for pattern, repl in corrections.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text