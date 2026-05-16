import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL,
                commission REAL,
                platform TEXT,
                url TEXT,
                strategy TEXT
            );
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                platform_target TEXT,
                caption TEXT,
                link TEXT,
                status TEXT DEFAULT 'draft'
            );
        """)
    print("Database ready")

def save_products(products):
    with get_db() as conn:
        cur = conn.cursor()
        for p in products:
            cur.execute("INSERT INTO products (name, price, commission, platform, url, strategy) VALUES (?,?,?,?,?,?)",
                        (p['name'], p['price'], p.get('commission',5), p['platform'], p['url'], p.get('strategy','')))
        conn.commit()
    print(f"Saved {len(products)} products")

def save_post(product_id, platform, caption, link):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO posts (product_id, platform_target, caption, link) VALUES (?,?,?,?)",
                    (product_id, platform, caption, link))
        conn.commit()
