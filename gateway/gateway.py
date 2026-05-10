from core.kernel import Kernel

class Gateway:
    def __init__(self):
        self.kernel = Kernel()

    def handle(self, request):
        return self.kernel.execute(request)
