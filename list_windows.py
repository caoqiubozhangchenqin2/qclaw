import win32gui

def find_all_visible_windows():
    """Find all visible windows"""
    result = []
    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top
        if width < 200 or height < 100:
            return True  # Skip small windows
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        result.append({
            'hwnd': hwnd,
            'title': title,
            'class': class_name,
            'width': width,
            'height': height
        })
        return True
    win32gui.EnumWindows(callback, None)
    return sorted(result, key=lambda w: w['width'] * w['height'], reverse=True)

windows = find_all_visible_windows()
print(f"Found {len(windows)} visible windows:\n")
for w in windows[:15]:
    print(f"hwnd={w['hwnd']:8d} | {w['width']:4d}x{w['height']:4d} | {w['title']}")
