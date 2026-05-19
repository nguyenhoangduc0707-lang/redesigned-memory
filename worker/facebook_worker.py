import os

import requests
from dotenv import load_dotenv

from .base_worker import BaseWorker

load_dotenv()


def post_to_facebook(message, media_path=None, content_type="text"):
    access_token = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    if not access_token:
        return {"status": "error", "message": "Missing Facebook access token"}
    if not page_id:
        return {"status": "error", "message": "Missing FACEBOOK_PAGE_ID"}

    endpoint = "videos" if content_type == "video" and media_path else "feed"
    url = f"https://graph.facebook.com/{page_id}/{endpoint}"
    payload = {"access_token": access_token}
    files = None

    if endpoint == "videos":
        payload["description"] = message
        files = {"source": open(media_path, "rb")}
    else:
        payload["message"] = message

    try:
        response = requests.post(url, data=payload, files=files, timeout=30)
        return response.json()
    finally:
        if files:
            files["source"].close()


class FacebookWorker(BaseWorker):
    def __init__(self, campaign_id=None, caption="", media_path=None, content_type="text"):
        super().__init__(campaign_id)
        self.caption = caption or ""
        self.media_path = media_path
        self.content_type = content_type

    def run(self):
        self.log(f"Facebook worker for campaign {self.campaign_id}")
        result = post_to_facebook(self.caption, self.media_path, self.content_type)
        return {"status": "completed", "platform": "facebook", "result": result}


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 2 and sys.argv[1] == "--post":
        print(post_to_facebook(sys.argv[2]))
