# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

conn = sqlite3.connect('affiliate.db')
query = '''
SELECT c.budget, c.platform, cp.predicted_posts, cp.predicted_sales, cr.actual_sales
FROM campaigns c
JOIN campaign_predictions cp ON c.id = cp.campaign_id
JOIN campaign_results cr ON c.id = cr.campaign_id
WHERE c.status = 'completed'
'''
df = pd.read_sql_query(query, conn)
df = pd.get_dummies(df, columns=['platform'])
X = df.drop('actual_sales', axis=1)
y = df['actual_sales']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
joblib.dump(model, 'sales_prediction_model.pkl')
print('Model trained and saved.')



