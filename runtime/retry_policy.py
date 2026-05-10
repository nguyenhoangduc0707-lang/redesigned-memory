class RetryPolicy:
    def __init__(self, retries=3):
        self.retries = retries

    def should_retry(self, attempt):
        return attempt < self.retries