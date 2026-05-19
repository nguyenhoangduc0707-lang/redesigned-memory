from src.agents import Agent
from src.learning.sentiment_analyzer import SentimentAnalyzer
from src.ml.algo_simulator import simulate_campaign
from worker.executor import run_worker


def test_marketplace_workers_smoke():
    assert run_worker("lazada", 1)["platform"] == "lazada"
    assert run_worker("amazon", 1)["platform"] == "amazon"
    assert run_worker("tiktok_shop", 1)["platform"] == "tiktok_shop"


def test_algo_simulator_smoke():
    result = simulate_campaign(budget=1000, post_count=10, conversion_rate=0.02, avg_order_value=100)
    assert result["reach"] > 0
    assert "roi" in result


def test_sentiment_analyzer_smoke():
    result = SentimentAnalyzer().score("san pham tot va giao nhanh")
    assert result["label"] == "positive"


def test_agent_fallback_shape_without_keys():
    class LocalFail:
        def ask(self, prompt, system_prompt=None):
            return {"ok": False, "source": "local", "error": "offline", "answer": None}

    class FallbackOk:
        def ask(self, prompt, system_prompt=None):
            return {"ok": True, "source": "test", "error": None, "answer": "ok"}

    result = Agent("test", local_controller=LocalFail(), fallback=FallbackOk()).run("task")
    assert result["source"] == "test"
    assert result["answer"] == "ok"
