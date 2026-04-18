import win32gui
import ctypes
import time

hwnd = 4589934
rect = win32gui.GetWindowRect(hwnd)
left, top, right, bottom = rect
width = right - left
height = bottom - top

print(f"Window: left={left}, top={top}, width={width}, height={height}")

# Click at bottom center (立即下载 button)
click_x = left + width // 2
click_y = bottom - 50  # 50 pixels from bottom

print(f"Clicking at ({click_x}, {click_y})")

# Bring to foreground
try:
    win32gui.SetForegroundWindow(hwnd)
except:
    pass
time.sleep(0.3)

# Move and click
ctypes.windll.user32.SetCursorPos(click_x, click_y)
time.sleep(0.1)
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
time.sleep(0.05)
ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

print("Clicked!")
