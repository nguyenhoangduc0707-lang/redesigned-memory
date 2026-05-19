from .base_worker import BaseWorker

class ShopeeWorker(BaseWorker):
    def run(self):
        self.log(f"Shopee worker for campaign {self.campaign_id} - Mock")
        return {"status": "mock", "message": "Shopee worker not implemented"}
