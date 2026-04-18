import win32gui
import win32api
import win32con
import ctypes
import time

# Get Thunder window rect
hwnd = 9834534
rect = win32gui.GetWindowRect(hwnd)
left, top, right, bottom = rect
width = right - left
height = bottom - top

print(f"Thunder window: left={left}, top={top}, width={width}, height={height}")

# Click at bottom center (button is at bottom)
click_x = left + width // 2
click_y = bottom - 40  # 40 pixels from bottom

print(f"Clicking at ({click_x}, {click_y})")

# Bring window to foreground first
win32gui.SetForegroundWindow(hwnd)
time.sleep(0.3)

# Move mouse and click
ctypes.windll.user32.SetCursorPos(click_x, click_y)
time.sleep(0.1)

# Mouse down and up
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
time.sleep(0.05)
ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

print("Clicked!")
