import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                platform TEXT,
                start_date DATE,
                end_date DATE,
                budget REAL,
                goal TEXT,
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS campaign_products (
                campaign_id INTEGER,
                product_id INTEGER,
                post_ids TEXT,
                FOREIGN KEY(campaign_id) REFERENCES campaigns(id),
                FOREIGN KEY(product_id) REFERENCES products(id)
            );
            CREATE TABLE IF NOT EXISTS campaign_predictions (
                campaign_id INTEGER,
                predicted_posts INTEGER,
                predicted_likes REAL,
                predicted_sales INTEGER,
                predicted_revenue REAL,
                prediction_date TIMESTAMP,
                FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
            );
            CREATE TABLE IF NOT EXISTS campaign_results (
                campaign_id INTEGER,
                actual_posts INTEGER,
                actual_likes INTEGER,
                actual_sales INTEGER,
                actual_revenue REAL,
                accuracy_percent REAL,
                result_date TIMESTAMP,
                FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
            );
            CREATE TABLE IF NOT EXISTS algorithm_adjustments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT,
                adjustment_reason TEXT,
                old_params TEXT,
                new_params TEXT,
                created_at TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS algorithm_params (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT,
                param_name TEXT,
                param_value REAL,
                updated_at TIMESTAMP
            );
        ''')
    print("All tables created")

if __name__ == "__main__":
    create_tables()
