Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")] public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll")] public static extern IntPtr FindWindowEx(IntPtr hWnd, IntPtr hWndAfter, string lpszClass, string lpszWindow);
    [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@

$w = [Win32]::FindWindow($null, 'mudr-363ch - TorrentKitty - Google Chrome')
if ($w -eq [IntPtr]::Zero) {
    Write-Host 'Not found'
    Get-Process chrome -ErrorAction SilentlyContinue | ForEach-Object { $_.MainWindowTitle } | Select-Object -First 5
} else {
    Write-Host "Found: $w"
}
