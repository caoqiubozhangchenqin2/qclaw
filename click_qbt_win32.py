import win32gui
import win32api
import win32con
import time

def find_qbt_windows():
    """Find all qBittorrent windows"""
    windows = []
    
    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if 'qbittorrent' in title.lower() or 'qBittorrent' in class_name or '种子' in title or 'Torrent' in title:
                rect = win32gui.GetWindowRect(hwnd)
                windows.append({
                    'hwnd': hwnd,
                    'title': title,
                    'class': class_name,
                    'rect': rect
                })
        return True
    
    win32gui.EnumWindows(enum_callback, None)
    return windows

def click_at(hwnd, x, y):
    """Click at position relative to window"""
    # Bring window to front
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.2)
    
    # Get window rect for absolute position
    rect = win32gui.GetWindowRect(hwnd)
    abs_x = rect[0] + x
    abs_y = rect[1] + y
    
    # Move cursor and click
    win32api.SetCursorPos((abs_x, abs_y))
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)

# Find windows
windows = find_qbt_windows()
print(f"Found {len(windows)} qBittorrent-related windows")

for w in windows:
    print(f"  - [{w['class']}] {w['title'][:50]} @ {w['rect']}")

if not windows:
    print("No windows found! Let me check all windows...")
    # List all visible windows
    all_windows = []
    def enum_all(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                all_windows.append((hwnd, title[:60]))
        return True
    win32gui.EnumWindows(enum_all, None)
    print(f"\nAll visible windows ({len(all_windows)}):")
    for hwnd, title in all_windows[:20]:
        print(f"  - {title}")
else:
    # For each dialog, click the Download button (usually bottom-right)
    for w in windows:
        rect = w['rect']
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        
        print(f"\nProcessing: {w['title'][:40]} ({width}x{height})")
        
        # Click at bottom-right area (Download/OK button)
        click_x = width - 100  # 100px from right edge
        click_y = height - 40  # 40px from bottom
        
        print(f"  Clicking at ({click_x}, {click_y}) relative to window")
        click_at(w['hwnd'], click_x, click_y)
        time.sleep(0.8)
    
    print(f"\nClicked {len(windows)} windows!")
