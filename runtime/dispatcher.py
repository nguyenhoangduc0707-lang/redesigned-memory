import uuid


class Dispatcher:

    def __init__(self):

        self.results = {}

    def create_task_id(self):

        return str(uuid.uuid4())

    def store_result(self, task_id, result):

        self.results[task_id] = result

    def get_result(self, task_id):

        return self.results.get(task_id)