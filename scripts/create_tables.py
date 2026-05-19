# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Báº£ng algorithm_params (quan trá»ng nháº¥t)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            param_name TEXT NOT NULL,
            param_value REAL NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    ''')
    
    # CÃ¡c báº£ng khÃ¡c cáº§n thiáº¿t
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            platform TEXT,
            start_date TEXT,
            end_date TEXT,
            budget REAL,
            goal TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaign_products (
            campaign_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaign_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            predicted_posts INTEGER,
            predicted_likes INTEGER,
            predicted_sales INTEGER,
            predicted_revenue REAL,
            prediction_date TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS campaign_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            actual_posts INTEGER,
            actual_likes INTEGER,
            actual_sales INTEGER,
            actual_revenue REAL,
            accuracy_percent REAL,
            result_date TIMESTAMP
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            adjustment_reason TEXT,
            old_params TEXT,
            new_params TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("âœ… All tables created successfully!")

if __name__ == "__main__":
    create_tables()

