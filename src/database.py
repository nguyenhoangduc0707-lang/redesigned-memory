# -*- coding: utf-8 -*-
import sqlite3
from src.config import DB_PATH

def get_db():
    return sqlite3.connect(DB_PATH)

def get_db_connection():
    return get_db()

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS data_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                row_id INTEGER,
                operation TEXT NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    print("Database ready")

def save_post(product_id, platform, caption, link):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts (product_id, platform_target, caption, link) VALUES (?,?,?,?)",
            (product_id, platform, caption, link),
        )
        conn.commit()

def get_user_by_username(username):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, role FROM users WHERE username=?", (username,))
        return cur.fetchone()

def add_user(username, password, role="user"):
    from werkzeug.security import generate_password_hash
    with get_db() as conn:
        cur = conn.cursor()
        hash_pw = generate_password_hash(password)
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                (username, hash_pw, role),
            )
            user_id = cur.lastrowid
            cur.execute("INSERT INTO user_stats (user_id) VALUES (?)", (user_id,))
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
