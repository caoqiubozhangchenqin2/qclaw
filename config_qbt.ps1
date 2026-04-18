# Create download folder if not exists
$dlPath = "G:\迅雷下载"
if (-not (Test-Path $dlPath)) {
    New-Item -Path $dlPath -ItemType Directory -Force | Out-Null
    Write-Host "Created: $dlPath"
} else {
    Write-Host "Exists: $dlPath"
}

# Check qBittorrent config location
$qbtCfg = "$env:APPDATA\qBittorrent\qBittorrent.ini"
$qbtDir = Split-Path $qbtCfg -Parent

if (-not (Test-Path $qbtDir)) {
    New-Item -Path $qbtDir -ItemType Directory -Force | Out-Null
    Write-Host "Created qBittorrent config dir"
}

# Write config
$config = @"
[Preferences]
Downloads\SavePath=$dlPath
Downloads\TempPath=$dlPath\temp
Downloads\ScanDirsV2=@Invalid()
Downloads\ExcludedFileNames=
Connection\GlobalDLLimit=0
Connection\GlobalUPLimit=0
"@

if (Test-Path $qbtCfg) {
    # Update existing config
    $content = Get-Content $qbtCfg -Raw
    if ($content -notmatch 'SavePath') {
        Add-Content $qbtCfg $config
        Write-Host "Appended config"
    } else {
        # Update the SavePath line
        $content = $content -replace 'SavePath=.*', "SavePath=$dlPath"
        Set-Content $qbtCfg $content
        Write-Host "Updated SavePath"
    }
} else {
    # Create new config
    "[AutoRun]\n" + $config | Set-Content $qbtCfg
    Write-Host "Created new config"
}

Write-Host "`nDownload path set to: $dlPath"
Write-Host "Please restart qBittorrent to apply changes"
