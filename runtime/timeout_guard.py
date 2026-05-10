import threading


class TimeoutGuard:
    def run_with_timeout(self, fn, timeout=30):
        result = {
            "done": False,
            "value": None,
            "error": None
        }

        def target():
            try:
                result["value"] = fn()
            except Exception as e:
                result["error"] = e

            result["done"] = True

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)

        if not result["done"]:
            raise TimeoutError("Task timeout")

        if result["error"]:
            raise result["error"]

        return result["value"]