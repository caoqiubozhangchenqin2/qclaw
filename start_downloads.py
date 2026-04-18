import win32gui
import win32api
import win32con
import time
import ctypes

def send_key(vk_code):
    """Send a key press"""
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)
    time.sleep(0.1)

def send_ctrl_a():
    """Ctrl+A to select all"""
    ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)  # Ctrl down
    ctypes.windll.user32.keybd_event(0x41, 0, 0, 0)  # A down
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x41, 0, 2, 0)  # A up
    ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)  # Ctrl up
    time.sleep(0.1)

def find_qbt_window():
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

hwnd = find_qbt_window()
if hwnd:
    print("Found qBittorrent, activating...")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    
    # Press Ctrl+A to select all torrents
    print("Selecting all torrents (Ctrl+A)...")
    send_ctrl_a()
    time.sleep(0.3)
    
    # Press Ctrl+U to force start (or just right arrow then Enter)
    # Actually, let's try pressing the Start button
    # In qBittorrent, you can use Ctrl+Shift+S to force start
    print("Force starting all (Ctrl+Shift+S)...")
    
    # Ctrl+Shift+S = Force Start
    ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)  # Ctrl down
    ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)  # Shift down
    ctypes.windll.user32.keybd_event(0x53, 0, 0, 0)  # S down
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(0x53, 0, 2, 0)  # S up
    ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)  # Shift up
    ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)  # Ctrl up
    
    print("Done! Check if downloads started.")
else:
    print("qBittorrent not found!")
