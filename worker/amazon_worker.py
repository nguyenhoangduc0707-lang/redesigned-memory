from .base_worker import BaseWorker


class AmazonWorker(BaseWorker):
    def run(self):
        self.log(f"Amazon worker for campaign {self.campaign_id}")
        return {
            "status": "mock",
            "platform": "amazon",
            "message": "Amazon affiliate worker scaffold ready; PA-API credentials and associate tag required.",
        }
