from atomic_base import AtomicBase

class Security(AtomicBase):
    def execute(self, **kwargs):
        return {"safe": True}
