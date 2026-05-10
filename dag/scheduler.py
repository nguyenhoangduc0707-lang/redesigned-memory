from atomic_base import AtomicBase

class Scheduler(AtomicBase):
    def execute(self, task=None):
        return {"schedule": f"Task {task} scheduled"}
