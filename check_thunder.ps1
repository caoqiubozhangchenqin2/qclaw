Add-Type -AssemblyName UIAutomationClient
$proc = Get-Process Thunder -ErrorAction SilentlyContinue | Select-Object -First 1
if ($proc) {
    Write-Host "Thunder PID:" $proc.Id
    $hwnd = $proc.MainWindowHandle
    Write-Host "Window Handle:" $hwnd
    Write-Host "Window Title:" $proc.MainWindowTitle
} else {
    Write-Host "Thunder not found"
}
