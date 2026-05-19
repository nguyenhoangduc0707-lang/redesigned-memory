# init_db.py
import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('ai_os.db')
c = conn.cursor()

# Tạo bảng campaigns
c.execute('''
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY,
        name TEXT,
        status TEXT
    )
''')

# Tạo bảng campaign_metrics
c.execute('''
    CREATE TABLE IF NOT EXISTS campaign_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER,
        platform TEXT,
        impressions INTEGER,
        clicks INTEGER,
        conversions INTEGER,
        revenue REAL,
        timestamp DATETIME
    )
''')

# Tạo bảng campaign_variants
c.execute('''
    CREATE TABLE IF NOT EXISTS campaign_variants (
        campaign_id INTEGER,
        variant_name TEXT,
        title TEXT,
        conversions INTEGER,
        impressions INTEGER
    )
''')

# Tạo bảng affiliate_clicks
c.execute('''
    CREATE TABLE IF NOT EXISTS affiliate_clicks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        click_id TEXT UNIQUE,
        campaign_id INTEGER,
        product_id INTEGER,
        user_ip TEXT,
        timestamp DATETIME,
        converted INTEGER DEFAULT 0
    )
''')

# Chèn dữ liệu mẫu
c.execute('INSERT OR IGNORE INTO campaigns VALUES (1, "Campaign A", "active")')
c.execute('INSERT OR IGNORE INTO campaigns VALUES (2, "Campaign B", "draft")')

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
c.execute('INSERT INTO campaign_metrics (campaign_id, platform, impressions, clicks, conversions, revenue, timestamp) VALUES (?,?,?,?,?,?,?)',
          (1, 'Facebook', 1200, 60, 6, 300.0, yesterday))
c.execute('INSERT INTO campaign_metrics (campaign_id, platform, impressions, clicks, conversions, revenue, timestamp) VALUES (?,?,?,?,?,?,?)',
          (1, 'TikTok', 900, 40, 4, 200.0, yesterday))
c.execute('INSERT INTO campaign_metrics (campaign_id, platform, impressions, clicks, conversions, revenue, timestamp) VALUES (?,?,?,?,?,?,?)',
          (2, 'Zalo', 500, 25, 2, 100.0, yesterday))

c.execute('INSERT INTO campaign_variants (campaign_id, variant_name, title, conversions, impressions) VALUES (1, "A", "Giảm 20%", 10, 1000)')
c.execute('INSERT INTO campaign_variants (campaign_id, variant_name, title, conversions, impressions) VALUES (1, "B", "Miễn phí ship", 15, 1200)')

conn.commit()
conn.close()
print('Database initialized with sample data')