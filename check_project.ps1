# Kiểm tra toàn bộ cấu trúc AI_OS_KERNEL_V3
$basePath = "C:\AI_OS_KERNEL_V3"

# Danh sách file cần có và nội dung tối thiểu
$expectedFiles = @{
    "core\kernel.py"      = "class Kernel"
    "worker\executor.py"  = "class Executor"
    "sandbox\security.py" = "def check_safety"
    "contracts\contracts.py" = "def contract_info"
    "runtime\engine.py"   = "def run_engine"
    "dag\scheduler.py"    = "def schedule_task"
    "security\firewall.py"= "def firewall_check"
    "gateway\router.py"   = "router = APIRouter"
    "main.py"             = "FastAPI"
}

Write-Host "🔍 Bắt đầu kiểm tra project tại $basePath"

foreach ($file in $expectedFiles.Keys) {
    $fullPath = Join-Path $basePath $file
    if (Test-Path $fullPath) {
        $content = Get-Content $fullPath -Raw
        if ($content -match $expectedFiles[$file]) {
            Write-Host "✅ $file OK"
        } else {
            Write-Host "⚠️  $file thiếu định nghĩa: $($expectedFiles[$file])"
        }
    } else {
        Write-Host "❌ Thiếu file: $file"
    }
}

# Kiểm tra __init__.py trong các thư mục
$folders = @("core","gateway","worker","sandbox","security","contracts","dag","runtime")
foreach ($f in $folders) {
    $initPath = Join-Path $basePath "$f\__init__.py"
    if (Test-Path $initPath) {
        Write-Host "✅ $f có __init__.py"
    } else {
        Write-Host "❌ Thiếu __init__.py trong $f"
    }
}
