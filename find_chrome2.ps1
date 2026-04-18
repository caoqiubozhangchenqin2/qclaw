Get-Process chrome -ErrorAction SilentlyContinue | ForEach-Object { "$($_.MainWindowTitle) [$($_.Id)]" }
