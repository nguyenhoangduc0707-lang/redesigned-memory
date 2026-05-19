import subprocess
import tempfile
import os
import sys
import json

def run_in_sandbox(code: str, input_data: dict = None) -> dict:
    """
    Chạy code Python trong subprocess (tạm thời, không cô lập hoàn toàn).
    Trả về kết quả dạng dict.
    """
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            if input_data:
                f.write(f"import json\ninput_data = {json.dumps(input_data)}\n")
            f.write(code)
            tmp_path = f.name
        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        if result.returncode == 0:
            return {"success": True, "output": output.strip()}
        else:
            return {"success": False, "error": output.strip()}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Execution timeout"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
