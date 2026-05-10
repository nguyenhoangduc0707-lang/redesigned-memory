# Script test toàn bộ endpoint của AI_OS_KERNEL_V3
$baseUrl = "http://127.0.0.1:8080"

$endpoints = @(
    "/ping",
    "/run",
    "/execute/test",
    "/safe-check",
    "/contract-info",
    "/engine-run",
    "/schedule/demo",
    "/firewall"
)

Write-Host "🚀 Bắt đầu test API tại $baseUrl"

foreach ($ep in $endpoints) {
    $url = "$baseUrl$ep"
    try {
        $response = Invoke-RestMethod -Uri $url -Method Get
        Write-Host "✅ $ep -> $($response | ConvertTo-Json -Compress)"
    }
    catch {
        Write-Host "❌ $ep lỗi: $($_.Exception.Message)"
    }
}
