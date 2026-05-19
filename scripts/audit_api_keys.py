import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.key_manager import audit_keys


def write_report(records, output_path):
    lines = [
        "# API Key Audit",
        "",
        "Secrets are redacted. This report only records status, group, and value length.",
        "",
        "| Group | Name | Status | Length | Reason |",
        "|---|---|---:|---:|---|",
    ]
    for record in records:
        lines.append(
            f"| {record.group} | `{record.name}` | {record.status} | {record.length} | {record.reason} |"
        )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    records = audit_keys()
    output_path = ROOT / "API_KEY_AUDIT.md"
    write_report(records, output_path)
    for record in records:
        print(f"{record.group}:{record.name} status={record.status} length={record.length}")
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
