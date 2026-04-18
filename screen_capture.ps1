Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Capture full screen
$screen = [System.Windows.Forms.Screen]::PrimaryScreen
$bmp = New-Object System.Drawing.Bitmap $screen.Bounds.Width, $screen.Bounds.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($screen.Bounds.Location, (New-Object System.Drawing.Point 0, 0), $screen.Bounds.Size)
$bmp.Save("C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\full_screen.png")
$g.Dispose()
$bmp.Dispose()
Write-Host "Full screen captured:" $screen.Bounds.Width "x" $screen.Bounds.Height
