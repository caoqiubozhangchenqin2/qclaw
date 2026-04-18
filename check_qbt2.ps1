# Check if port 8080 is listening
$conn = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue
if ($conn) {
    Write-Host "Port 8080 in use:"
    $conn | Format-Table LocalAddress,LocalPort,State -AutoSize
} else {
    Write-Host "Port 8080 not listening"
}

# Check qBittorrent config
$cfg = "$env:APPDATA\qBittorrent\qBittorrent.ini"
if (Test-Path $cfg) {
    Write-Host "Config found: $cfg"
    Write-Host "Size: $((Get-Item $cfg).Length) bytes"
    # Print relevant sections
    $content = Get-Content $cfg -Raw
    $lines = $content -split "`n" | Where-Object { $_ -match 'WebUI|webui|Port|localhost|Login|password' }
    if ($lines) {
        Write-Host "WebUI-related:"
        $lines | ForEach-Object { Write-Host $_ }
    }
} else {
    Write-Host "Config not yet created"
    Get-ChildItem "$env:APPDATA\qBittorrent" -ErrorAction SilentlyContinue | Format-Table Name -AutoSize
}
