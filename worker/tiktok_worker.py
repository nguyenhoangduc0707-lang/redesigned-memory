from .base_worker import BaseWorker

class TikTokWorker(BaseWorker):
    def run(self):
        self.log(f"TikTok worker for campaign {self.campaign_id} - Mock")
        return {"status": "mock", "message": "TikTok worker not implemented"}
