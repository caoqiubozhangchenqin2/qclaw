$content = Get-Content 'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\mudr363_search.html' -Raw
if ($content -match 'magnet') {
    Write-Host "Found magnet links"
    # Try to find the section around magnet
    $idx = $content.IndexOf('magnet')
    Write-Host $content.Substring([Math]::Max(0, $idx-50), [Math]::Min(300, $content.Length - [Math]::Max(0, $idx-50)))
} else {
    Write-Host "No magnet found in content"
    Write-Host "First 500 chars:"
    Write-Host $content.Substring(0, [Math]::Min(500, $content.Length))
}
