Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Collections.Generic;
public class Win32 {
    [DllImport("user32.dll")] public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll")] public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr hWnd, Win32.EnumCallback lpEnumFunc, IntPtr lParam);
    public delegate bool EnumCallback(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern int SendMessage(IntPtr hWnd, int Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")] public static extern int SendMessage(IntPtr hWnd, int Msg, IntPtr wParam, StringBuilder lParam);
    [DllImport("user32.dll")] public static extern int SendMessage(IntPtr hWnd, int Msg, IntPtr wParam, string lParam);
    public const int WM_GETTEXT = 0x000D;
    public const int WM_GETTEXTLENGTH = 0x000E;
    public const int BM_CLICK = 0x00F5;
    public const int LB_GETCOUNT = 0x018B;
    public const int LB_GETTEXT = 0x0189;
    public const int LB_GETTEXTLEN = 0x018A;
    public const int LB_GETCURSEL = 0x0188;
    public const int LB_SETCURSEL = 0x0186;
    public const int LVM_GETITEMCOUNT = 0x1004;
    public const int LVM_GETITEMTEXT = 0x102B;
    public const int LVM_GETSELECTEDCOLLECTION = 0x1093;
    public const int LVM_GETSELECTEDITEM = 0x100C;
    public const int TVM_GETITEMTEXT = 0x1100 + 13;
}
"@

function Get-WindowText($hwnd) {
    $len = [Win32]::SendMessage($hwnd, [Win32]::WM_GETTEXTLENGTH, [IntPtr]::Zero, [IntPtr]::Zero)
    if ($len -le 0) { return "" }
    $sb = New-Object System.Text.StringBuilder ($len + 2)
    [Win32]::SendMessage($hwnd, [Win32]::WM_GETTEXT, [IntPtr]::Zero, $sb) | Out-Null
    return $sb.ToString()
}

function Get-ClassName($hwnd) {
    $sb = New-Object System.Text.StringBuilder 256
    [Win32]::GetClassName($hwnd, $sb, 256) | Out-Null
    return $sb.ToString()
}

function Find-AllWindows($hwnd, $depth=0) {
    if ($hwnd -eq [IntPtr]::Zero) { return }
    $text = Get-WindowText $hwnd
    $cls = Get-ClassName $hwnd
    $prefix = "  " * $depth
    if ($text -or ($cls -match "SysListView|SysTreeView|Static|Button|Edit|ComboBox")) {
        Write-Host "$prefix[HWD=$($hwnd.ToInt64().ToString('X8'))] Class: $cls"
        if ($text) { Write-Host "$prefix  Text: $text" }
    }
    $child = [Win32]::FindWindowEx($hwnd, [IntPtr]::Zero, $null, $null)
    while ($child -ne [IntPtr]::Zero) {
        Find-AllWindows $child ($depth+1)
        $child = [Win32]::FindWindowEx($hwnd, $child, $null, $null)
    }
}

Write-Host "=== Thunder Windows ==="
# Find Thunder main and child windows
$allThunder = @()
$w = [Win32]::FindWindow("ThunderLoginUI.MainWindow.1", $null)
if ($w -ne [IntPtr]::Zero) { Write-Host "Found ThunderLogin: $($w.ToInt64().ToString('X8'))" }
$w = [Win32]::FindWindow("ATOM_MAIN_WINDOW", $null)
if ($w -ne [IntPtr]::Zero) { Write-Host "Found ATOM_MAIN: $($w.ToInt64().ToString('X8'))" }
$w = [Win32]::FindWindow("TXGuiFoundation.3", $null)
if ($w -ne [IntPtr]::Zero) { Write-Host "Found TXGuiFoundation: $($w.ToInt64().ToString('X8'))" }

# Try by process
$procs = Get-Process -Name "Thunder" -ErrorAction SilentlyContinue
foreach ($p in $procs) {
    Write-Host "Thunder process: PID=$($p.Id) $($p.MainWindowTitle)"
    $mainWin = $p.MainWindowHandle
    if ($mainWin -ne [IntPtr]::Zero) {
        $title = Get-WindowText $mainWin
        $cls = Get-ClassName $mainWin
        Write-Host "  Main HWND=$($mainWin.ToInt64().ToString('X8')) Class=$cls Title=$title"
        # Get all children of Thunder main window
        Write-Host "  --- Child windows ---"
        Find-AllWindows $mainWin 1
    }
}

# Also look for dialogs
Write-Host "`n=== Dialog Windows ==="
$dlgClasses = @("ThunderDownload", "ThunderAddTask", "ThunderNewDownWin", "DialogBoxClass", "TXGuiFoundation.6")
foreach ($c in $dlgClasses) {
    $w = [Win32]::FindWindow($c, $null)
    if ($w -ne [IntPtr]::Zero) {
        $title = Get-WindowText $w
        Write-Host "Found [$c]: HWND=$($w.ToInt64().ToString('X8')) Title=$title"
        Find-AllWindows $w 1
    }
}

# Try common dialog-like windows
Write-Host "`n=== All TXGuiFoundation windows ==="
$h = [Win32]::FindWindow("TXGuiFoundation.6", $null)
if ($h -ne [IntPtr]::Zero) {
    Write-Host "Found TXGuiFoundation.6 HWND=$($h.ToInt64().ToString('X8'))"
    Find-AllWindows $h 0
}
