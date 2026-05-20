# -*- coding: utf-8 -*-
from .base_worker import BaseWorker

class AmazonWorker(BaseWorker):
    def run(self):
        self.log(f"Amazon worker for campaign {self.campaign_id}")
        return {"status": "mock", "platform": "amazon", "message": "Amazon affiliate worker scaffold ready."}
