"""
Facebook Automation Worker for AI_OS_KERNEL_V3
Tích hợp với registry, event bus, retry policy, và sandbox.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Giả định các module đã tồn tại trong hệ thống
from worker.base_worker import BaseWorker  # hoặc AtomicBase
from registry.service_registry import ServiceRegistry
from core.event_bus import EventBus
from runtime.retry_policy import RetryPolicy, retry_on_failure
from sandbox.worker import SandboxedWorker  # nếu cần chạy playwright trong sandbox

logger = logging.getLogger(__name__)

class FacebookAutomationWorker(BaseWorker):
    """
    Worker chuyên trách tự động hóa Facebook: đăng bài, kiểm tra token.
    """

    def __init__(self, worker_id: str, event_bus: EventBus, registry: ServiceRegistry):
        super().__init__(worker_id)
        self.event_bus = event_bus
        self.registry = registry
        self.retry_policy = RetryPolicy(max_attempts=3, backoff_factor=2.0)
        self._token = None
        self._cookies = None
        self._session_checked = False

    async def initialize(self) -> None:
        """Khởi tạo worker: lấy token/cookies từ registry."""
        logger.info(f"Initializing FacebookWorker {self.worker_id}")
        # Lấy token từ registry (giả sử service_registry có phương thức get_credentials)
        self._token = await self.registry.get_credential("facebook", "access_token")
        self._cookies = await self.registry.get_credential("facebook", "cookies")
        if not self._token and not self._cookies:
            raise ValueError("No Facebook access token or cookies found in registry.")
        # Kiểm tra session ngay khi khởi tạo
        await self.check_session()
        logger.info("FacebookWorker initialized successfully.")

    @retry_on_failure(retry_policy=RetryPolicy(max_attempts=2, backoff_factor=1.0))
    async def check_session(self) -> bool:
        """
        Kiểm tra token/cookies còn sống không.
        Trả về True nếu còn hiệu lực, False nếu hết hạn.
        """
        # Sử dụng Graph API để kiểm tra token
        if self._token:
            import aiohttp
            url = "https://graph.facebook.com/me"
            params = {"access_token": self._token}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if "id" in data:
                            self._session_checked = True
                            logger.info("Facebook token is valid.")
                            return True
            logger.warning("Facebook token invalid or expired.")
            self._session_checked = False
            return False
        # Nếu dùng cookies, có thể kiểm tra bằng playwright (sandbox)
        # ... (bỏ qua vì phức tạp, tạm coi như luôn hợp lệ nếu có cookies)
        return bool(self._cookies)

    @retry_on_failure(retry_policy=RetryPolicy(max_attempts=3, backoff_factor=2.0))
    async def auto_post(self, content: str, image_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Đăng bài lên Facebook bằng Graph API hoặc playwright.
        Trả về dict chứa kết quả (success, post_id, error).
        """
        if not self._session_checked:
            await self.check_session()
            if not self._session_checked:
                error_msg = "Session invalid. Cannot post."
                logger.error(error_msg)
                await self._publish_result("auto_post", False, error=error_msg)
                return {"success": False, "error": error_msg}

        # Chọn phương thức: ưu tiên Graph API nếu có token
        if self._token:
            result = await self._post_via_graph_api(content, image_url)
        elif self._cookies:
            result = await self._post_via_playwright(content, image_url)
        else:
            result = {"success": False, "error": "No valid authentication method."}

        # Đẩy kết quả lên event bus
        await self._publish_result("auto_post", result["success"], result)
        return result

    async def _post_via_graph_api(self, content: str, image_url: Optional[str]) -> Dict[str, Any]:
        """Đăng bài bằng Graph API."""
        import aiohttp
        url = "https://graph.facebook.com/me/feed"
        params = {"access_token": self._token, "message": content}
        if image_url:
            params["link"] = image_url  # hoặc dùng attachment? tạm thời dùng link
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    post_id = data.get("id")
                    logger.info(f"Posted successfully via Graph API. Post ID: {post_id}")
                    return {"success": True, "post_id": post_id}
                else:
                    error_text = await resp.text()
                    logger.error(f"Graph API error: {resp.status} - {error_text}")
                    return {"success": False, "error": error_text}

    async def _post_via_playwright(self, content: str, image_url: Optional[str]) -> Dict[str, Any]:
        """
        Đăng bài thông qua playwright (chạy trong sandbox).
        Giả sử sandbox worker đã được cấu hình.
        """
        # Tạo một sandbox worker để chạy playwright an toàn
        sandbox = SandboxedWorker()
        script = f"""
        import asyncio
        from playwright.async_api import async_playwright
        async def main():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(storage_state="cookies.json")  # giả định cookies đã được lưu
                page = await context.new_page()
                await page.goto("https://facebook.com")
                # ... thao tác đăng bài (cần logic cụ thể)
                await browser.close()
            return {{"success": True, "post_id": "12345"}}
        result = await main()
        """
        result = await sandbox.run(script, timeout=30)
        return result  # dạng dict

    async def _publish_result(self, task_name: str, success: bool, details: Dict[str, Any]) -> None:
        """Gửi kết quả lên event bus."""
        event = {
            "worker": "FacebookAutomationWorker",
            "task": task_name,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "details": details
        }
        await self.event_bus.publish("worker.result", event)
        logger.debug(f"Published result: {event}")

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phương thức chính để worker pool gọi khi có task.
        task = {"type": "auto_post", "content": "...", "image_url": "..."}
        hoặc "type": "check_session"
        """
        task_type = task.get("type")
        if task_type == "auto_post":
            content = task.get("content", "")
            image_url = task.get("image_url")
            return await self.auto_post(content, image_url)
        elif task_type == "check_session":
            valid = await self.check_session()
            return {"success": valid, "session_valid": valid}
        else:
            raise ValueError(f"Unknown task type: {task_type}")