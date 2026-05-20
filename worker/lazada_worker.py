# -*- coding: utf-8 -*-
from .base_worker import BaseWorker

class LazadaWorker(BaseWorker):
    def run(self):
        self.log(f"Lazada worker for campaign {self.campaign_id}")
        return {"status": "mock", "platform": "lazada", "message": "Lazada integration scaffold ready."}
