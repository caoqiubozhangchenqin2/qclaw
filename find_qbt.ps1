Write-Host "=== qBittorrent info ==="
$paths = @(
    "C:\Program Files\qBittorrent\qbittorrent.exe",
    "C:\Program Files (x86)\qBittorrent\qbittorrent.exe",
    "C:\Program Files\qBittorrent\qbittorrent-nox.exe"
)
foreach ($p in $paths) {
    if (Test-Path $p) {
        Write-Host "Found: $p"
        $f = Get-Item $p
        Write-Host "  Size: $([math]::Round($f.Length/1MB, 2)) MB"
        Write-Host "  Modified: $($f.LastWriteTime)"
    }
}

# qBittorrent config path
$cfg = "$env:APPDATA\qBittorrent\qBittorrent.ini"
if (Test-Path $cfg) {
    Write-Host "`nConfig exists: $cfg"
} else {
    Write-Host "`nConfig not found yet (qBittorrent not run yet)"
}

# Default WebUI port
Write-Host "`nDefault WebUI: http://localhost:8080"
Write-Host "Default credentials: admin / adminadmin"
