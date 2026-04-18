import win32gui
import win32con
import time
import ctypes

# Bring Thunder window to foreground
hwnd = 9834534  # Thunder main window

print("Bringing Thunder to foreground...")
win32gui.SetForegroundWindow(hwnd)
time.sleep(0.5)

# Method 1: Try pressing Enter (might work if button has focus)
print("Pressing Enter...")
ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)  # Enter down
time.sleep(0.05)
ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)  # Enter up

print("Done! Check if download started.")
