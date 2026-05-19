import importlib
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import DB_PATH, ROOT_DIR


REQUIRED_TABLES = {
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            commission REAL,
            platform TEXT,
            url TEXT,
            strategy TEXT
        )
    """,
    "posts": """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            platform_target TEXT,
            caption TEXT,
            link TEXT,
            status TEXT DEFAULT 'draft'
        )
    """,
    "campaigns": """
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            platform TEXT,
            start_date DATE,
            end_date DATE,
            budget REAL,
            goal TEXT,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
    "data_changes": """
        CREATE TABLE IF NOT EXISTS data_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            row_id INTEGER,
            operation TEXT NOT NULL,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """,
}


def check_imports():
    for module in (
        "src.main",
        "src.database",
        "src.cdc_listener",
        "src.notebooklm_pro",
        "src.key_manager",
        "src.devweb_agent",
        "src.media.image_gen",
        "src.ml.algo_simulator",
        "src.learning.sentiment_analyzer",
        "src.agents.crm_bot",
        "worker.executor",
    ):
        importlib.import_module(module)
        print(f"[OK] import {module}")


def check_templates():
    for name in (
        "login.html",
        "unified_dashboard.html",
        "create_video.html",
        "video_result.html",
        "notebooklm.html",
        "review_station.html",
    ):
        path = ROOT_DIR / "src" / "templates" / name
        if not path.exists():
            raise FileNotFoundError(path)
        print(f"[OK] template {name}")


def check_database():
    with sqlite3.connect(DB_PATH) as conn:
        for ddl in REQUIRED_TABLES.values():
            conn.execute(ddl)
        conn.commit()
        existing = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    for table in REQUIRED_TABLES:
        if table not in existing:
            raise RuntimeError(f"Missing table: {table}")
        print(f"[OK] table {table}")


def check_models():
    model = ROOT_DIR / "models" / "sales_prediction_model.pkl"
    fp16 = ROOT_DIR / "models" / "sales_prediction_model_fp16.pkl"
    print(f"[{'OK' if model.exists() else 'WARN'}] model {model.name}")
    print(f"[{'OK' if fp16.exists() else 'WARN'}] model {fp16.name}")


def main():
    check_imports()
    check_templates()
    check_database()
    check_models()
    print("[OK] validation complete")


if __name__ == "__main__":
    main()
