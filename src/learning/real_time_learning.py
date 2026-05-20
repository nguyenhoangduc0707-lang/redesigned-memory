# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import joblib
import pandas as pd
import numpy as np
from src.database import get_db
from collections import deque
import datetime
import subprocess
import os

class RealTimeLearner:
    def __init__(self, max_history=100):
        self.max_history = max_history
        self.recent_data = deque(maxlen=max_history)
        self.model = None
        self.load_model()
    
    def load_model(self):
        try:
            if os.path.exists('models/sales_prediction_model.pkl'):
                self.model = joblib.load('models/sales_prediction_model.pkl')
                print("? Real-time learner loaded")
            else:
                print("?? No model found, will collect data first")
        except Exception as e:
            print(f"?? Cannot load model: {e}")
    
    def add_campaign_result(self, campaign_id):
         # -*- coding: utf-8 -*-
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.budget, c.platform, c.goal,
                       cr.actual_posts, cr.actual_sales, cr.actual_revenue
                FROM campaigns c
                LEFT JOIN campaign_results cr ON c.id = cr.campaign_id
                WHERE c.id = ? AND c.status = 'completed'
            """, (campaign_id,))
            row = cur.fetchone()
            
            if row:
                self.recent_data.append({
                    'timestamp': datetime.datetime.now(),
                    'budget': row[0],
                    'platform': row[1],
                    'goal': row[2],
                    'actual_posts': row[3],
                    'actual_sales': row[4],
                    'actual_revenue': row[5]
                })
                print(f"? Added campaign {campaign_id} to learning queue")
                
                if len(self.recent_data) >= 10:
                    self.auto_retrain()
    
    def auto_retrain(self):
        """T? d?ng retrain model v?i d? li?u m?i"""
        print("?? Auto-retraining with new data...")
        try:
            subprocess.run(["python", "retrain_model.py"], capture_output=True)
            self.load_model()
        except Exception as e:
            print(f"?? Auto-retrain failed: {e}")
    
    def predict_sales(self, budget, platform, goal):
        """D? do�n doanh số"""
        if self.model is None:
            return {"error": "Model not ready", "predicted_sales": 0}
        
        try:
            # M� h�a platform v� goal
            platform_map = {'facebook':0, 'tiktok':1, 'zalo':2, 'shopee':3, 'lazada':4}
            goal_map = {'sales':0, 'traffic':1, 'awareness':2}
            
            platform_encoded = platform_map.get(platform, 0)
            goal_encoded = goal_map.get(goal, 0)
            
            features = [[budget, platform_encoded, goal_encoded]]
            predicted_sales = self.model.predict(features)[0]
            
            return {
                "predicted_sales": int(predicted_sales),
                "confidence": min(100, len(self.recent_data) * 5),
                "samples_used": len(self.recent_data)
            }
        except Exception as e:
            return {"error": str(e), "predicted_sales": 0}

# Kh?i t?o global instance
learner = RealTimeLearner()

if __name__ == "__main__":
    print("Real-time learning system ready")
    print(f"Collected samples: {len(learner.recent_data)}")


