import win32gui
import ctypes
import time

def find_visible_thunder_windows():
    """Find all visible Thunder windows"""
    result = []
    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top
        if width < 100 or height < 100:
            return True  # Skip small windows
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if '迅雷' in title or 'thunder' in title.lower() or 'thunder' in class_name.lower():
            result.append({
                'hwnd': hwnd,
                'title': title,
                'class': class_name,
                'left': left,
                'top': top,
                'width': width,
                'height': height
            })
        return True
    win32gui.EnumWindows(callback, None)
    return result

def click_at(x, y):
    """Click at screen coordinates"""
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.1)
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# Find visible Thunder windows
windows = find_visible_thunder_windows()
print(f"Found {len(windows)} visible Thunder windows:")
for w in windows:
    print(f"  hwnd={w['hwnd']}, title='{w['title']}', size={w['width']}x{w['height']}, pos=({w['left']}, {w['top']})")

if windows:
    # Use the largest window (likely the main one)
    main_win = max(windows, key=lambda w: w['width'] * w['height'])
    print(f"\nUsing main window: {main_win['title']}")
    
    # Click at bottom center
    click_x = main_win['left'] + main_win['width'] // 2
    click_y = main_win['top'] + main_win['height'] - 50
    
    print(f"Clicking at ({click_x}, {click_y})...")
    click_at(click_x, click_y)
    print("Done!")
else:
    print("No visible Thunder windows found!")
