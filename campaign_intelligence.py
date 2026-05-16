import sqlite3
import json
import datetime
import numpy as np
import joblib
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "affiliate.db"

def get_db():
    return sqlite3.connect(DB_PATH)

class CampaignIntelligence:
    def __init__(self):
        self.model = None
        try:
            self.model = joblib.load('sales_prediction_model.pkl')
            print("Loaded sales prediction model")
        except:
            print("No model found, using default heuristics")
        self._init_default_params()

    def _init_default_params(self):
        with get_db() as conn:
            cur = conn.cursor()
            for platform in ['tiktok','facebook','shopee','lazada','zalo','alibaba']:
                cur.execute("SELECT 1 FROM algorithm_params WHERE platform=? AND param_name='post_factor'", (platform,))
                if not cur.fetchone():
                    cur.execute("INSERT INTO algorithm_params (platform, param_name, param_value, updated_at) VALUES (?,?,?,?)",
                                (platform, 'post_factor', 5.0, datetime.datetime.now()))
                    cur.execute("INSERT INTO algorithm_params (platform, param_name, param_value, updated_at) VALUES (?,?,?,?)",
                                (platform, 'like_per_post', 100.0, datetime.datetime.now()))
                    cur.execute("INSERT INTO algorithm_params (platform, param_name, param_value, updated_at) VALUES (?,?,?,?)",
                                (platform, 'conversion_rate', 0.02, datetime.datetime.now()))
            conn.commit()

    def get_param(self, platform, param_name):
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT param_value FROM algorithm_params WHERE platform=? AND param_name=?", (platform, param_name))
            row = cur.fetchone()
            return row[0] if row else None

    def set_param(self, platform, param_name, value):
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE algorithm_params SET param_value=?, updated_at=? WHERE platform=? AND param_name=?",
                        (value, datetime.datetime.now(), platform, param_name))
            conn.commit()

    def analyze_competitors(self, product_id):
        # Giữ nguyên code cũ (đã có)
        pass

    def suggest_strategy(self, product_id, platform, budget=100000):
        # Giữ nguyên code cũ
        pass

    def predict_campaign(self, campaign_id):
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT platform, budget FROM campaigns WHERE id=?", (campaign_id,))
            row = cur.fetchone()
            if not row:
                return None
            platform, budget = row
            cur.execute("SELECT product_id FROM campaign_products WHERE campaign_id=?", (campaign_id,))
            product_ids = [r[0] for r in cur.fetchall()]
            if not product_ids:
                return None
            total_price = 0
            for pid in product_ids:
                cur.execute("SELECT price FROM products WHERE id=?", (pid,))
                p = cur.fetchone()
                if p:
                    total_price += p[0]
            if self.model is not None:
                # Tạo dataframe cho dự đoán
                df = pd.DataFrame({
                    'budget': [budget],
                    'platform_' + platform: [1],
                    'predicted_posts': [int(budget / 10000 * self.get_param(platform, 'post_factor'))],
                    'predicted_likes': [int(budget / 10000 * self.get_param(platform, 'like_per_post'))],
                    'predicted_sales': [0],
                    'predicted_revenue': [0]
                })
                all_platforms = ['tiktok','facebook','shopee','lazada','zalo','alibaba']
                for p in all_platforms:
                    col = f'platform_{p}'
                    if col not in df.columns:
                        df[col] = 0
                feature_cols = ['budget'] + [f'platform_{p}' for p in all_platforms] + ['predicted_posts', 'predicted_likes', 'predicted_sales', 'predicted_revenue']
                df = df[feature_cols]
                try:
                    predicted_sales = self.model.predict(df)[0]
                    predicted_sales = max(1, int(predicted_sales))
                    predicted_revenue = total_price * predicted_sales * 0.1
                    predicted_posts = int(budget / 10000 * self.get_param(platform, 'post_factor'))
                    predicted_likes = int(budget / 10000 * self.get_param(platform, 'like_per_post'))
                except Exception as e:
                    print(f"Model error: {e}, using fallback")
                    predicted_posts = int(budget / 10000 * self.get_param(platform, 'post_factor'))
                    predicted_likes = predicted_posts * self.get_param(platform, 'like_per_post')
                    predicted_sales = int(predicted_likes * self.get_param(platform, 'conversion_rate'))
                    predicted_revenue = total_price * predicted_sales * 0.1
            else:
                predicted_posts = int(budget / 10000 * self.get_param(platform, 'post_factor'))
                predicted_likes = predicted_posts * self.get_param(platform, 'like_per_post')
                predicted_sales = int(predicted_likes * self.get_param(platform, 'conversion_rate'))
                predicted_revenue = total_price * predicted_sales * 0.1
            cur.execute("INSERT INTO campaign_predictions (campaign_id, predicted_posts, predicted_likes, predicted_sales, predicted_revenue, prediction_date) VALUES (?,?,?,?,?,?)",
                        (campaign_id, predicted_posts, predicted_likes, predicted_sales, predicted_revenue, datetime.datetime.now()))
            conn.commit()
            return {
                "predicted_posts": predicted_posts,
                "predicted_likes": predicted_likes,
                "predicted_sales": predicted_sales,
                "predicted_revenue": predicted_revenue
            }

    def evaluate_campaign(self, campaign_id, actual_posts, actual_likes, actual_sales, actual_revenue):
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT predicted_posts, predicted_likes, predicted_sales, predicted_revenue FROM campaign_predictions WHERE campaign_id=? ORDER BY prediction_date DESC LIMIT 1", (campaign_id,))
            pred = cur.fetchone()
            if not pred:
                return {"error": "No prediction found"}
            pred_posts, pred_likes, pred_sales, pred_rev = pred
            def acc(actual, predicted):
                if predicted == 0: return 0
                return min(100, (actual / predicted) * 100)
            acc_posts = acc(actual_posts, pred_posts)
            acc_likes = acc(actual_likes, pred_likes)
            acc_sales = acc(actual_sales, pred_sales)
            acc_rev = acc(actual_revenue, pred_rev)
            accuracy = (acc_posts + acc_likes + acc_sales + acc_rev) / 4
            cur.execute("INSERT INTO campaign_results (campaign_id, actual_posts, actual_likes, actual_sales, actual_revenue, accuracy_percent, result_date) VALUES (?,?,?,?,?,?,?)",
                        (campaign_id, actual_posts, actual_likes, actual_sales, actual_revenue, accuracy, datetime.datetime.now()))
            cur.execute("UPDATE campaigns SET status='completed' WHERE id=?", (campaign_id,))
            conn.commit()
            if accuracy < 90:
                self.optimize_algorithm(campaign_id)
            return {
                "accuracy_percent": accuracy,
                "need_optimization": accuracy < 90,
                "details": {"posts": acc_posts, "likes": acc_likes, "sales": acc_sales, "revenue": acc_rev}
            }

    def optimize_algorithm(self, campaign_id):
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("SELECT platform FROM campaigns WHERE id=?", (campaign_id,))
            platform = cur.fetchone()[0]
            cur.execute("SELECT actual_posts, actual_likes, actual_sales, actual_revenue FROM campaign_results WHERE campaign_id=?", (campaign_id,))
            actual = cur.fetchone()
            cur.execute("SELECT predicted_posts, predicted_likes, predicted_sales, predicted_revenue FROM campaign_predictions WHERE campaign_id=? ORDER BY prediction_date DESC LIMIT 1", (campaign_id,))
            pred = cur.fetchone()
            if not actual or not pred:
                return {"error": "Missing data"}
            post_factor_old = self.get_param(platform, 'post_factor')
            like_per_post_old = self.get_param(platform, 'like_per_post')
            conv_rate_old = self.get_param(platform, 'conversion_rate')
            def safe_ratio(actual, predicted):
                if predicted <= 0: return 1.0
                ratio = actual / predicted
                return max(0.5, min(2.0, ratio))
            ratio_posts = safe_ratio(actual[0], pred[0])
            ratio_likes = safe_ratio(actual[1], pred[1])
            ratio_sales = safe_ratio(actual[2], pred[2])
            new_post_factor = post_factor_old * ratio_posts
            new_like_per_post = like_per_post_old * ratio_likes
            new_conv_rate = conv_rate_old * ratio_sales
            new_post_factor = max(0.8, min(5.0, new_post_factor))
            new_like_per_post = max(20, min(500, new_like_per_post))
            new_conv_rate = max(0.005, min(0.1, new_conv_rate))
            self.set_param(platform, 'post_factor', new_post_factor)
            self.set_param(platform, 'like_per_post', new_like_per_post)
            self.set_param(platform, 'conversion_rate', new_conv_rate)
            print(f"[DEBUG] Updated {platform}.post_factor to {new_post_factor}")
            print(f"[DEBUG] Updated {platform}.like_per_post to {new_like_per_post}")
            print(f"[DEBUG] Updated {platform}.conversion_rate to {new_conv_rate}")
            cur.execute("INSERT INTO algorithm_adjustments (platform, adjustment_reason, old_params, new_params, created_at) VALUES (?,?,?,?,?)",
                        (platform, f"Optimization after campaign {campaign_id}",
                         json.dumps({"post_factor": post_factor_old, "like_per_post": like_per_post_old, "conversion_rate": conv_rate_old}),
                         json.dumps({"post_factor": new_post_factor, "like_per_post": new_like_per_post, "conversion_rate": new_conv_rate}),
                         datetime.datetime.now()))
            conn.commit()
            return {"message": "Algorithm parameters adjusted", "new_params": {"post_factor": new_post_factor, "like_per_post": new_like_per_post, "conversion_rate": new_conv_rate}}