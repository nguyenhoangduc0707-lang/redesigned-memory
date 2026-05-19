import sqlite3
conn = sqlite3.connect('ai_os.db')
conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, role TEXT)')
conn.execute('INSERT OR REPLACE INTO users (id, username, password_hash, role) VALUES (1, "admin", "admin", "admin")')
conn.commit()
conn.close()
print('✅ User admin created')
