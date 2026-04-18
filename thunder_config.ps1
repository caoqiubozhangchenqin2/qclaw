# Find Thunder config files
$thunderPath = "C:\Users\Administrator\AppData\Roaming\Thunder"
if (Test-Path $thunderPath) {
    Write-Host "=== Thunder Roaming files ==="
    Get-ChildItem $thunderPath -File | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
    Write-Host "`n=== Thunder directories ==="
    Get-ChildItem $thunderPath -Directory | Select-Object Name
} else {
    Write-Host "Thunder path not found"
}

# Also check ProgramData
$pd = "C:\ProgramData\Thunder\Network"
if (Test-Path $pd) {
    Write-Host "`n=== ProgramData Thunder ==="
    Get-ChildItem $pd -File | Select-Object Name, Length | Format-Table -AutoSize
} else {
    Write-Host "ProgramData Thunder not found"
}

# Check local thunder
$localT = "C:\Users\Administrator\AppData\Local\Thunder"
if (Test-Path $localT) {
    Write-Host "`n=== Local Thunder files ==="
    Get-ChildItem $localT -File -Recurse 2>$null | Select-Object Name, Length | Sort-Object Length -Descending | Select-Object -First 20 | Format-Table -AutoSize
}
