Write-Host "=== Checking qBittorrent ==="

$found = $false

# Check if installed
$paths = @(
    "C:\Program Files\qBittorrent\qbittorrent.exe",
    "C:\Program Files (x86)\qBittorrent\qbittorrent.exe",
    "C:\Program Files\qBittorrent\qbittorrent-nox.exe",
    "C:\Users\Administrator\AppData\Local\qBittorrent\qbittorrent.exe"
)

foreach ($p in $paths) {
    if (Test-Path $p) {
        Write-Host "Found: $p"
        $found = $true
    }
}

# Check PATH
$qt = (Get-Command qbittorrent -ErrorAction SilentlyContinue)
if ($qt) {
    Write-Host "In PATH: $($qt.Source)"
    $found = $true
}

if (-not $found) {
    Write-Host "qBittorrent not found - need to install"
}

# Check winget availability
$wg = (Get-Command winget -ErrorAction SilentlyContinue)
if ($wg) {
    Write-Host "winget available at: $($wg.Source)"
} else {
    Write-Host "winget NOT found"
}
