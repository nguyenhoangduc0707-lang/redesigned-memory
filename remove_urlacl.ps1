<#
.SYNOPSIS
  Safely list, back up, and optionally delete an HTTP.SYS URL reservation (urlacl).

.DESCRIPTION
  - Runs netsh http show urlacl and saves a timestamped backup to the script folder.
  - Accepts either -Url (exact URL string) or -Port (numeric port) to target.
  - Shows matching entries, asks for explicit confirmation, then attempts deletion.
  - Logs actions and errors to a timestamped log file.

.NOTES
  Run this script in an elevated PowerShell (Run as Administrator).
  Use -WhatIf to preview deletion command without executing.
#>

param(
  [Parameter(Mandatory=$false)]
  [string]$Url,

  [Parameter(Mandatory=$false)]
  [int]$Port = 0,

  [switch]$WhatIf
)

function Write-Log {
  param([string]$Text)
  $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
  $line = "$ts`t$Text"
  $global:LogLines += $line
  Write-Host $Text
}

# Prepare paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $scriptDir) { $scriptDir = Get-Location }
$timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$backupFile = Join-Path $scriptDir "urlacl_backup_$timestamp.txt"
$logFile = Join-Path $scriptDir "remove_urlacl_log_$timestamp.txt"

# Ensure running elevated
if (-not ([bool]([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))) {
  Write-Host "ERROR: This script must be run as Administrator. Right-click PowerShell and choose 'Run as administrator'." -ForegroundColor Red
  exit 1
}

$global:LogLines = @()
Write-Log "Starting remove_urlacl.ps1"
Write-Log "Backing up current urlacl to $backupFile"

# Backup current urlacl
try {
  netsh http show urlacl > $backupFile 2>&1
  Write-Log "Backup saved."
} catch {
  Write-Log "Failed to save backup: $($_.Exception.Message)"
}

# Show current urlacl
Write-Host "`nCurrent URL ACL entries:`n"
netsh http show urlacl
Write-Host "`n"

# Determine target entries
if ($Url) {
  $target = $Url.Trim()
} elseif ($Port -gt 0) {
  $target = "http://*:$Port/"
} else {
  Write-Host "No -Url or -Port provided. To delete a reservation, re-run with -Url 'http://*:5357/' or -Port 5357."
  Write-Log "Aborted: no target specified."
  $global:LogLines | Out-File -FilePath $logFile -Encoding UTF8
  exit 0
}

Write-Log "Target to delete: $target"

# Find matching lines in the backup file to show user
$matches = Select-String -Path $backupFile -Pattern [regex]::Escape($target) -SimpleMatch -ErrorAction SilentlyContinue
if (-not $matches) {
  Write-Host "No exact match found for target in current urlacl output. Please verify the exact URL string from 'netsh http show urlacl'." -ForegroundColor Yellow
  Write-Log "No match found for $target"
  $global:LogLines | Out-File -FilePath $logFile -Encoding UTF8
  exit 1
}

Write-Host "`nFound the following matching urlacl lines:`n"
$matches | ForEach-Object { Write-Host $_.Line }
Write-Host "`n"

# Confirm
$confirm = Read-Host "Type YES to delete the reservation $target (type exactly YES to proceed)"
if ($confirm -ne "YES") {
  Write-Log "User aborted deletion."
  Write-Host "Aborted by user."
  $global:LogLines | Out-File -FilePath $logFile -Encoding UTF8
  exit 0
}

# Execute deletion (or WhatIf)
if ($WhatIf) {
  Write-Host "WhatIf: netsh http delete urlacl url=`"$target`""
  Write-Log "WhatIf mode - no deletion performed."
  $global:LogLines | Out-File -FilePath $logFile -Encoding UTF8
  exit 0
}

Write-Log "Attempting to delete $target"
try {
  $proc = Start-Process -FilePath netsh -ArgumentList "http delete urlacl url=`"$target`"" -NoNewWindow -Wait -PassThru -WindowStyle Hidden
  $exit = $proc.ExitCode
  if ($exit -eq 0) {
    Write-Log "Deletion command returned exit code 0 (success)."
    Write-Host "Deletion attempted. Verify with 'netsh http show urlacl'."
  } else {
    Write-Log "Deletion command returned exit code $exit."
    Write-Host "Deletion command returned exit code $exit. See log for details." -ForegroundColor Yellow
  }
} catch {
  Write-Log "Exception while running delete command: $($_.Exception.Message)"
  Write-Host "Error while attempting deletion: $($_.Exception.Message)" -ForegroundColor Red
}

# Final verification
Write-Host "`nVerifying current urlacl entries:`n"
netsh http show urlacl

Write-Log "Completed. See $logFile for details."
$global:LogLines | Out-File -FilePath $logFile -Encoding UTF8
Write-Host "`nLog saved to $logFile"
