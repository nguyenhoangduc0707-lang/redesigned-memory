from fastapi import APIRouter
from core.kernel import Kernel
from worker.executor import Executor
from sandbox.security import check_safety
from contracts.contracts import contract_info
from runtime.engine import run_engine
from dag.scheduler import schedule_task
from security.firewall import firewall_check

# Khởi tạo router
router = APIRouter()
kernel = Kernel()
executor = Executor()

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("/run")
def run_task():
    return {"result": kernel.run()}

@router.get("/execute/{task}")
def execute_task(task: str):
    return {"result": executor.execute(task)}

@router.get("/safe-check")
def safe_check():
    return {"safe": check_safety()}

@router.get("/contract-info")
def contract_info_endpoint():
    return {"contract": contract_info()}

@router.get("/engine-run")
def engine_run():
    return {"engine": run_engine()}

@router.get("/schedule/{task}")
def schedule(task: str):
    return {"schedule": schedule_task(task)}

@router.get("/firewall")
def firewall():
    return {"firewall": firewall_check()}
from fastapi import APIRouter
from core.kernel import Kernel
from worker.executor import Executor
from sandbox.security import check_safety
from contracts.contracts import contract_info
from runtime.engine import run_engine
from dag.scheduler import schedule_task
from security.firewall import firewall_check

class Kernel:
    def run(self):
        return "Kernel executed successfully"


# Khởi tạo router
router = APIRouter()
kernel = Kernel()
executor = Executor()

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("/run")
def run_task():
    return {"result": kernel.run()}

@router.get("/execute/{task}")
def execute_task(task: str):
    return {"result": executor.execute(task)}

@router.get("/safe-check")
def safe_check():
    return {"safe": check_safety()}

@router.get("/contract-info")
def contract_info_endpoint():
    return {"contract": contract_info()}

@router.get("/engine-run")
def engine_run():
    return {"engine": run_engine()}

@router.get("/schedule/{task}")
def schedule(task: str):
    return {"schedule": schedule_task(task)}

@router.get("/firewall")
def firewall():
    return {"firewall": firewall_check()}
