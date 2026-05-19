import os

import requests

from .base_worker import BaseWorker


class TikTokShopAPIWorker(BaseWorker):
    def __init__(self, campaign_id=None, access_token=None, business_id=None):
        super().__init__(campaign_id)
        self.access_token = access_token or os.getenv("TIKTOK_ACCESS_TOKEN")
        self.business_id = business_id or os.getenv("TIKTOK_BUSINESS_ID")

    def run(self):
        self.log(f"TikTok Shop API worker for campaign {self.campaign_id}")
        if not self.access_token or not self.business_id:
            return {
                "status": "missing_credentials",
                "platform": "tiktok_shop",
                "message": "Missing TIKTOK_ACCESS_TOKEN or TIKTOK_BUSINESS_ID.",
            }
        return {
            "status": "ready",
            "platform": "tiktok_shop",
            "business_id": self.business_id,
            "message": "Credentials present. Implement endpoint-specific calls after product/catalog mapping is confirmed.",
        }

    def get(self, url, params=None):
        if not self.access_token:
            raise RuntimeError("Missing TIKTOK_ACCESS_TOKEN")
        response = requests.get(
            url,
            params=params or {},
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
