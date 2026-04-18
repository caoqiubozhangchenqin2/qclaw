import subprocess, re, time

# Try to find pywin32
try:
    import win32gui, win32con, win32api, ctypes
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False
    print("win32gui not found, using PowerShell fallback")
    # Use PowerShell EnumWindows via subprocess
    ps = r'''
Add-Type @" 
using System;
using System.Runtime.InteropServices;
using System.Text;
using System.Collections.Generic;
public class Win32 {
    [DllImport("user32.dll")] public static extern bool EnumWindows(WNDENUMPROC lpEnumFunc, IntPtr lParam);
    public delegate bool WNDENUMPROC(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern IntPtr GetShellWindow();
    public const int GWL_STYLE = -16;
    public const int GWL_EXSTYLE = -20;
    public const int WM_GETTEXT = 0x000D;
    public const int WM_GETTEXTLENGTH = 0x000E;
    [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetClassName(IntPtr hWnd, StringBuilder lpClassName, int nMaxCount);
    [DllImport("user32.dll")] public static extern int GetWindowLong(IntPtr hWnd, int nIndex);
    [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
}
public class WinResult {
    public static List<string> results = new List<string>();
    public static bool Callback(IntPtr hWnd, IntPtr lParam) {
        if (!Win32.IsWindowVisible(hWnd)) return true;
        uint pid = 0; Win32.GetWindowThreadProcessId(hWnd, out pid);
        int style = Win32.GetWindowLong(hWnd, Win32.GWL_STYLE);
        int exstyle = Win32.GetWindowLong(hWnd, Win32.GWL_EXSTYLE);
        int len = Win32.SendMessage(hWnd, Win32.WM_GETTEXTLENGTH, IntPtr.Zero, IntPtr.Zero);
        string txt = ""; if (len > 0) {
            var sb = new StringBuilder(len+1);
            Win32.SendMessage(hWnd, Win32.WM_GETTEXT, (IntPtr)(len+1), sb);
            txt = sb.ToString();
        }
        var cls = new StringBuilder(256);
        Win32.GetClassName(hWnd, cls, 256);
        if (pid > 0 || txt.Length > 0 || cls.ToString().Contains("Thunder") || cls.ToString().Contains("TXGui") || cls.ToString().Contains("List") || cls.ToString().Contains("Combo") || cls.ToString().Contains("Button") || cls.ToString().Contains("Edit")) {
            results.Add(string.Format("0x{0:X8} [{1}] pid={2} style=0x{3:X} ex=0x{4:X} \"{5}\"", hWnd.ToInt64(), cls, pid, style, exstyle, txt.Replace("\\n","~").Replace("\\r","~")));
        }
        return true;
    }
}
"@
$cb = [WinResult+Callback]{ param($h,$p) [WinResult]::Callback($h, $p) }
[Win32]::EnumWindows($cb, [IntPtr]::Zero)
$results = [WinResult]::results
$results | Sort-Object
'''
    result = subprocess.run(['powershell', '-Command', ps], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr[:500])
    exit(0)

if not HAS_WIN32:
    exit(1)

def get_window_text(hwnd):
    try:
        length = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        if length == 0:
            return ''
        buf = win32gui.PyGetString(hwnd, length + 1)
        return buf.rstrip('\x00')
    except:
        return ''

def get_class_name(hwnd):
    try:
        return win32gui.GetClassName(hwnd)
    except:
        return ''

def get_pid(hwnd):
    try:
        import win32process
        return win32process.GetWindowThreadProcessId(hwnd)[1]
    except:
        return 0

def is_thunder_related(hwnd, txt, cls):
    pid = get_pid(hwnd)
    keywords = ['thunder', 'txgui', 'download', 'atom', 'select', 'task', 'file', 'save', 'folder', 'path', 'confirm', 'ok', 'cancel']
    if any(k in (txt+cls).lower() for k in keywords):
        return True
    if cls in ('SysListView32', 'SysTreeView32', 'ComboBox', 'ComboBoxEx32', 'Static', 'Button', 'Edit'):
        return True
    return False

results = []

def callback(hwnd, extra):
    try:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        txt = get_window_text(hwnd)
        cls = get_class_name(hwnd)
        pid = get_pid(hwnd)
        if pid > 0 or txt or cls:
            if 'Thunder' in cls or 'TXGui' in cls or 'ATOM' in cls:
                results.append((hwnd, cls, txt, pid))
    except:
        pass
    return True

# Enum all top-level windows
win32gui.EnumWindows(callback, None)

# Filter Thunder-related
print("=== Thunder-related windows ===")
for hwnd, cls, txt, pid in sorted(results, key=lambda x: x[1]):
    hwnd_int = int(hwnd)
    print(f"0x{hwnd_int:08X} [{cls}] pid={pid} '{txt[:60]}'")

# Now try to find the specific download dialog by searching all windows
print("\n=== Looking for ListView/ComboBox with file names ===")
all_windows = []
def all_cb(hwnd, lst):
    try:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        txt = get_window_text(hwnd)
        cls = get_class_name(hwnd)
        pid = get_pid(hwnd)
        if txt and any(ext in txt.lower() for ext in ['.mp4', '.wmv', '.avi', '.mkv', '.flv', 'webm']):
            lst.append((hwnd, cls, txt, pid))
    except:
        pass
    return True

win32gui.EnumWindows(all_cb, all_windows)
for hwnd, cls, txt, pid in sorted(all_windows, key=lambda x: x[1]):
    print(f"0x{int(hwnd):08X} [{cls}] pid={pid} '{txt[:80]}'")

# Try finding the download dialog that contains a ListView
print("\n=== ListView windows (likely file lists) ===")
lv_windows = []
def lv_cb(hwnd, lst):
    try:
        cls = get_class_name(hwnd)
        if 'SysListView32' in cls:
            pid = get_pid(hwnd)
            txt = get_window_text(hwnd)
            count = win32gui.SendMessage(hwnd, win32con.LVM_GETITEMCOUNT, 0, 0)
            lst.append((hwnd, pid, count, txt))
    except:
        pass
    return True

win32gui.EnumWindows(lv_cb, lv_windows)
for hwnd, pid, count, txt in sorted(lv_windows, key=lambda x: x[2], reverse=True):
    print(f"0x{int(hwnd):08X} ListView pid={pid} items={count} '{txt[:50]}'")
