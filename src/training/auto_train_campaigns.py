# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
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
    cur.execute("SELECT id, name, price FROM products LIMIT 5")  # Chá»n 5 sáº£n pháº©m Ä‘áº§u
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
    # Gá»i hÃ m dá»± Ä‘oÃ¡n trong campaign_intelligence (cáº§n import)
    from src.campaign_intelligence import CampaignIntelligence
    ci = CampaignIntelligence()
    return ci.predict_campaign(camp_id)

def evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue):
    from src.campaign_intelligence import CampaignIntelligence
    ci = CampaignIntelligence()
    return ci.evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue)

def simulate_results(predicted_sales):
    """MÃ´ phá»ng káº¿t quáº£ thá»±c táº¿ xoay quanh dá»± Ä‘oÃ¡n vá»›i sai sá»‘ ngáº«u nhiÃªn"""
    actual_sales = max(0, int(predicted_sales * random.uniform(0.5, 1.5)))
    actual_revenue = actual_sales * random.randint(50000, 200000)
    actual_posts = max(1, int(actual_sales * random.uniform(2, 5)))
    actual_likes = actual_posts * random.randint(20, 200)
    return actual_posts, actual_likes, actual_sales, actual_revenue

def main():
    products = get_products()
    if not products:
        print("KhÃ´ng cÃ³ sáº£n pháº©m. HÃ£y cháº¡y main.py --run-pipeline trÆ°á»›c.")
        return

    platforms = ['facebook', 'tiktok', 'shopee', 'lazada']
    budgets = [50000, 100000, 200000, 500000]
    goals = ['engagement', 'sales', 'reach']

    # Táº¡o 30 chiáº¿n dá»‹ch má»›i
    for i in range(30):
        product = random.choice(products)
        product_id, product_name, product_price = product
        platform = random.choice(platforms)
        budget = random.choice(budgets)
        goal = random.choice(goals)
        name = f"AutoCampaign_{i+1}_{platform}_{int(time.time())}"
        camp_id = create_campaign(name, platform, budget, goal, product_id)
        print(f"ÄÃ£ táº¡o campaign {camp_id}: {name}")

        # Dá»± Ä‘oÃ¡n
        pred = predict_campaign(camp_id)
        if not pred:
            print(f"  Dá»± Ä‘oÃ¡n tháº¥t báº¡i cho campaign {camp_id}")
            continue
        predicted_sales = pred.get('predicted_sales', 1)
        print(f"  Dá»± Ä‘oÃ¡n: {predicted_sales} sales")

        # MÃ´ phá»ng káº¿t quáº£ thá»±c táº¿
        actual_posts, actual_likes, actual_sales, actual_revenue = simulate_results(predicted_sales)
        print(f"  MÃ´ phá»ng: {actual_sales} sales (posts={actual_posts}, likes={actual_likes}, rev={actual_revenue})")

        # ÄÃ¡nh giÃ¡ vÃ  tá»‘i Æ°u
        result = evaluate_campaign(camp_id, actual_posts, actual_likes, actual_sales, actual_revenue)
        acc = result.get('accuracy_percent', 0)
        print(f"  Äá»™ chÃ­nh xÃ¡c: {acc:.2f}% - {'ÄÃ£ tá»‘i Æ°u' if acc < 90 else 'Táº¡m á»•n'}")

        # Chá» má»™t chÃºt Ä‘á»ƒ trÃ¡nh quÃ¡ táº£i database
        time.sleep(0.5)

    print("\n=== HOÃ€N Táº¤T ===")
    print("ÄÃ£ táº¡o vÃ  Ä‘Ã¡nh giÃ¡ 30 chiáº¿n dá»‹ch. Thuáº­t toÃ¡n Ä‘Ã£ Ä‘Æ°á»£c tá»‘i Æ°u liÃªn tá»¥c.")
    print("Báº¡n cÃ³ thá»ƒ cháº¡y láº¡i script nÃ y nhiá»u láº§n Ä‘á»ƒ tÄƒng Ä‘á»™ chÃ­nh xÃ¡c.")

if __name__ == "__main__":
    main()



