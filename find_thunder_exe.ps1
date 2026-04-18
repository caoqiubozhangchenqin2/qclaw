$thunderPaths = @(
    "C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe",
    "C:\Program Files\Thunder Network\Thunder\Program\Thunder.exe",
    "C:\Program Files (x86)\Xunlei\Thunder\Program\Thunder.exe",
    "C:\Program Files\Xunlei\Thunder\Program\Thunder.exe",
    "${env:LOCALAPPDATA}\Thunder Network\Thunder\Program\Thunder.exe",
    "${env:PROGRAMFILES}\Thunder\Program\Thunder.exe"
)
foreach ($p in $thunderPaths) {
    $expanded = $ExecutionContext.InvokeCommand.ExpandString($p)
    if (Test-Path $expanded) {
        Write-Host "Found: $expanded"
        $f = Get-Item $expanded
        Write-Host "Size: $([math]::Round($f.Length/1MB,2)) MB, Modified: $($f.LastWriteTime)"
    }
}
# Also search in registry
$reg = Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName -like "*迅雷*" -or $_.DisplayName -like "*Thunder*" }
if ($reg) {
    Write-Host "`nRegistry uninstall entries:"
    $reg | ForEach-Object { Write-Host "$($_.DisplayName) -> $($_.InstallLocation)" }
}
