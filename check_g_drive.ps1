# Check G drive
$g = Get-PSDrive G -ErrorAction SilentlyContinue
if ($g) {
    Write-Host "G: drive exists"
    Write-Host "Root: $($g.Root)"
    Write-Host "Free: $([math]::Round($g.Free/1GB,2)) GB"
    # List folders
    $folders = Get-ChildItem G:\ -Directory -ErrorAction SilentlyContinue | Select-Object -First 10 Name
    if ($folders) {
        Write-Host "`nFolders on G:"
        $folders | Format-Table -AutoSize
    }
} else {
    Write-Host "G: drive not found"
}
