# Find Chrome debugging port
Get-CdpPort 8080 | Select-Object -First 1

$proc = Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match '--remote-debugging-port=(\d+)' } | Select-Object -First 1
if ($proc) {
    $port = [regex]::Match($proc.CommandLine, '--remote-debugging-port=(\d+)').Groups[1].Value
    Write-Host "Chrome debug port: $port"
    try {
        $r = Invoke-RestMethod "http://localhost:$port/json" -TimeoutSec 3
        Write-Host "Tabs:"
        $r | ForEach-Object { Write-Host "  $($_.title) -> $($_.id)" }
    } catch {
        Write-Host "Failed to connect: $_"
    }
} else {
    Write-Host "No Chrome with debug port found"
    # Try common ports
    9222, 9223, 9333 | ForEach-Object {
        try {
            $r = Invoke-RestMethod "http://localhost:$_/json" -TimeoutSec 2
            Write-Host "Found on port: $_"
            $r | ForEach-Object { Write-Host "  $($_.title)" }
        } catch {}
    }
}
