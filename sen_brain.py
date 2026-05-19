import joblib
import numpy as np
from src.learning.sentiment_analyzer import SentimentAnalyzer
from src.ml.algo_simulator import AlgoSimulator, CampaignScenario

class SEN_Brain:
    def __init__(self, model_path='models/sales_prediction_model.pkl'):
        self.model = joblib.load(model_path)
        self.sentiment = SentimentAnalyzer()
        self.algo = AlgoSimulator()
        self.feature_names = getattr(self.model, 'feature_names_in_', None)
        print("🧠 SEN Brain initialized (LinearRegression + Sentiment + Algo)")

    def predict_sales(self, budget, predicted_posts, predicted_sales,
                      platform_facebook=1, platform_lazada=1, platform_shopee=1, platform_tiktok=1):
        if self.feature_names is not None:
            features = np.array([budget, predicted_posts, predicted_sales,
                                 platform_facebook, platform_lazada, platform_shopee, platform_tiktok]).reshape(1, -1)
        else:
            features = np.array([budget, predicted_posts, predicted_sales]).reshape(1, -1)
        return float(self.model.predict(features)[0])

    def analyze_sentiment(self, text):
        return self.sentiment.score(text)

    def optimize_campaign(self, budget, post_count, commission_rate=0.1,
                          conversion_rate=0.02, avg_order_value=250000):
        scenario = CampaignScenario(budget=budget, post_count=post_count, commission_rate=commission_rate)
        scenario.conversion_rate = conversion_rate
        scenario.avg_order_value = avg_order_value
        return self.algo.simulate(scenario)

    def quantum_optimize(self, code: str):
        from src.quantum.planner import generate_improved_versions
        try:
            return generate_improved_versions(code)
        except Exception as e:
            return [{"error": str(e)}]

    def safe_execute(self, code: str, input_data: dict = None):
        from src.execution.sandbox import run_in_sandbox
        try:
            return run_in_sandbox(code, input_data)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def check_affiliate_policy(self, user_id: str, context: str) -> bool:
        from src.security.policy_checker import can_send_link
        return can_send_link(user_id, context)

default_brain = SEN_Brain()
