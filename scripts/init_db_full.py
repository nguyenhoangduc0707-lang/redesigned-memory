# -*- coding: utf-8 -*-
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def init_all_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # T?o b?ng algorithm_params (quan tr?ng nh?t, dang thi?u)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS algorithm_params (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            param_name TEXT NOT NULL,
            param_value REAL NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    ''')
    
    # T?o b?ng campaigns
    cursor.execute('''
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
    
    # T?o b?ng campaign_products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_products (
            campaign_id INTEGER,
            product_id INTEGER,
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    # T?o b?ng campaign_predictions
    cursor.execute('''
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
    
    # T?o b?ng campaign_results
    cursor.execute('''
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
    
    # T?o b?ng algorithm_adjustments
    cursor.execute('''
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
    print("? All required tables created successfully!")

if __name__ == "__main__":
    init_all_tables()

