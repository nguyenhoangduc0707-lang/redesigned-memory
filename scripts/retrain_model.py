import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from src.database import get_db


def load_training_data():
    with get_db() as conn:
        query = """
            SELECT
                c.budget,
                c.platform,
                c.goal,
                cr.actual_posts,
                cr.actual_sales,
                cr.actual_revenue
            FROM campaigns c
            LEFT JOIN campaign_results cr ON c.id = cr.campaign_id
            WHERE c.status = 'completed' AND cr.actual_sales IS NOT NULL
        """
        df = pd.read_sql_query(query, conn)

    if len(df) < 5:
        print(f"Only {len(df)} samples. Need at least 5 for training.")
        return None

    df["platform_encoded"] = df["platform"].astype("category").cat.codes
    df["goal_encoded"] = df["goal"].astype("category").cat.codes

    feature_cols = ["budget", "platform_encoded", "goal_encoded"]
    return df[feature_cols], df["actual_sales"], feature_cols


def train_model(x, y, feature_names):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"MAE: {mae:.2f}, R2: {r2:.2f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/sales_prediction_model.pkl")
    print("Model saved to models/sales_prediction_model.pkl")
    return model


def main():
    data = load_training_data()
    if data is None:
        print("Not enough data. Please add more completed campaigns.")
        return

    x, y, feature_names = data
    print(f"Training data: {len(x)} samples")
    train_model(x, y, feature_names)
    print("Retraining complete")


if __name__ == "__main__":
    main()
