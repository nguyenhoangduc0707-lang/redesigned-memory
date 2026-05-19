from .base_worker import BaseWorker

class ZaloWorker(BaseWorker):
    def run(self):
        self.log(f"Zalo worker for campaign {self.campaign_id} - Mock")
        return {"status": "mock", "message": "Zalo worker not implemented"}
