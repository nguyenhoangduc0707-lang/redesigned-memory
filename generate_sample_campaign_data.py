import sqlite3
import random
import datetime

conn = sqlite3.connect('affiliate.db')
cur = conn.cursor()
platforms = ['facebook','tiktok','shopee','lazada']
for i in range(10):
    name = f"Test Campaign {i+1}"
    platform = random.choice(platforms)
    start = datetime.date.today() - datetime.timedelta(days=random.randint(1,30))
    end = start + datetime.timedelta(days=7)
    budget = random.randint(50000,500000)
    goal = random.choice(['engagement','sales','reach'])
    cur.execute("INSERT INTO campaigns (name, platform, start_date, end_date, budget, goal, status) VALUES (?,?,?,?,?,?,'completed')",
                (name, platform, start, end, budget, goal))
    camp_id = cur.lastrowid
    predicted_posts = random.randint(5,20)
    predicted_likes = predicted_posts * random.randint(50,200)
    predicted_sales = random.randint(1,10)
    predicted_revenue = predicted_sales * random.randint(50000,200000)
    cur.execute("INSERT INTO campaign_predictions (campaign_id, predicted_posts, predicted_likes, predicted_sales, predicted_revenue, prediction_date) VALUES (?,?,?,?,?,?)",
                (camp_id, predicted_posts, predicted_likes, predicted_sales, predicted_revenue, datetime.datetime.now()))
    actual_posts = int(predicted_posts * random.uniform(0.7,1.3))
    actual_likes = int(predicted_likes * random.uniform(0.6,1.4))
    actual_sales = int(predicted_sales * random.uniform(0.5,1.5))
    actual_revenue = predicted_revenue * random.uniform(0.5,1.5)
    accuracy = random.uniform(50,95)
    cur.execute("INSERT INTO campaign_results (campaign_id, actual_posts, actual_likes, actual_sales, actual_revenue, accuracy_percent, result_date) VALUES (?,?,?,?,?,?,?)",
                (camp_id, actual_posts, actual_likes, actual_sales, actual_revenue, accuracy, datetime.datetime.now()))
conn.commit()
conn.close()
print("Created 10 sample campaigns")
