$content = Get-Content 'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\mudr363_search.html' -Raw
# Find table or results section
$patterns = @('id="result"', 'class="result"', '<table', '<tr', 'id="share', 'class="share', 'onclick', 'magnet')
foreach ($p in $patterns) {
    $idx = $content.IndexOf($p)
    if ($idx -ge 0) {
        Write-Host "=== Found '$p' at $idx ==="
        $start = [Math]::Max(0, $idx-30)
        $len = [Math]::Min(200, $content.Length - $start)
        Write-Host $content.Substring($start, $len)
        Write-Host ""
    }
}
# Also look for the results container
$idx2 = $content.IndexOf('<main')
if ($idx2 -ge 0) {
    Write-Host "=== <main section ==="
    Write-Host $content.Substring($idx2, [Math]::Min(500, $content.Length - $idx2))
}
