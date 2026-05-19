# Trong worker/pool.py
from worker.fb_executor import FacebookAutomationWorker

class WorkerPool:
    def __init__(self, event_bus, registry):
        self.workers = {}
        # ... code khởi tạo
        self._register_worker("facebook_auto", FacebookAutomationWorker)

    def _register_worker(self, name, worker_class):
        worker = worker_class(f"{name}_{id}", self.event_bus, self.registry)
        self.workers[name] = worker
        asyncio.create_task(worker.initialize())
