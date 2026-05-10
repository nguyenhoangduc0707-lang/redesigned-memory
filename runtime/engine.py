from runtime.dispatcher import Dispatcher
from runtime.worker_pool import WorkerPool
from runtime.event_bus import EventBus
from runtime.dag_engine import DAG


class Engine:
    def __init__(self):
        self.dispatcher = Dispatcher()

        self.worker_pool = WorkerPool(
            num_workers=4
        )

        self.event_bus = EventBus()

    def create_dag(self):
        return DAG(
            self.dispatcher,
            self.worker_pool,
            self.event_bus
        )