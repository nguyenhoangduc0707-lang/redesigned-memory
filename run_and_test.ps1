import pytest

from core.kernel import Kernel
from worker.executor import Executor
from sandbox.security import check_safety
from contracts.contracts import contract_info
from runtime.engine import run_engine
from dag.scheduler import schedule_task
from security.firewall import firewall_check

def test_kernel_run():
    k = Kernel()
    assert k.run() == "Kernel executed successfully"

def test_executor_execute():
    e = Executor()
    assert e.execute("demo") == "Executing demo"

def test_check_safety():
    assert check_safety() is True

def test_contract_info():
    assert contract_info() == "Contract details"

def test_run_engine():
    assert run_engine() == "Engine running"

def test_schedule_task():
    assert schedule_task("demo") == "Task demo scheduled"

def test_firewall_check():
    assert firewall_check() == "Firewall active"
