import sqlite3
conn = sqlite3.connect('affiliate.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    competitor_name TEXT,
    price REAL,
    likes INTEGER,
    sales INTEGER,
    platform TEXT,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id)
);
''')
conn.commit()
conn.close()
print('Table competitors created successfully')
