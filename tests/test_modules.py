from core.kernel import Kernel
from worker.executor import Executor
from sandbox.security import Security
from contracts.contracts import Contracts
from runtime.engine import Engine
from dag.scheduler import Scheduler
from security.firewall import Firewall


def test_kernel_run():
    k = Kernel()
    assert k.execute() == "Kernel executed successfully"


def test_executor_execute():
    e = Executor()
    assert e.execute("test") == "Executing test"


def test_check_safety():
    s = Security()
    assert s.execute() == {"safe": True}


def test_contract_info():
    c = Contracts()
    assert c.execute() == {"contract": "Contract details"}


def test_run_engine():
    e = Engine()
    assert e.execute() == {"engine": "Engine running"}


def test_schedule_task():
    sch = Scheduler()
    assert sch.execute("demo") == {"schedule": "Task demo scheduled"}


def test_firewall_check():
    f = Firewall()
    assert f.execute() == {"firewall": "Firewall active"}
