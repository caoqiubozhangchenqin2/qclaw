import win32gui
import win32con
import time
import ctypes

def press_key(vk):
    """Press and release a key"""
    ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk, 0, 2, 0)

def press_keys(keys):
    """Press multiple keys (like Alt+D)"""
    for k in keys:
        ctypes.windll.user32.keybd_event(k, 0, 0, 0)
    time.sleep(0.05)
    for k in reversed(keys):
        ctypes.windll.user32.keybd_event(k, 0, 2, 0)

# Virtual key codes
VK_MENU = 0x12  # Alt
VK_D = 0x44     # D

# Bring Thunder to foreground
hwnd = 9834534
print("Bringing Thunder to foreground...")
win32gui.SetForegroundWindow(hwnd)
time.sleep(0.5)

# Method 1: Alt+D
print("Trying Alt+D...")
press_keys([VK_MENU, VK_D])
time.sleep(1)

# Method 2: Tab multiple times then Enter
print("Trying Tab navigation...")
for i in range(10):
    ctypes.windll.user32.keybd_event(0x09, 0, 0, 0)  # Tab down
    ctypes.windll.user32.keybd_event(0x09, 0, 2, 0)  # Tab up
    time.sleep(0.1)

print("Pressing Enter...")
press_key(0x0D)  # Enter

print("Done!")
