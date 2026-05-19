# src/affiliate_manager.py
import secrets, sqlite3
from datetime import date

from src.config import DB_PATH

def get_db():
    return sqlite3.connect(DB_PATH)

def init_affiliate_tables():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS affiliate_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                link_code TEXT UNIQUE,
                target_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_count INTEGER DEFAULT 0,
                max_uses_per_day INTEGER DEFAULT 3
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS link_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id INTEGER,
                clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                image_url TEXT,
                destination_url TEXT,
                reward_type TEXT,
                reward_value INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS commissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        for col in ['affiliate_code', 'referrer_id', 'daily_link_count', 'last_reset_date']:
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT")
            except: pass
        cur.execute("UPDATE users SET daily_link_count = 3 WHERE daily_link_count IS NULL")
        cur.execute("UPDATE users SET last_reset_date = date('now') WHERE last_reset_date IS NULL")
        conn.commit()
        print("âœ… Affiliate tables ready")

def get_user_role(user_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else 'user'

def can_create_link(user_id):
    role = get_user_role(user_id)
    if role != 'user':
        return True
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT daily_link_count, last_reset_date FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row: return False
        limit, last = row
        today = date.today().isoformat()
        if last != today:
            cur.execute("UPDATE users SET daily_link_count=3, last_reset_date=? WHERE id=?", (today, user_id))
            conn.commit()
            return True
        return limit > 0

def decrement_link_quota(user_id):
    role = get_user_role(user_id)
    if role != 'user': return True
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET daily_link_count = daily_link_count - 1 WHERE id=? AND daily_link_count > 0", (user_id,))
        conn.commit()
        return cur.rowcount > 0

def create_affiliate_link(user_id, target_url):
    if not can_create_link(user_id):
        return None, "Báº¡n Ä‘Ã£ háº¿t lÆ°á»£t táº¡o link hÃ´m nay. HÃ£y xem quáº£ng cÃ¡o Ä‘á»ƒ nháº­n thÃªm lÆ°á»£t."
    code = secrets.token_urlsafe(8)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO affiliate_links (user_id, link_code, target_url) VALUES (?,?,?)", (user_id, code, target_url))
        conn.commit()
        decrement_link_quota(user_id)
    return code, None

def get_random_ad():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, title, image_url, destination_url, reward_type, reward_value FROM ads ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchone()
        if row:
            return {"id": row[0], "title": row[1], "image_url": row[2], "destination_url": row[3], "reward_type": row[4], "reward_value": row[5]}
    return None

def reward_user_for_ad(user_id, ad):
    rtype = ad['reward_type']
    val = ad['reward_value']
    with get_db() as conn:
        cur = conn.cursor()
        if rtype == 'extra_link':
            cur.execute("UPDATE users SET daily_link_count = daily_link_count + ? WHERE id=?", (val, user_id))
            conn.commit()
            return f"Nháº­n thÃªm {val} lÆ°á»£t táº¡o link."
        elif rtype == 'direct_commission':
            cur.execute("INSERT INTO commissions (user_id, amount, description) VALUES (?,?,?)", (user_id, val, f"Xem ad: {ad['title']}"))
            conn.commit()
            return f"Nháº­n {val} VND hoa há»“ng."
    return "Cáº£m Æ¡n."

def track_click(link_code, ip):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, user_id FROM affiliate_links WHERE link_code=?", (link_code,))
        row = cur.fetchone()
        if not row: return None
        link_id, uid = row
        cur.execute("INSERT INTO link_clicks (link_id, ip_address) VALUES (?,?)", (link_id, ip))
        cur.execute("UPDATE affiliate_links SET used_count = used_count + 1 WHERE id=?", (link_id,))
        conn.commit()
        return uid
    return None

def record_commission(sale_amount, user_id, description):
    """Chia hoa hồng: 40% user, 30% referrer, 30% admin (user_id=1)"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT referrer_id FROM users WHERE id=?", (user_id,))
        ref_row = cur.fetchone()
        manager_id = ref_row[0] if ref_row else None
        admin_id = 1
        commission_user = sale_amount * 0.4
        commission_manager = sale_amount * 0.3 if manager_id else 0
        commission_admin = sale_amount * 0.3
        if commission_user > 0:
            cur.execute("INSERT INTO commissions (user_id, amount, description, status) VALUES (?,?,?,?)",
                        (user_id, commission_user, description, 'confirmed'))
        if manager_id and commission_manager > 0:
            cur.execute("INSERT INTO commissions (user_id, amount, description, status) VALUES (?,?,?,?)",
                        (manager_id, commission_manager, description, 'confirmed'))
        if commission_admin > 0:
            cur.execute("INSERT INTO commissions (user_id, amount, description, status) VALUES (?,?,?,?)",
                        (admin_id, commission_admin, description, 'confirmed'))
        conn.commit()
