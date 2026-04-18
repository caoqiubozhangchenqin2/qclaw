$thunderPaths = @(
    "C:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe",
    "C:\Program Files\Thunder Network\Thunder\Program\Thunder.exe",
    "C:\Program Files (x86)\Xunlei\Thunder\Program\Thunder.exe",
    "C:\Program Files\Xunlei\Thunder\Program\Thunder.exe",
    "${env:LOCALAPPDATA}\Thunder Network\Thunder\Program\Thunder.exe",
    "${env:PROGRAMFILES}\Thunder\Program\Thunder.exe"
)
$found = $null
foreach ($p in $thunderPaths) {
    $expanded = $ExecutionContext.InvokeCommand.ExpandString($p)
    if (Test-Path $expanded) {
        $found = $expanded
        Write-Host "Found Thunder: $found"
        break
    }
}
if (-not $found) {
    Write-Host "Thunder not found in common paths, searching..."
    $found = Get-ChildItem -Path "C:\Program Files*" -Recurse -Filter "Thunder.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName
    if ($found) {
        Write-Host "Found: $found"
    }
}
if ($found) {
    # Register magnet protocol
    $regPath = "HKCU:\Software\Classes\magnet\shell\open\command"
    Set-ItemProperty -Path $regPath -Name "(Default)" -Value "`"$found`" `"%1`"" -Force -ErrorAction SilentlyContinue
    if (-not (Test-Path "HKCU:\Software\Classes\magnet")) {
        New-Item -Path "HKCU:\Software\Classes\magnet" -Force | Out-Null
        Set-ItemProperty -Path "HKCU:\Software\Classes\magnet" -Name "(Default)" -Value "URL:Magnet Protocol" -Force
        New-Item -Path "HKCU:\Software\Classes\magnet\shell\open\command" -Force | Out-Null
        Set-ItemProperty -Path "HKCU:\Software\Classes\magnet\shell\open\command" -Name "(Default)" -Value "`"$found`" `"%1`"" -Force
    }
    Write-Host "Magnet protocol registered to Thunder!"
} else {
    Write-Host "Thunder not found! Please check if it's installed."
}
