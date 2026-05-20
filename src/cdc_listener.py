# -*- coding: utf-8 -*-
import sqlite3
import time
import threading
from pathlib import Path
from datetime import datetime
import sys
import os

# Đảm bảo thư mục gốc được thêm vào sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.database import get_db
from src.learning.real_time_learning import RealTimeLearner
from src.config import DB_PATH

class CDCListener:
    def __init__(self, db_path=DB_PATH, poll_interval=2):
        self.db_path = db_path
        self.poll_interval = poll_interval
        self._ensure_change_table()
        self.last_id = self._get_max_change_id()
        self.running = False
        self.learner = RealTimeLearner()

    def _ensure_change_table(self):
        with sqlite3.connect(self.db_path) as conn:
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

    def _get_max_change_id(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM data_changes")
            row = cur.fetchone()
            return row[0] if row and row[0] else 0

    def _process_changes(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, table_name, row_id, operation FROM data_changes WHERE id > ? ORDER BY id", (self.last_id,))
            changes = cur.fetchall()
            for change_id, table, row_id, op in changes:
                print(f"[CDC] {op} on {table} id={row_id}")
                # Giả sử row_id là campaign_id (cần kiểm tra table)
                if table == 'campaigns' and op in ('INSERT', 'UPDATE'):
                    self.learner.add_campaign_result(row_id)
                self.last_id = change_id

    def start(self):
        self.running = True
        print("[CDC] Listener started")
        while self.running:
            self._process_changes()
            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    listener = CDCListener()
    try:
        listener.start()
    except KeyboardInterrupt:
        listener.stop()
        print("[CDC] Listener stopped")



