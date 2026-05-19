# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import sqlite3
import requests
import time
import json

def get_shopee_similar(product_name):
    url = f"https://shopee.vn/api/v4/search/search_items?keyword={product_name}&limit=5"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get('items', [])
            result = []
            for item in items:
                name = item.get('name', '')
                price = item.get('price', 0) / 100000
                sold = item.get('historical_sold', 0)
                result.append({
                    'name': name[:50],
                    'price': int(price),
                    'sales': sold,
                    'platform': 'shopee'
                })
            return result
    except Exception as e:
        print(f"Error: {e}")
    return []

def update_competitors(product_id, product_name):
    competitors = get_shopee_similar(product_name)
    conn = sqlite3.connect('affiliate.db')
    cur = conn.cursor()
    for comp in competitors:
        cur.execute('''
            INSERT INTO competitors (product_id, competitor_name, price, sales, platform)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, comp['name'], comp['price'], comp['sales'], comp['platform']))
    conn.commit()
    conn.close()
    print(f"Added {len(competitors)} competitors for product {product_id}")

# Láº¥y danh sÃ¡ch sáº£n pháº©m tá»« database
conn = sqlite3.connect('affiliate.db')
cur = conn.cursor()
cur.execute("SELECT id, name FROM products LIMIT 10")
rows = cur.fetchall()
conn.close()

for pid, pname in rows:
    update_competitors(pid, pname)
    time.sleep(1)



