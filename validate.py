import sqlite3
import requests
import re
import json

def get_sample_products():
    conn = sqlite3.connect("affiliate.db")
    cur = conn.cursor()
    cur.execute("SELECT name, price, platform, url, strategy FROM products LIMIT 5")
    rows = cur.fetchall()
    conn.close()
    return [{"name": r[0], "price": r[1], "platform": r[2], "url": r[3], "strategy": r[4]} for r in rows]

def search_real_price(product_name):
    try:
        url = f"https://www.google.com/search?q={product_name}+giá"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        # Tìm giá VND
        match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s*(?:đ|vnđ|vnd|₫)', resp.text, re.IGNORECASE)
        if match:
            price_str = match.group(1).replace('.', '').replace(',', '.')
            return float(price_str)
        return None
    except:
        return None

def main():
    products = get_sample_products()
    if not products:
        print("Không có sản phẩm trong database. Hãy chạy pipeline trước.")
        return
    print("Báo cáo xác minh giá sản phẩm\n")
    for p in products:
        real_price = search_real_price(p['name'])
        print(f"Sản phẩm: {p['name']}")
        print(f"  - Giá AI: {p['price']} VND")
        print(f"  - Giá thực tế (ước lượng): {real_price if real_price else 'Không tìm thấy'} VND")
        if real_price:
            diff = abs(real_price - p['price']) / p['price'] * 100
            print(f"  - Độ chênh lệch: {diff:.1f}%")
            print(f"  - Kết luận: {'CHÍNH XÁC' if diff <= 30 else 'CẦN KIỂM TRA'}")
        else:
            print("  - Kết luận: Không xác định được")
        print()

if __name__ == "__main__":
    main()