import win32gui, win32con, win32process, ctypes

def get_text(hwnd):
    try:
        n = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
        if n == 0: return ''
        buf = win32gui.PyGetString(hwnd, n + 1)
        return buf.rstrip('\x00')
    except: return ''

def get_cls(hwnd):
    try: return win32gui.GetClassName(hwnd)
    except: return ''

def get_pid(hwnd):
    try: return win32process.GetWindowThreadProcessId(hwnd)[1]
    except: return 0

results = []
def cb(hwnd, _):
    try:
        if not win32gui.IsWindowVisible(hwnd): return True
        txt = get_text(hwnd)
        cls = get_cls(hwnd)
        pid = get_pid(hwnd)
        results.append((hwnd, cls, txt, pid))
    except: pass
    return True

print("Scanning all windows...")
win32gui.EnumWindows(cb, None)
print(f"Found {len(results)} windows\n")

print("--- Top level Chrome/Thunder windows ---")
for hwnd, cls, txt, pid in sorted(results, key=lambda x: x[1]):
    if any(k in cls for k in ['Chrome', 'Thunder', 'TXGui', 'ATOM', 'Mozilla', 'Firefox', 'IEFrame']):
        print(f"  0x{int(hwnd):08X} [{cls}] pid={pid} '{txt[:60]}'")

print("\n--- All windows with non-empty text (first 50) ---")
shown = 0
for hwnd, cls, txt, pid in sorted(results, key=lambda x: -len(x[2])):
    if txt and shown < 50:
        print(f"  0x{int(hwnd):08X} [{cls}] pid={pid} '{txt[:80]}'")
        shown += 1

print("\n--- ListView windows ---")
for hwnd, cls, txt, pid in results:
    if 'SysListView' in cls:
        try:
            cnt = win32gui.SendMessage(hwnd, win32con.LVM_GETITEMCOUNT, 0, 0)
        except: cnt = -1
        print(f"  0x{int(hwnd):08X} ListView pid={pid} items={cnt} '{txt[:50]}'")

print("\n--- All processes named 'Thunder' ---")
import subprocess
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Thunder.exe', '/FO', 'CSV', '/NH'], capture_output=True, text=True)
print(r.stdout)
