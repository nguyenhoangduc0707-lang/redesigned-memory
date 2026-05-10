import uuid
import time


class Task:

    def __init__(self, task_type, payload):

        self.id = str(uuid.uuid4())

        self.task_type = task_type

        self.payload = payload

        self.created_at = time.time()

        self.status = "PENDING"

    def to_dict(self):

        return {
            "id": self.id,
            "type": self.task_type,
            "payload": self.payload,
            "status": self.status,
            "created_at": self.created_at
        }