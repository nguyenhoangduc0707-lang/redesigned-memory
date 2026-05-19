POSITIVE_WORDS = {
    "good",
    "great",
    "best",
    "love",
    "like",
    "tot",
    "hay",
    "re",
    "dep",
    "nhanh",
    "chat luong",
}

NEGATIVE_WORDS = {
    "bad",
    "poor",
    "hate",
    "expensive",
    "slow",
    "te",
    "kem",
    "loi",
    "chan",
    "dat",
}


class SentimentAnalyzer:
    def score(self, text):
        normalized = (text or "").lower()
        positive = sum(1 for word in POSITIVE_WORDS if word in normalized)
        negative = sum(1 for word in NEGATIVE_WORDS if word in normalized)
        total = positive + negative
        score = 0 if total == 0 else (positive - negative) / total
        if score > 0.2:
            label = "positive"
        elif score < -0.2:
            label = "negative"
        else:
            label = "neutral"
        return {"label": label, "score": round(score, 3), "positive_hits": positive, "negative_hits": negative}

    def summarize(self, texts):
        results = [self.score(text) for text in texts]
        if not results:
            return {"label": "neutral", "score": 0, "count": 0}
        avg = sum(item["score"] for item in results) / len(results)
        if avg > 0.2:
            label = "positive"
        elif avg < -0.2:
            label = "negative"
        else:
            label = "neutral"
        return {"label": label, "score": round(avg, 3), "count": len(results), "items": results}
