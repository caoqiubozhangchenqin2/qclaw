import win32gui
import win32con
import time
import pyautogui

def find_qbt_windows():
    """Find all qBittorrent windows"""
    windows = []
    
    def enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            class_name = win32gui.GetClassName(hwnd)
            if 'qbittorrent' in title.lower() or 'qBittorrent' in class_name:
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

def click_download_button(hwnd):
    """Click the download/OK button in qBittorrent add torrent dialog"""
    # Bring window to front
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    
    # Get window rect
    rect = win32gui.GetWindowRect(hwnd)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    
    print(f"Window: {rect}, size: {width}x{height}")
    
    # For qBittorrent "Add torrent" dialog, the Download button is typically at bottom right
    # Try clicking near bottom right area
    click_x = rect[0] + width - 80
    click_y = rect[3] - 40
    
    print(f"Clicking at ({click_x}, {click_y})")
    pyautogui.click(click_x, click_y)
    time.sleep(0.5)

# Find windows
windows = find_qbt_windows()
print(f"Found {len(windows)} qBittorrent windows")

for w in windows:
    print(f"  - [{w['class']}] {w['title']} @ {w['rect']}")

if not windows:
    print("No qBittorrent windows found!")
else:
    # Click each window's download button
    for w in windows:
        print(f"\nProcessing: {w['title']}")
        click_download_button(w['hwnd'])
