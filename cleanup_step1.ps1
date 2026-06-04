[Console]::OutputEncoding = [Text.Encoding]::UTF8

# 1. Temp folders
$tempPaths = @($env:TEMP, 'C:\Windows\Temp')
foreach ($p in $tempPaths) {
    if (Test-Path $p) {
        $before = (Get-ChildItem $p -Recurse -Force -EA SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        Get-ChildItem $p -Recurse -Force -EA SilentlyContinue | Remove-Item -Recurse -Force -EA SilentlyContinue
        $after = (Get-ChildItem $p -Recurse -Force -EA SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $freed = [math]::Round(($before - $after)/1MB, 0)
        Write-Output "Temp $p : freed ${freed}MB"
    }
}

# 2. CrashDumps
$crash = 'C:\ProgramData\CrashDumps'
if (Test-Path $crash) {
    $before = (Get-ChildItem $crash -Recurse -Force -EA SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    Get-ChildItem $crash -Recurse -Force -EA SilentlyContinue | Remove-Item -Recurse -Force -EA SilentlyContinue
    Write-Output "CrashDumps : freed $([math]::Round($before/1MB,0))MB"
} else { Write-Output "No CrashDumps" }

# 3. Current free space
$free = [math]::Round((Get-PSDrive C).Free/1GB, 2)
Write-Output "Current C: free = ${free}GB"
