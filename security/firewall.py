from atomic_base import AtomicBase

class Firewall(AtomicBase):
    def execute(self, **kwargs):
        return {"firewall": "Firewall active"}
