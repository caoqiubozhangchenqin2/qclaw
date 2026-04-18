import win32gui
import win32api
import win32con
import time
import ctypes

# Send keystrokes using Windows API
def press_enter():
    """Simulate pressing Enter key"""
    ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)  # Key down
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)  # Key up
    time.sleep(0.1)

def send_enter():
    """Send Enter key to active window"""
    ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)

def find_qbt_window():
    """Find qBittorrent window"""
    result = [None]
    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if 'qBittorrent' in title:
                result[0] = hwnd
                return False
        return True
    win32gui.EnumWindows(enum_callback, None)
    return result[0]

# Find and activate qBittorrent
hwnd = find_qbt_window()
if hwnd:
    print(f"Found qBittorrent window, bringing to front...")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    # Press Enter multiple times to confirm dialogs
    print("Pressing Enter 20 times to confirm dialogs...")
    for i in range(20):
        send_enter()
        time.sleep(0.8)
        print(f"  {i+1}/20")
    
    print("\nDone! Check if all dialogs are confirmed.")
else:
    print("qBittorrent window not found!")
