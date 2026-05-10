class AtomicBase:
    def execute(self, **kwargs):
        raise NotImplementedError("Atomic feature must implement execute()")
