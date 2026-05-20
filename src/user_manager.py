import sqlite3

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import get_db


class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role


def get_db_connection():
    return get_db()


def add_user(username, password, role="user"):
    with get_db_connection() as conn:
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


def authenticate_user(username, password):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, role FROM users WHERE username=?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row[2], password):
            return User(row[0], row[1], row[3])
    return None


def get_user_by_id(user_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if row:
            return User(row[0], row[1], row[2])
    return None


def list_users():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, role, created_at FROM users")
        return cur.fetchall()
