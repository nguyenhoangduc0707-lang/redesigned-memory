import ast
import os
import sys

def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source, filename=filepath)
        return True, None
    except IndentationError as e:
        return False, f"IndentationError at line {e.lineno}: {e.msg}"
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)

def scan_project(root_dir='.', exclude_dirs=['venv', '__pycache__', '.git', 'node_modules', 'venv_ci_test', 'venv_aios']):
    errors = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for file in filenames:
            if file.endswith('.py'):
                full_path = os.path.join(dirpath, file)
                ok, msg = analyze_file(full_path)
                if not ok:
                    errors.append((full_path, msg))
                    print(f"❌ {full_path}: {msg}")
    return errors

if __name__ == '__main__':
    print("🔍 Scanning project for syntax errors...")
    errs = scan_project()
    if errs:
        print(f"\nFound {len(errs)} error(s). Please fix them.")
        sys.exit(1)
    else:
        print("✅ No syntax errors found.")
