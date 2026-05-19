# dashboard_api.py (phiên bản an toàn)
from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Dashboard is running. Use /api/campaigns"

@app.route('/api/campaigns')
def get_campaigns():
    conn = sqlite3.connect('ai_os.db')
    c = conn.cursor()
    try:
        c.execute("SELECT id, name, status FROM campaigns")
        rows = c.fetchall()
        return jsonify([{"id": r[0], "name": r[1], "status": r[2]} for r in rows])
    except sqlite3.OperationalError:
        return jsonify([])
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
