# -*- coding: utf-8 -*-
from .base_worker import BaseWorker

class ShopeeWorker(BaseWorker):
    def run(self):
        self.log(f"Shopee worker for campaign {self.campaign_id}")
        return {"status": "mock", "platform": "shopee", "message": "Shopee worker scaffold ready."}
