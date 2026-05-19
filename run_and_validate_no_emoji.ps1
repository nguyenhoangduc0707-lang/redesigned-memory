$ErrorActionPreference = "Stop"

Write-Host "=== RUNNING PIPELINE ===" -ForegroundColor Cyan
python -m src.main --run-pipeline

Write-Host "`n=== CHECKING DATABASE ===" -ForegroundColor Cyan
python -c "import sqlite3; from src.config import DB_PATH; conn=sqlite3.connect(DB_PATH); cur=conn.cursor(); cur.execute('SELECT name, price, platform FROM products LIMIT 5'); rows=cur.fetchall(); [print(f'{r[0]} | {r[1]} VND | {r[2]}') for r in rows]; conn.close()"
