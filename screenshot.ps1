Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
$hwnd = [IntPtr]4589934
$rect = New-Object Win32+RECT
[Win32]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
$w = $rect.Right - $rect.Left
$h = $rect.Bottom - $rect.Top
Write-Host "Window size: $w x $h"
if ($w -gt 0 -and $h -gt 0) {
    $bmp = New-Object System.Drawing.Bitmap $w, $h
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($rect.Left, $rect.Top, 0, 0, (New-Object System.Drawing.Size $w, $h))
    $bmp.Save("C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\thunder_screen.png")
    $g.Dispose()
    $bmp.Dispose()
    Write-Host "Screenshot saved to thunder_screen.png"
} else {
    Write-Host "Invalid window dimensions"
}
