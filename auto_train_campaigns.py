import sqlite3
import random
import datetime
import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

DB_PATH = 'affiliate.db'

def get_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products LIMIT 5")  # Chọn 5 sản phẩm đầu
    products = cur.fetchall()
    conn.close()
    return products

def create_campaign(name, platform, budget, goal, product_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    start = datetime.date.today()
    end = start + datetime.timedelta(days=7)
    cur.execute("""
        INSERT INTO campaigns (name, platform, start_date, end_date, budget, goal, status)
        VALUES (?,?,?,?,?,?,'running')
    """, (name, platform, start, end, budget, goal))
    camp_id = cur.lastrowid
    cur.execute("INSERT INTO campaign_products (campaign_id, product_id) VALUES (?,?)", (camp_id, product_id))
    conn.commit()
    conn.close()
    return camp_id

def predict_campaign(camp_id):
    # Gọi hàm dự đoán trong campaign_intelligence (cần import)
    from campaign_intelligence import CampaignIntelligence
    ci = CampaignIntelligence()
    return ci.predict_campaign(camp_id)

def evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue):
    from campaign_intelligence import CampaignIntelligence
    ci = CampaignIntelligence()
    return ci.evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue)

def simulate_results(predicted_sales):
    """Mô phỏng kết quả thực tế xoay quanh dự đoán với sai số ngẫu nhiên"""
    actual_sales = max(0, int(predicted_sales * random.uniform(0.5, 1.5)))
    actual_revenue = actual_sales * random.randint(50000, 200000)
    actual_posts = max(1, int(actual_sales * random.uniform(2, 5)))
    actual_likes = actual_posts * random.randint(20, 200)
    return actual_posts, actual_likes, actual_sales, actual_revenue

def main():
    products = get_products()
    if not products:
        print("Không có sản phẩm. Hãy chạy main.py --run-pipeline trước.")
        return

    platforms = ['facebook', 'tiktok', 'shopee', 'lazada']
    budgets = [50000, 100000, 200000, 500000]
    goals = ['engagement', 'sales', 'reach']

    # Tạo 30 chiến dịch mới
    for i in range(30):
        product = random.choice(products)
        product_id, product_name, product_price = product
        platform = random.choice(platforms)
        budget = random.choice(budgets)
        goal = random.choice(goals)
        name = f"AutoCampaign_{i+1}_{platform}_{int(time.time())}"
        camp_id = create_campaign(name, platform, budget, goal, product_id)
        print(f"Đã tạo campaign {camp_id}: {name}")

        # Dự đoán
        pred = predict_campaign(camp_id)
        if not pred:
            print(f"  Dự đoán thất bại cho campaign {camp_id}")
            continue
        predicted_sales = pred.get('predicted_sales', 1)
        print(f"  Dự đoán: {predicted_sales} sales")

        # Mô phỏng kết quả thực tế
        actual_posts, actual_likes, actual_sales, actual_revenue = simulate_results(predicted_sales)
        print(f"  Mô phỏng: {actual_sales} sales (posts={actual_posts}, likes={actual_likes}, rev={actual_revenue})")

        # Đánh giá và tối ưu
        result = evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue)
        acc = result.get('accuracy_percent', 0)
        print(f"  Độ chính xác: {acc:.2f}% - {'Đã tối ưu' if acc < 90 else 'Tạm ổn'}")

        # Chờ một chút để tránh quá tải database
        time.sleep(0.5)

    print("\n=== HOÀN TẤT ===")
    print("Đã tạo và đánh giá 30 chiến dịch. Thuật toán đã được tối ưu liên tục.")
    print("Bạn có thể chạy lại script này nhiều lần để tăng độ chính xác.")

if __name__ == "__main__":
    main()