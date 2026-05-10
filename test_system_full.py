import os
import sys
import subprocess

# =========================
# AI_OS KERNEL BOOTSTRAP FIX (V4 STABLE)
# =========================

# Root project
ROOT = os.path.abspath(os.path.dirname(__file__))

# Force project root FIRST in import path
sys.path.insert(0, ROOT)

# Stabilize environment
os.environ["PYTHONPATH"] = ROOT

# Optional venv python (safe fallback)
venv_python = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(venv_python):
    venv_python = sys.executable  # fallback system python

# Debug bootstrap
print("[BOOTSTRAP] ROOT =", ROOT)
print("[BOOTSTRAP] PYTHONPATH =", os.environ["PYTHONPATH"])
print("[BOOTSTRAP] SYS PATH[0] =", sys.path[0])
print("[BOOTSTRAP] PYTHON =", venv_python)


# =========================
# TEST HELPERS
# =========================

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


# =========================
# MAIN TEST
# =========================

def main():
    print("\n" + "=" * 50)
    print("  AI_OS_KERNEL_V3 - FULL SYSTEM TEST")
    print("=" * 50 + "\n")

    # 1. STRUCTURE CHECK
    print("[1] Kiểm tra cấu trúc thư mục:")
    required_dirs = [
        "core", "gateway", "runtime", "scheduler", "worker",
        "security", "sandbox", "contracts", "registry", "dag", "tests"
    ]

    for d in required_dirs:
        path = os.path.join(ROOT, d)
        print(f"     {'✅' if os.path.isdir(path) else '❌'} {d}")

    # 2. ENV CHECK
    print("\n[2] Kiểm tra .env:")
    env_path = os.path.join(ROOT, ".env")

    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        print(f"     ✅ .env tồn tại, nội dung: {content[:50]}...")
    else:
        print("     ❌ .env không tồn tại!")

    # 3. PYTHON SYNTAX CHECK
    print("\n[3] Kiểm tra syntax Python:")

    for root, dirs, files in os.walk(ROOT):
        if ".venv" in root or "__pycache__" in root:
            continue

        for f in files:
            if f.endswith(".py"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ROOT)

                result = run_cmd([venv_python, "-m", "py_compile", full_path])

                if result.returncode == 0:
                    print(f"     ✅ {rel_path}")
                else:
                    print(f"     ❌ {rel_path}: {result.stderr[:120]}")

    # 4. IMPORT CHECK
    print("\n[4] Kiểm tra imports:")

    modules = ["core", "gateway", "runtime", "scheduler", "worker", "security", "contracts"]

    for mod in modules:
        cmd = [
            venv_python,
            "-c",
            f"import sys; sys.path.insert(0, r'{ROOT}'); import {mod}; print('{mod} OK')"
        ]

        result = run_cmd(cmd)

        if result.returncode == 0:
            print(f"     ✅ {mod}")
        else:
            print(f"     ❌ {mod}: {result.stderr[:120]}")

    # 5. PORT CHECK
    print("\n[5] Kiểm tra ports:")

    result = run_cmd(["netstat", "-ano"])

    listening = [l for l in result.stdout.splitlines() if "LISTENING" in l]

    print(f"     📊 Có {len(listening)} ports đang LISTENING")

    # 6. PROCESS CHECK
    print("\n[6] Kiểm tra process Python:")

    result = run_cmd([
        "tasklist",
        "/FI", "IMAGENAME eq python.exe",
        "/FO", "CSV"
    ])

    lines = [l for l in result.stdout.splitlines() if "python" in l.lower()]

    print(f"     🔄 Số process Python: {len(lines)}")

    print("\n" + "=" * 50)
    print("  ✅ TEST HOÀN TẤT")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()