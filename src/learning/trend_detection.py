# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from src.database import get_db
from datetime import datetime, timedelta

class TrendDetector:
    def __init__(self):
        self.trends = {}
    
    def analyze_hot_products(self, days=30):
        """Phân lo?i s?n ph?m hot"""
        with get_db() as conn:
            query = f"""
            SELECT 
                p.id,
                p.name,
                p.price,
                p.strategy,
                COUNT(po.id) as post_count,
                SUM(CASE WHEN po.status='published' THEN 1 ELSE 0 END) as published_count
            FROM products p
            LEFT JOIN posts po ON p.id = po.product_id
            GROUP BY p.id
            ORDER BY published_count DESC
            LIMIT 10
            """
            df = pd.read_sql_query(query, conn)
        
        if df.empty:
            return []
        
        hot_products = []
        for _, row in df.iterrows():
            if row['published_count'] > 5:
                level = "??????"
            elif row['published_count'] > 2:
                level = "????"
            elif row['published_count'] > 0:
                level = "??"
            else:
                level = "?"
            
            hot_products.append({
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'strategy': row['strategy'],
                'hot_level': level,
                'posts': row['post_count'],
                'published': row['published_count']
            })
        
        return hot_products
    
    def detect_platform_trends(self):
        """Phát hi?n xu hu?ng n?n t?ng"""
        with get_db() as conn:
            query = """
            SELECT 
                platform_target,
                COUNT(*) as total_posts,
                SUM(CASE WHEN status='published' THEN 1 ELSE 0 END) as published
            FROM posts
            GROUP BY platform_target
            """
            df = pd.read_sql_query(query, conn)
        
        if df.empty:
            return []
        
        total = df['total_posts'].sum()
        trends = []
        for _, row in df.iterrows():
            trends.append({
                'platform': row['platform_target'],
                'total_posts': row['total_posts'],
                'percentage': round(row['total_posts'] / total * 100, 1) if total > 0 else 0,
                'published_rate': round(row['published'] / row['total_posts'] * 100, 1) if row['total_posts'] > 0 else 0
            })
        
        return sorted(trends, key=lambda x: x['percentage'], reverse=True)
    
    def get_recommendations(self):
        """Ð? xu?t chi?n lu?c"""
        hot_products = self.analyze_hot_products()
        platform_trends = self.detect_platform_trends()
        
        recommendations = []
        
        if hot_products and hot_products[0]['hot_level'] != "?":
            recommendations.append({
                'type': 'product',
                'title': '?? S?N PH?M HOT',
                'content': f"Nên uu tiên {hot_products[0]['name']} - dã có {hot_products[0]['published']} bài dang thành công"
            })
        
        if platform_trends and platform_trends[0]['percentage'] > 30:
            recommendations.append({
                'type': 'platform',
                'title': '?? XU HU?NG N?N T?NG',
                'content': f"{platform_trends[0]['platform']} dang d?n d?u v?i {platform_trends[0]['percentage']}% bài dang"
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'info',
                'title': '?? G?I Ý',
                'content': 'T?o thêm chi?n d?ch d? có d? li?u phân tích xu hu?ng'
            })
        
        return recommendations

detector = TrendDetector()

if __name__ == "__main__":
    print("=" * 50)
    print("?? TREND DETECTION SYSTEM")
    print("=" * 50)
    
    hot = detector.analyze_hot_products()
    print(f"\n?? Hot products: {len(hot)}")
    for p in hot[:3]:
        print(f"   {p['hot_level']} {p['name']}: {p['published']} posts")
    
    trends = detector.detect_platform_trends()
    print(f"\n?? Platform trends:")
    for t in trends:
        print(f"   {t['platform']}: {t['percentage']}%")
    
    recs = detector.get_recommendations()
    print(f"\n?? Recommendations:")
    for r in recs:
        print(f"   {r['title']}: {r['content']}")



