Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinMsg {
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll")]
    public static extern IntPtr FindWindowEx(IntPtr parent, IntPtr after, string className, string windowName);
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern IntPtr SendMessage(IntPtr hWnd, int Msg, IntPtr wParam, IntPtr lParam);
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out POINT lpPoint);
    [StructLayout(LayoutKind.Sequential)]
    public struct POINT { public int X; public int Y; }
    public const int WM_KEYDOWN = 0x0100;
    public const int WM_KEYUP = 0x0101;
    public const int WM_LBUTTONDOWN = 0x0201;
    public const int WM_LBUTTONUP = 0x0202;
    public const byte VK_SPACE = 0x20;
    public const byte VK_TAB = 0x09;
    public const byte VK_DOWN = 0x28;
    public const uint KEYEVENTF_KEYUP = 0x0002;
}
"@

# First, find the dialog
$dialogHwnd = [WinMsg]::FindWindow("Chrome_WidgetWin_0", "新建任务面板")
if ($dialogHwnd -eq [IntPtr]::Zero) {
    Write-Host "Dialog not found"
} else {
    Write-Host "Found dialog HWND: $dialogHwnd"
    [WinMsg]::SetForegroundWindow($dialogHwnd) | Out-Null
    Start-Sleep -Milliseconds 200
    
    # Dialog is at (660,196) size 600x648
    # Usually in such dialogs:
    # - File list starts around y=350-400
    # - Checkboxes might be around x=680
    # - "立即下载" button is typically bottom area around y=700-780
    # - "仅下载勾选" checkbox might be in the middle
    
    # Let's click in the center of the dialog first to focus it
    $cx = 660 + 300  # center x
    $cy = 196 + 324  # center y
    Write-Host "Clicking center of dialog ($cx, $cy)"
    
    # Click
    [WinMsg]::SetCursorPos($cx, $cy) | Out-Null
    Start-Sleep -Milliseconds 100
    [WinMsg]::SendMessage($dialogHwnd, [WinMsg]::WM_LBUTTONDOWN, [IntPtr]::Zero, [IntPtr](($cy -shl 16) -bor ($cx -band 0xFFFF))) | Out-Null
    Start-Sleep -Milliseconds 50
    [WinMsg]::SendMessage($dialogHwnd, [WinMsg]::WM_LBUTTONUP, [IntPtr]::Zero, [IntPtr](($cy -shl 16) -bor ($cx -band 0xFFFF))) | Out-Null
    
    Start-Sleep -Milliseconds 300
    
    # Try pressing Tab a few times to cycle through elements
    for ($i = 0; $i -lt 5; $i++) {
        [WinMsg]::keybd_event([WinMsg]::VK_TAB, 0, 0, [UIntPtr]::Zero) | Out-Null
        Start-Sleep -Milliseconds 100
        [WinMsg]::keybd_event([WinMsg]::VK_TAB, 0, [WinMsg]::KEYEVENTF_KEYUP, [UIntPtr]::Zero) | Out-Null
    }
    
    Write-Host "Tried focusing with Tab"
}
