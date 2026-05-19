# real_time_learning.py
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
import json

class RealTimeLearning:
    def __init__(self, db_path='ai_os.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                platform TEXT,
                impressions INTEGER,
                clicks INTEGER,
                conversions INTEGER,
                revenue REAL,
                timestamp DATETIME
            )
        ''')
        self.conn.commit()

    def analyze_trends(self, campaign_id=None):
        # Lấy dữ liệu gần đây
        query = "SELECT * FROM campaign_metrics"
        if campaign_id:
            query += f" WHERE campaign_id={campaign_id}"
        df = pd.read_sql_query(query, self.conn)
        if df.empty:
            return {}
        # Tính xu hướng đơn giản (slope)
        trends = {}
        for col in ['impressions', 'clicks', 'conversions', 'revenue']:
            if col in df.columns:
                x = np.arange(len(df))
                y = df[col].values
                slope = np.polyfit(x, y, 1)[0] if len(x) > 1 else 0
                trends[col] = slope
        return trends

    def suggest_adjustments(self, campaign_id):
        trends = self.analyze_trends(campaign_id)
        suggestions = []
        if trends.get('conversions', 0) < 0:
            suggestions.append("Giảm ngân sách, thay đổi nội dung quảng cáo.")
        if trends.get('clicks', 0) < 0:
            suggestions.append("Cải thiện tiêu đề và hình ảnh.")
        if trends.get('revenue', 0) < 0:
            suggestions.append("Kiểm tra lại link affiliate và landing page.")
        return suggestions

    def auto_adjust(self, campaign_id):
        suggestions = self.suggest_adjustments(campaign_id)
        # Ghi log
        with open('auto_adjust_log.json', 'a') as f:
            f.write(json.dumps({
                'timestamp': str(datetime.now()),
                'campaign_id': campaign_id,
                'suggestions': suggestions
            }) + '\n')
        return suggestions

if __name__ == "__main__":
    rl = RealTimeLearning()
    # Ví dụ: điều chỉnh campaign 1
    print(rl.auto_adjust(1))