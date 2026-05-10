import multiprocessing

def _exec(task, q):
    q.put(f'SANDBOX_EXEC:{task}')

class Sandbox:
    def run(self, task):
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=_exec, args=(task, q))
        p.start()
        p.join()
        return {'result': q.get()}
