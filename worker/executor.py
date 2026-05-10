from atomic_base import AtomicBase

class Executor(AtomicBase):
    def execute(self, task=None):
        return f"Executing {task}"
