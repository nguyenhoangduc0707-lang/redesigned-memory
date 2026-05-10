from concurrent.futures import ThreadPoolExecutor


class WorkerPool:
    def __init__(self, num_workers=4):
        self.executor = ThreadPoolExecutor(
            max_workers=num_workers
        )

    def submit(self, fn, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self):
        self.executor.shutdown(wait=True)