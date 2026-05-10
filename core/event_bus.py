import asyncio
from collections import defaultdict


class EventBus:

    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_name, handler):
        self.listeners[event_name].append(handler)

    async def emit(self, event_name, payload=None):

        handlers = self.listeners.get(event_name, [])

        for handler in handlers:
            asyncio.create_task(handler(payload))