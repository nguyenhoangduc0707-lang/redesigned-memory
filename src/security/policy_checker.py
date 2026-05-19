import re
from datetime import datetime, timedelta

user_link_history = {}

def can_send_link(user_id: str, context: str) -> bool:
    shop_keywords = ["mua", "giá", "bán", "sản phẩm", "affiliate", "deal"]
    if not any(kw in context.lower() for kw in shop_keywords):
        return False
    now = datetime.now()
    last_sent = user_link_history.get(user_id)
    if last_sent and (now - last_sent) < timedelta(hours=24):
        return False
    user_link_history[user_id] = now
    return True
