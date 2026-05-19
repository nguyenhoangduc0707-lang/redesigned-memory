import os
from datetime import datetime
from pathlib import Path

ROOT = Path("C:/AI_OS_KERNEL_V3")
OUTPUT_FILE = ROOT / "AI_OS_KERNEL_V3_FULL_EXPORT.md"
MAX_FILE_SIZE = 120 * 1024

CORE_DIRS = {
    "src",
    "scripts",
    "worker",
    "tests",
    "gateway/templates",
    "monitors",
}

CORE_ROOT_FILES = {
    "README.md",
    "FINAL_REPORT.md",
    "requirements.txt",
    "docker-compose.yml",
    "Dockerfile.txt",
    "Fix_and_Check_All.ps1",
    "run_and_validate_no_emoji.ps1",
    "export_to_notebooklm.py",
}

BACKUP_DIRS = {
    "_duplicates_backup",
}

EXCLUDE_DIR_NAMES = {
    ".git",
    ".pytest_cache",
    ".venv",
    ".venv_aios",
    "__pycache__",
    "audio",
    "BANER_ADMIN",
    "data",
    "devcodeai",
    "dockerun-host",
    "logs",
    "models",
    "reports",
    "static",
    "uploads",
}

EXCLUDE_FILE_NAMES = {
    ".env",
    ".env.backup",
    ".cmd_history",
    ".sen_history",
    "AI_OS_KERNEL_V3_FULL_EXPORT.md",
    "API_KEYS_FOUND.txt",
    "API_KEY_AUDIT.md",
    "Project_File_Inventory.csv",
    "cleanup_log_20260518_182039.txt",
    "py_files.txt",
    "project_structure.csv",
    "project_structure.txt",
}

INCLUDE_EXT = {
    ".py",
    ".html",
    ".ps1",
    ".md",
    ".txt",
    ".json",
    ".css",
    ".js",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
}


def is_under(path, folder):
    try:
        path.relative_to(ROOT / folder)
        return True
    except ValueError:
        return False


def is_core_file(path):
    if path.name in EXCLUDE_FILE_NAMES:
        return False
    if any(part in EXCLUDE_DIR_NAMES or part.startswith("_backup_") for part in path.relative_to(ROOT).parts):
        return False
    if path.suffix.lower() not in INCLUDE_EXT:
        return False
    if path.parent == ROOT and path.name in CORE_ROOT_FILES:
        return True
    return any(is_under(path, folder) for folder in CORE_DIRS)


def read_file_safe(path):
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        if len(content) > MAX_FILE_SIZE:
            return content[:MAX_FILE_SIZE] + f"\n... [TRUNCATED AT {MAX_FILE_SIZE} CHARS]"
        return content
    except Exception as exc:
        return f"[READ ERROR: {exc}]"


def language_for(path):
    ext = path.suffix.lower()
    return {
        ".py": "python",
        ".html": "html",
        ".ps1": "powershell",
        ".json": "json",
        ".md": "markdown",
        ".css": "css",
        ".js": "javascript",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".toml": "toml",
    }.get(ext, "text")


def iter_core_files():
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and is_core_file(path):
            yield path


def backup_manifest():
    lines = ["## Backup Manifest", ""]
    for folder in sorted(BACKUP_DIRS):
        backup_path = ROOT / folder
        if not backup_path.exists():
            continue
        lines.append(f"### `{folder}`")
        for path in sorted(backup_path.rglob("*")):
            if path.is_file() and path.suffix.lower() in INCLUDE_EXT:
                rel = path.relative_to(ROOT)
                lines.append(f"- `{rel}` ({path.stat().st_size} bytes)")
        lines.append("")
    return lines


def project_tree(files):
    lines = ["## Project Tree", "", "```text"]
    for path in files:
        lines.append(str(path.relative_to(ROOT)))
    lines.append("```")
    return lines


def main():
    files = list(iter_core_files())
    lines = [
        "# AI_OS_KERNEL_V3 - Clean NotebookLM Export",
        "",
        f"Exported: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "Scope: one active project plus a minimal backup manifest.",
        "Excluded: .env, API/key scans, generated exports, logs, binary assets, databases, models, caches, and old backup dumps.",
        "",
    ]
    lines.extend(project_tree(files))
    lines.append("")
    lines.extend(backup_manifest())

    for path in files:
        rel = path.relative_to(ROOT)
        lines.append(f"\n## FILE: `{rel}`\n")
        lines.append(f"```{language_for(path)}")
        lines.append(read_file_safe(path))
        lines.append("```")

    OUTPUT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Exported clean NotebookLM file: {OUTPUT_FILE}")
    print(f"Files included: {len(files)}")
    print(f"Size MB: {OUTPUT_FILE.stat().st_size / (1024 * 1024):.2f}")


if __name__ == "__main__":
    main()
