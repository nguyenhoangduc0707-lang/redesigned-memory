# atomic_run_and_test.ps1
param(
    [int]$Port = 8080,
    [int]$StartupWaitSeconds = 5,
    [string]$ProjectDir = "C:\AI_OS_KERNEL_V3"
)

Set-StrictMode -Version Latest
Write-Host "📁 Project dir:" $ProjectDir
Write-Host "🔌 Target port:" $Port

# 1) Kiểm tra tiến trình đang lắng nghe trên cổng
Write-Host "🔎 Kiểm tra cổng $Port..."
$net = netstat -ano | Select-String ":$Port\s"
if ($net) {
    Write-Host "⚠️  Cổng $Port đang bị chiếm. Tìm PID..."
    $lines = $net -split "`n"
    foreach ($line in $lines) {
        $parts = ($line -split '\s+') | Where-Object { $_ -ne "" }
        if ($parts.Length -ge 5) {
            $pid = $parts[-1]
            Write-Host "➡️  Dừng tiến trình PID" $pid "..."
            try {
                Stop-Process -Id $pid -Force -ErrorAction Stop
                Write-Host "✅ Đã dừng PID" $pid
            } catch {
                # In lỗi an toàn: truyền từng phần, không dùng nội suy biến trong chuỗi
                Write-Host "❌ Không thể dừng PID" $pid ":" $_.Exception.Message
            }
        }
    }
} else {
    Write-Host "✅ Cổng $Port hiện rảnh."
}

# 2) (Tùy chọn) Dừng tất cả python.exe nếu thực sự cần
# Get-Process python -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.Id -Force }

# 3) Chuyển vào thư mục dự án
Set-Location $ProjectDir

# 4) Khởi động uvicorn trong tiến trình PowerShell mới (tách tiến trình)
Write-Host "🚀 Khởi động Uvicorn trên cổng $Port..."
$uvicornCmd = "cd `"$ProjectDir`"; python -m uvicorn main:app --host 127.0.0.1 --port $Port"
Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Hidden -Command $uvicornCmd" -PassThru | Out-Null

# 5) Chờ server khởi động
Write-Host "⏳ Chờ $StartupWaitSeconds giây để server khởi động..."
Start-Sleep -Seconds $StartupWaitSeconds

# 6) Kiểm tra server đã lắng nghe chưa
$net2 = netstat -ano | Select-String ":$Port\s"
if (-not $net2) {
    Write-Host "❌ Server chưa lắng nghe trên cổng $Port. Kiểm tra log uvicorn hoặc tăng thời gian chờ."
    exit 1
}
Write-Host "✅ Server đang lắng nghe trên cổng $Port."

# 7) Chạy unit tests
Write-Host "🧪 Chạy unit tests (pytest)..."
try {
    python -m pytest -v
    Write-Host "✅ Pytest hoàn tất."
} catch {
    Write-Host "❌ Pytest gặp lỗi:" $_.Exception.Message
}

# 8) Chạy test endpoint (script test_endpoints.ps1)
$endpointsScript = Join-Path $ProjectDir "test_endpoints.ps1"
if (Test-Path $endpointsScript) {
    Write-Host "🔍 Chạy test_endpoints.ps1..."
    try {
        & $endpointsScript
        Write-Host "✅ test_endpoints.ps1 hoàn tất."
    } catch {
        Write-Host "❌ Lỗi khi chạy test_endpoints.ps1:" $_.Exception.Message
    }
} else {
    Write-Host "⚠️ Không tìm thấy test_endpoints.ps1 tại" $endpointsScript
}

Write-Host "🎉 Hoàn tất atomic_run_and_test.ps1"
