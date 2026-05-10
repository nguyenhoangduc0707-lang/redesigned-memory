# Script tự động kiểm tra và bổ sung các file/hàm còn thiếu trong AI_OS_KERNEL_V3
$basePath = "C:\AI_OS_KERNEL_V3"

# Danh sách file và nội dung tối thiểu
$filesContent = @{
    "core\kernel.py"      = "class Kernel:`n    def run(self):`n        return 'Kernel executed successfully'"
    "worker\executor.py"  = "class Executor:`n    def execute(self, task: str):`n        return f'Executing {task}'"
    "sandbox\security.py" = "def check_safety():`n    return True"
    "contracts\contracts.py" = "def contract_info():`n    return 'Contract details'"
    "runtime\engine.py"   = "def run_engine():`n    return 'Engine running'"
    "dag\scheduler.py"    = "def schedule_task(task: str):`n    return f'Task {task} scheduled'"
    "security\firewall.py"= "def firewall_check():`n    return 'Firewall active'"
}

Write-Host "🔧 Bắt đầu kiểm tra và bổ sung project tại $basePath"

foreach ($file in $filesContent.Keys) {
    $fullPath = Join-Path $basePath $file
    if (!(Test-Path $fullPath)) {
        Write-Host "❌ Thiếu file: $file -> tạo mới"
        $dir = Split-Path $fullPath
        if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force }
        Set-Content -Path $fullPath -Value $filesContent[$file]
    } else {
        $content = Get-Content $fullPath -Raw
        if ($content -notmatch ($filesContent[$file].Split("`n")[0])) {
            Write-Host "⚠️  $file thiếu định nghĩa -> bổ sung"
            Set-Content -Path $fullPath -Value $filesContent[$file]
        } else {
            Write-Host "✅ $file OK"
        }
    }
}

# Đảm bảo có __init__.py trong các thư mục
$folders = @("core","gateway","worker","sandbox","security","contracts","dag","runtime")
foreach ($f in $folders) {
    $initPath = Join-Path $basePath "$f\__init__.py"
    if (!(Test-Path $initPath)) {
        Write-Host "❌ Thiếu __init__.py trong $f -> tạo mới"
        Set-Content -Path $initPath -Value ""
    } else {
        Write-Host "✅ $f có __init__.py"
    }
}
