# PowerShell UTF-8 setup
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
chcp 65001 > $null
$ErrorActionPreference = "Stop"

$root = "C:\AI_OS_KERNEL_V3"
Set-Location $root

Write-Host "=== AI_OS_KERNEL_V3 CHECK AND FIX ===" -ForegroundColor Cyan

Write-Host "[1] Ensure database schema" -ForegroundColor Yellow
python -c "from src.database import init_db; from src.affiliate_manager import init_affiliate_tables; init_db(); init_affiliate_tables()"

Write-Host "[2] Validate imports and structure" -ForegroundColor Yellow
python scripts\validate.py

Write-Host "[3] Check entrypoint" -ForegroundColor Yellow
python -c "import src.main; print('[OK] src.main importable')"

Write-Host "=== COMPLETE ===" -ForegroundColor Cyan
Write-Host "Run server with: python -m src.main" -ForegroundColor Green
