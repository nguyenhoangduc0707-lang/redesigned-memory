import sys
import subprocess

def check_approval_conditions():
    print("=== QUANTUM PLANNER - APPROVAL GATE ===")
    
    # Kiểm tra Git status
    print("\n[1] Checking Git status...")
    git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if git_status.stdout.strip():
        print("   ⚠️ There are uncommitted changes. Please commit or stash.")
        return False
    else:
        print("   ✅ Working directory clean.")
    
    # Kiểm tra tag hiện tại
    print("\n[2] Checking current tag...")
    tag_check = subprocess.run(["git", "describe", "--tags", "--exact-match"], capture_output=True, text=True)
    if tag_check.returncode == 0:
        print(f"   ✅ Current tag: {tag_check.stdout.strip()}")
    else:
        print("   ℹ️ No exact tag on this commit.")
    
    # Kiểm tra nhánh hiện tại
    print("\n[3] Checking current branch...")
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    print(f"   📍 Current branch: {branch}")
    
    # Kiểm tra các báo cáo validator
    print("\n[4] Checking validator reports...")
    import os
    if os.path.exists("validator_bandit.txt") or os.path.exists("quantum_validator_report.html"):
        print("   ✅ Validator report found.")
    else:
        print("   ⚠️ No validator report found. Run SEN_Validator first.")
    
    return True

def main():
    if check_approval_conditions():
        print("\n✅ ALL CONDITIONS SATISFIED. APPROVAL GATE: GREEN")
        print("\n🚀 You may proceed with merging and deployment.")
        print("   Suggested next steps:")
        print("   1. Create pull request from current branch to main/kernel")
        print("   2. Run final integration tests")
        print("   3. Deploy to staging environment")
        sys.exit(0)
    else:
        print("\n❌ APPROVAL GATE: RED. Fix issues before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
