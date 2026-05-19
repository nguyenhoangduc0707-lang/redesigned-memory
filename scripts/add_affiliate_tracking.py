from src.database import get_db


def add_tables():
    with get_db() as conn:
        cur = conn.cursor()

        for col in ("affiliate_code", "referrer_id", "last_reset_date", "daily_link_count"):
            try:
                cur.execute(f"ALTER TABLE users ADD COLUMN {col}")
            except Exception:
                pass
        cur.execute(
            "UPDATE users SET daily_link_count=3, last_reset_date=date('now') "
            "WHERE daily_link_count IS NULL"
        )

        cur.execute("""
            CREATE TABLE IF NOT EXISTS affiliate_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                link_code TEXT UNIQUE,
                target_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                used_count INTEGER DEFAULT 0,
                max_uses_per_day INTEGER DEFAULT 3,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS link_clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link_id INTEGER,
                clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                FOREIGN KEY (link_id) REFERENCES affiliate_links(id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                image_url TEXT,
                destination_url TEXT,
                reward_type TEXT,
                reward_value INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS commissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("[OK] Affiliate tracking tables ready")


if __name__ == "__main__":
    add_tables()
