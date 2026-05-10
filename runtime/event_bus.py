class EventBus:

    def __init__(self):

        self.listeners = {}

    def subscribe(self, event_name, callback):

        if event_name not in self.listeners:
            self.listeners[event_name] = []

        self.listeners[event_name].append(callback)

    def emit(self, event_name, payload=None):

        listeners = self.listeners.get(event_name, [])

        for callback in listeners:
            callback(payload)