Write-Host "=== RUNNING PIPELINE ===" -ForegroundColor Cyan
python main.py --run-pipeline

Write-Host "`n=== CHECKING DATABASE ===" -ForegroundColor Cyan
python -c "
import sqlite3
conn = sqlite3.connect('affiliate.db')
cur = conn.cursor()
cur.execute('SELECT name, price, platform FROM products LIMIT 5')
rows = cur.fetchall()
for row in rows:
    print(f'{row[0]} | {row[1]} VND | {row[2]}')
conn.close()
"