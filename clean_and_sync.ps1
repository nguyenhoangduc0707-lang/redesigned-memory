cd C:\AI_OS_KERNEL_V3

Write-Host "🧹 Dọn dẹp cache và file biên dịch..."
Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "📂 Chuẩn hóa thư mục và __init__.py..."
$folders = @("core","gateway","worker","sandbox","security","contracts","dag","runtime","tests")
foreach ($f in $folders) {
    $path = "C:\AI_OS_KERNEL_V3\$f"
    if (!(Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force }
    $initPath = "$path\__init__.py"
    if (!(Test-Path $initPath)) { Set-Content -Path $initPath -Value "" }
}

Write-Host "🔧 Fix lại code nếu thiếu định nghĩa..."
.\fix_project.ps1

Write-Host "🧪 Chạy unit test để xác nhận..."
python -m pytest -v

Write-Host "🚀 Khởi động server uvicorn..."
Start-Process powershell -ArgumentList "cd C:\AI_OS_KERNEL_V3; python -m uvicorn main:app --reload --host 127.0.0.1 --port 8080"

Write-Host "⏳ Chờ server khởi động..."
Start-Sleep -Seconds 5

Write-Host "🔍 Test endpoint API..."
.\test_endpoints.ps1

Write-Host "✅ Hoàn tất đồng bộ hóa và kiểm tra hệ thống!"
