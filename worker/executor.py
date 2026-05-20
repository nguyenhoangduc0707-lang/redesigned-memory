# -*- coding: utf-8 -*-
from .facebook_worker import FacebookWorker
from .tiktok_worker import TikTokWorker
from .zalo_worker import ZaloWorker
from .shopee_worker import ShopeeWorker
from .lazada_worker import LazadaWorker
from .amazon_worker import AmazonWorker
from .tiktok_shop_api import TikTokShopAPIWorker

def run_worker(platform, campaign_id=None, caption="", media_path=None, content_type="text"):
    workers = {
        'facebook': FacebookWorker,
        'tiktok': TikTokWorker,
        'zalo': ZaloWorker,
        'shopee': ShopeeWorker,
        'lazada': LazadaWorker,
        'amazon': AmazonWorker,
        'tiktok_shop': TikTokShopAPIWorker,
    }
    worker_class = workers.get(platform.lower())
    if worker_class:
        if platform.lower() == "facebook":
            worker = worker_class(campaign_id, caption, media_path, content_type)
        else:
            worker = worker_class(campaign_id)
        return worker.run()
    else:
        return {"error": f"No worker for platform {platform}"}
