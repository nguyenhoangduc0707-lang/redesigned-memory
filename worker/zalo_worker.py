# -*- coding: utf-8 -*-
from .base_worker import BaseWorker

class ZaloWorker(BaseWorker):
    def run(self):
        self.log(f"Zalo worker for campaign {self.campaign_id}")
        return {"status": "mock", "platform": "zalo", "message": "Zalo worker scaffold ready."}
