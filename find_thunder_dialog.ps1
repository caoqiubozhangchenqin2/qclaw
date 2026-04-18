Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Collections.Generic;
using System.Diagnostics;
public class TK {
    [DllImport("user32.dll")] public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll")] public static extern IntPtr FindWindowEx(IntPtr hwndParent, IntPtr hwndChildAfter, string lpszClass, string lpszWindow);
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);
    public delegate bool WinEnumProc(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool EnumWindows(WinEnumProc lpEnumFunc, IntPtr lParam);
    public const int WM_GETTEXT = 0x000D;
    public const int WM_GETTEXTLENGTH = 0x000E;
    public const int BM_CLICK = 0x00F5;
    public const int WM_SETTEXT = 0x000C;
    public const int WM_LBUTTONDOWN = 0x0201;
    public const int WM_LBUTTONUP = 0x0202;
    public const int LVM_GETITEMCOUNT = 0x1004;
    public const int LVM_GETITEMTEXT = 0x102B;
    public const int LVM_GETSELECTIONMARK = 0x005E;
    public const int LVM_GETNEXTITEM = 0x4000 + 12;
    public const int LVM_GETITEMSTATE = 0x4000 + 44;
    public const int LVM_SETITEMSTATE = 0x4000 + 43;
    public const int LVNI_SELECTED = 0x0002;
    public const int LVIS_SELECTED = 0x0002;
    public const int CB_GETCOUNT = 0x146;
    public const int CB_GETLBTEXT = 0x148;
    public const int TB_BUTTONCOUNT = 0x400 + 0;
    public const int TB_GETBUTTON = 0x400 + 23;
    public const int TB_GETITEMRECT = 0x400 + 29;
    [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
    [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
    public class LVITEM { public int mask; public int iItem; public int iSubItem; public int state; public int stateMask; [MarshalAs(UnmanagedType.LPTStr)] public string pszText; public int cchTextMax; public int iImage; public IntPtr lParam; public int iIndent; public int iGroupId; public int cColumns; public IntPtr puColumns; public int piColFmt; public int iGroup; }
}
public class TKUtil {
    public static string GetText(IntPtr h) {
        var sb = new StringBuilder(1024);
        TK.GetWindowText(h, sb, 1024); return sb.ToString();
    }
    public static string GetClass(IntPtr h) {
        var sb = new StringBuilder(256);
        TK.GetClassName(h, sb, 256); return sb.ToString();
    }
    public static void DumpWin(IntPtr h, int depth=0) {
        if (h == IntPtr.Zero) return;
        var cls = GetClass(h); var txt = GetText(h);
        var pref = new string(' ', depth*2);
        Console.WriteLine($"{pref}[0x{h.ToInt64():X8}] {cls} \"{txt}\"");
        var ch = TK.FindWindowEx(h, IntPtr.Zero, null, null);
        while (ch != IntPtr.Zero) { DumpWin(ch, depth+1); ch = TK.FindWindowEx(h, ch, null, null); }
    }
}
"@

# Find all windows via EnumWindows
$all = @{}
$cb = [TK+WinEnumProc]{ param($h,$p); $cls=[TKUtil]::GetClass($h); $txt=[TKUtil]::GetText($h); if($txt){$G:all[$h]="$cls :: $txt"}; return $true }
[TK]::EnumWindows($cb, [IntPtr]::Zero)

# Show Thunder-related windows
Write-Host "=== Thunder-related windows ==="
$thunder = @()
foreach ($kv in $all.GetEnumerator()) {
    $v = $kv.Value
    if ($v -match "Thunder|TXGui|ATOM|download|Download|Downloader|NewDown") {
        Write-Host "[$($kv.Key.ToInt64().ToString('X8'))] $v"
        $thunder += $kv.Key
    }
}

# Also scan by process
Write-Host "`n=== Thunder process windows ==="
Get-Process -Name "Thunder" -ErrorAction SilentlyContinue | % {
    Write-Host "PID=$($_.Id) Title=$($_.MainWindowTitle)"
    # Get all windows of this process via EnumWindows
    foreach ($kv in $all.GetEnumerator()) {
        $pid = 0; [TKUtil]::GetWindowThreadProcessId($kv.Key, [ref]$pid) | Out-Null
        if ($pid -eq $_.Id) {
            Write-Host "  [$($kv.Key.ToInt64().ToString('X8'))] $($kv.Value)"
        }
    }
}

# If we found a download dialog, dump its children
if ($thunder.Count -gt 0) {
    foreach ($h in $thunder) {
        Write-Host "`n=== Children of $($h.ToInt64().ToString('X8')) ==="
        [TKUtil]::DumpWin($h, 0)
    }
}
