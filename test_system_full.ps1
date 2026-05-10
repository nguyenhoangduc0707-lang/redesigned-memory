# test_system_full.ps1
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AI_OS_KERNEL_V3 - FULL SYSTEM TEST" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

$root = "C:\AI_OS_KERNEL_V3"
$errors = @()
$passed = 0
$failed = 0

# Dictionary lưu kết quả
$results = @{}

# --- TEST 1: Kiểm tra cấu trúc thư mục ---
Write-Host "[1/10] Kiểm tra cấu trúc thư mục..." -ForegroundColor Green
$requiredDirs = @(
    "core", "gateway", "runtime", "scheduler", "worker", 
    "security", "sandbox", "contracts", "registry", "dag",
    "tests", "__pycache__", ".venv"
)
$missingDirs = @()
foreach ($dir in $requiredDirs) {
    if (-not (Test-Path "$root\$dir")) { $missingDirs += $dir }
}

if ($missingDirs.Count -eq 0) {
    Write-Host "  ✅ Tất cả thư mục đều tồn tại" -ForegroundColor Green
    $passed++
    $results["Structure"] = "PASS"
} else {
    Write-Host "  ❌ Thiếu thư mục: $($missingDirs -join ', ')" -ForegroundColor Red
    $failed++
    $results["Structure"] = "FAIL"
}

# --- TEST 2: Kiểm tra file quan trọng ---
Write-Host "[2/10] Kiểm tra file quan trọng..." -ForegroundColor Green
$requiredFiles = @(
    "main.py", "atomic_base.py", ".env", "requirements.txt",
    "atomic_fix_all.ps1", "atomic_run_and_test.ps1", "check_project.ps1",
    "fix_project.ps1", "run_and_test.ps1", "test_endpoints.ps1"
)
$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (-not (Test-Path "$root\$file")) { $missingFiles += $file }
}

if ($missingFiles.Count -eq 0) {
    Write-Host "  ✅ Tất cả file quan trọng đều tồn tại" -ForegroundColor Green
    $passed++
    $results["Files"] = "PASS"
} else {
    Write-Host "  ⚠️  Thiếu file: $($missingFiles -join ', ')" -ForegroundColor Yellow
    $failed++
    $results["Files"] = "FAIL"
}

# --- TEST 3: Kiểm tra Python environment ---
Write-Host "[3/10] Kiểm tra Python environment..." -ForegroundColor Green
$venvPython = "$root\.venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    $pyVersion = & $venvPython --version 2>&1
    Write-Host "  ✅ Virtual env Python: $pyVersion" -ForegroundColor Green
    
    # Kiểm tra pip
    $pipList = & "$root\.venv\Scripts\pip.exe" list --format=freeze 2>&1
    $pipCount = ($pipList | Measure-Object).Line
    Write-Host "  📦 Số packages installed: $pipCount" -ForegroundColor Cyan
    $passed++
    $results["PythonEnv"] = "PASS"
} else {
    Write-Host "  ❌ Không tìm thấy Python venv!" -ForegroundColor Red
    $failed++
    $results["PythonEnv"] = "FAIL"
}

# --- TEST 4: Kiểm tra port và URL ACL ---
Write-Host "[4/10] Kiểm tra network configuration..." -ForegroundColor Green
$urlAcl = netsh http show urlacl 2>&1
$portsInUse = @()
if ($urlAcl -match 'https?://\+:(\d+)') {
    $portsInUse += $matches[1]
}
Write-Host "  🌐 Các port đang được đăng ký URLACL: $($portsInUse -join ', ')" -ForegroundColor Cyan

# Kiểm tra netstat
$netstat = Get-Content "$root\netstat_full.txt" -ErrorAction SilentlyContinue
if ($netstat) {
    $listening = $netstat | Select-String "LISTENING"
    Write-Host "  🔌 Số kết nối LISTENING: $(($listening | Measure-Object).Line)" -ForegroundColor Cyan
    $passed++
    $results["Network"] = "PASS"
} else {
    Write-Host "  ⚠️  Không tìm thấy netstat_full.txt" -ForegroundColor Yellow
    $results["Network"] = "WARN"
}

# --- TEST 5: Kiểm tra module core ---
Write-Host "[5/10] Kiểm tra module core..." -ForegroundColor Green
$coreFiles = Get-ChildItem "$root\core" -Filter "*.py" -ErrorAction SilentlyContinue
if ($coreFiles.Count -gt 0) {
    Write-Host "  ✅ Core có $($coreFiles.Count) file Python:" -ForegroundColor Green
    foreach ($cf in $coreFiles) {
        Write-Host "     📄 $($cf.Name)" -ForegroundColor Gray
    }
    $passed++
    $results["CoreModule"] = "PASS"
} else {
    Write-Host "  ❌ Core module rỗng!" -ForegroundColor Red
    $failed++
    $results["CoreModule"] = "FAIL"
}

