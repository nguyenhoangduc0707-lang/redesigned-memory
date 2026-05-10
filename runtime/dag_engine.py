from runtime.node_state import NodeState
from runtime.retry_policy import RetryPolicy
from runtime.timeout_guard import TimeoutGuard

import time


class DAG:

    def __init__(self, dispatcher, worker_pool, event_bus):

        self.dispatcher = dispatcher
        self.worker_pool = worker_pool
        self.event_bus = event_bus

        self.nodes = {}

        self.retry_policy = RetryPolicy()
        self.timeout_guard = TimeoutGuard()

        self.results = {}

        self.active_futures = {}

        # subscribe events
        self.event_bus.subscribe(
            "NODE_COMPLETED",
            self.on_node_completed
        )

    def add_node(self, name, fn, deps=None):

        self.nodes[name] = {
            "fn": fn,
            "deps": deps or [],
            "state": NodeState.CREATED,
            "attempt": 0
        }

    def can_run(self, node_name):

        deps = self.nodes[node_name]["deps"]

        for dep in deps:

            if self.nodes[dep]["state"] != NodeState.COMPLETED:
                return False

        return True

    def schedule_node(self, node_name):

        node = self.nodes[node_name]

        # already running/completed
        if node["state"] != NodeState.CREATED:
            return

        # deps not ready
        if not self.can_run(node_name):
            return

        node["state"] = NodeState.RUNNING

        future = self.worker_pool.submit(
            self.run_node,
            node_name
        )

        self.active_futures[node_name] = future

    def run_node(self, node_name):

        node = self.nodes[node_name]

        try:

            result = self.timeout_guard.run_with_timeout(
                node["fn"],
                timeout=30
            )

            node["state"] = NodeState.COMPLETED

            self.results[node_name] = {
                "status": "COMPLETED",
                "result": result
            }

            self.event_bus.emit(
                "NODE_COMPLETED",
                {
                    "node": node_name
                }
            )

            return result

        except Exception as e:

            node["attempt"] += 1

            # retry logic
            if self.retry_policy.should_retry(node["attempt"]):

                node["state"] = NodeState.CREATED

                return self.run_node(node_name)

            # permanent fail
            node["state"] = NodeState.FAILED

            self.results[node_name] = {
                "status": "FAILED",
                "error": str(e)
            }

            self.event_bus.emit(
                "NODE_FAILED",
                {
                    "node": node_name,
                    "error": str(e)
                }
            )

            return None

    def on_node_completed(self, payload):

        completed_node = payload["node"]

        # unlock downstream nodes
        for node_name, node in self.nodes.items():

            if completed_node in node["deps"]:

                self.schedule_node(node_name)

    def run(self):

        # schedule root nodes
        for node_name, node in self.nodes.items():

            if not node["deps"]:
                self.schedule_node(node_name)

        # orchestration loop
        while len(self.active_futures) > 0:

            for node_name, future in list(self.active_futures.items()):

                if future.done():

                    try:
                        future.result()

                    except Exception as e:

                        self.results[node_name] = {
                            "status": "FAILED",
                            "error": str(e)
                        }

                    # safe delete
                    if node_name in self.active_futures:
                        del self.active_futures[node_name]

            # prevent busy loop
            time.sleep(0.05)

        return self.results