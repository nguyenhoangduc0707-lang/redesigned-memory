import getpass
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import ENV_PATH
from src.key_manager import KEY_GROUPS, audit_keys


def read_env_lines():
    if not ENV_PATH.exists():
        return []
    return ENV_PATH.read_text(encoding="utf-8", errors="replace").splitlines()


def upsert_env_value(name, value):
    lines = read_env_lines()
    prefix = f"{name}="
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith(prefix):
            new_lines.append(f"{name}={value}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        if new_lines and new_lines[-1].strip():
            new_lines.append("")
        new_lines.append(f"{name}={value}")
    ENV_PATH.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def list_keys():
    for group, names in KEY_GROUPS.items():
        print(f"\n[{group}]")
        for name in names:
            print(f"  - {name}")


def audit():
    for record in audit_keys():
        print(f"{record.group}:{record.name} status={record.status} length={record.length}")


def set_key(name):
    allowed = {name for names in KEY_GROUPS.values() for name in names}
    if name not in allowed:
        raise SystemExit(f"Unsupported key name: {name}")
    value = getpass.getpass(f"Enter value for {name}: ").strip()
    if not value:
        raise SystemExit("Empty value; nothing changed")
    upsert_env_value(name, value)
    print(f"Updated {name} in .env")


def main(argv):
    if len(argv) < 2 or argv[1] in ("help", "--help", "-h"):
        print("Usage:")
        print("  python scripts/credential_agent.py list")
        print("  python scripts/credential_agent.py audit")
        print("  python scripts/credential_agent.py set KEY_NAME")
        print("\nThis tool never collects cookies or scrapes credentials. It only stores values you enter.")
        return

    command = argv[1]
    if command == "list":
        list_keys()
    elif command == "audit":
        audit()
    elif command == "set" and len(argv) == 3:
        set_key(argv[2])
    else:
        raise SystemExit("Invalid command")


if __name__ == "__main__":
    main(sys.argv)