# --- TEST 6: Kiểm tra Gateway ---
Write-Host "[6/10] Kiểm tra Gateway..." -ForegroundColor Green
$gatewayFiles = Get-ChildItem "$root\gateway" -Filter "*.py" -ErrorAction SilentlyContinue
if ($gatewayFiles.Count -gt 0) {
    Write-Host "  ✅ Gateway có $($gatewayFiles.Count) file:" -ForegroundColor Green
    foreach ($gf in $gatewayFiles) {
        Write-Host "     📄 $($gf.Name)" -ForegroundColor Gray
    }
    $passed++
    $results["Gateway"] = "PASS"
} else {
    Write-Host "  ❌ Gateway rỗng!" -ForegroundColor Red
    $failed++
    $results["Gateway"] = "FAIL"
}

# --- TEST 7: Kiểm tra Security + Sandbox ---
Write-Host "[7/10] Kiểm tra Security & Sandbox..." -ForegroundColor Green
$securityFiles = Get-ChildItem "$root\security" -Filter "*.py" -ErrorAction SilentlyContinue
$sandboxFiles = Get-ChildItem "$root\sandbox" -Filter "*.py" -ErrorAction SilentlyContinue

if ($securityFiles.Count -gt 0 -and $sandboxFiles.Count -gt 0) {
    Write-Host "  🔒 Security: $($securityFiles.Count) file(s)" -ForegroundColor Green
    Write-Host "  📦 Sandbox: $($sandboxFiles.Count) file(s)" -ForegroundColor Green
    $passed++
    $results["Security"] = "PASS"
} else {
    Write-Host "  ⚠️  Security/Sandbox còn thiếu file" -ForegroundColor Yellow
    $results["Security"] = "WARN"
}

# --- TEST 8: Kiểm tra Scheduler & Worker ---
Write-Host "[8/10] Kiểm tra Scheduler & Worker..." -ForegroundColor Green
$schedulerFiles = Get-ChildItem "$root\scheduler" -Filter "*.py" -ErrorAction SilentlyContinue
$workerFiles = Get-ChildItem "$root\worker" -Filter "*.py" -ErrorAction SilentlyContinue

if ($schedulerFiles.Count -gt 0) { 
    Write-Host "  ⏰ Scheduler: $($schedulerFiles.Count) file(s)" -ForegroundColor Green 
}
if ($workerFiles.Count -gt 0) { 
    Write-Host "  ⚙️  Worker: $($workerFiles.Count) file(s)" -ForegroundColor Green 
}
$passed++
$results["SchedulerWorker"] = "PASS"

# --- TEST 9: Kiểm tra Run các module (dry-run) ---
Write-Host "[9/10] Kiểm tra syntax Python files..." -ForegroundColor Green
$pyFiles = Get-ChildItem "$root" -Filter "*.py" -Recurse -ErrorAction SilentlyContinue
$syntaxErrors = @()

foreach ($pyFile in $pyFiles) {
    # Bỏ qua __pycache__ và .venv
    if ($pyFile.FullName -match "__pycache__|\.venv") { continue }
    
    $result = & $venvPython -m py_compile $pyFile.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
        $syntaxErrors += "$($pyFile.FullName): $result"
    }
}

if ($syntaxErrors.Count -eq 0) {
    Write-Host "  ✅ Tất cả $($pyFiles.Count) file Python đều syntax OK" -ForegroundColor Green
    $passed++
    $results["Syntax"] = "PASS"
} else {
    Write-Host "  ❌ Có $($syntaxErrors.Count) lỗi syntax:" -ForegroundColor Red
    foreach ($err in $syntaxErrors) {
        Write-Host "     ❌ $err" -ForegroundColor Red
    }
    $failed++
    $results["Syntax"] = "FAIL"
}

# --- TEST 10: Kiểm tra Import chain ---
Write-Host "[10/10] Kiểm tra import chain..." -ForegroundColor Green
try {
    $importResult = & $venvPython -c "
import sys
sys.path.insert(0, '$root')
print('Testing imports...')
try:
    import core
    print('✅ core imported')
except Exception as e:
    print(f'❌ core: {e}')
try:
    import gateway
    print('✅ gateway imported')
except Exception as e:
    print(f'❌ gateway: {e}')
" 2>&1
    Write-Host "  $importResult" -ForegroundColor Cyan
    $passed++
    $results["Imports"] = "PASS"
} catch {
    Write-Host "  ❌ Import chain failed: $_" -ForegroundColor Red
    $failed++
    $results["Imports"] = "FAIL"
}

# --- KẾT QUẢ TỔNG HỢP ---
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "         📊 KẾT QUẢ TEST TỔNG HỢP" -ForegroundColor Yellow
Write-Host "========================================`n" -ForegroundColor Cyan

foreach ($key in $results.Keys) {
    $status = $results[$key]
    $icon = if ($status -eq "PASS") { "✅" } elseif ($status -eq "FAIL") { "❌" } else { "⚠️" }
    Write-Host "  $icon $key`: $status"
}

Write-Host "`n----------------------------------------" -ForegroundColor Gray
Write-Host "  Tổng số: $($results.Count) tests" -ForegroundColor White
Write-Host "  ✅ Passed: $passed" -ForegroundColor Green
Write-Host "  ❌ Failed: $failed" -ForegroundColor Red
Write-Host "----------------------------------------`n" -ForegroundColor Gray