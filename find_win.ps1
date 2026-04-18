Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class WinInfo {
    [DllImport("user32.dll")]
    public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")]
    public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }
}
"@

$allWindows = @()

function Get-WindowText {
    param([IntPtr]$hwnd)
    $sb = New-Object System.Text.StringBuilder 256
    [WinInfo]::GetWindowText($hwnd, $sb, 256) | Out-Null
    return $sb.ToString()
}

function Get-ClassName {
    param([IntPtr]$hwnd)
    $sb = New-Object System.Text.StringBuilder 256
    [WinInfo]::GetClassName($hwnd, $sb, 256) | Out-Null
    return $sb.ToString()
}

$callback = {
    param([IntPtr]$hwnd, [IntPtr]$param)
    if ([WinInfo]::IsWindowVisible($hwnd)) {
        $title = Get-WindowText $hwnd
        $class = Get-ClassName $hwnd
        $rect = New-Object WinInfo+RECT
        [WinInfo]::GetWindowRect($hwnd, [ref]$rect) | Out-Null
        $w = $rect.Right - $rect.Left
        $h = $rect.Bottom - $rect.Top
        if ($w -gt 50 -and $h -gt 30 -and $title) {
            $script:allWindows += [PSCustomObject]@{
                HWND = $hwnd
                Title = $title
                Class = $class
                X = $rect.Left; Y = $rect.Top
                W = $w; H = $h
            }
        }
    }
    return $true
}

$delegate = [WinInfo+EnumWindowsProc]$callback
[WinInfo]::EnumWindows($delegate, [IntPtr]::Zero) | Out-Null

# Filter interesting windows
$thunder = $allWindows | Where-Object { $_.Title -match 'thunder|迅雷|SUJI|300|下载|悬浮' -or $_.Class -match 'thunder|Thunder' }
$allWindows | Format-Table -AutoSize | Out-String | Write-Host
Write-Host "`n--- Thunder-related: ---"
$thunder | Format-Table -AutoSize | Out-String | Write-Host
