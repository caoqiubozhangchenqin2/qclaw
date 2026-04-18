import win32gui
import win32con

def print_window_tree(hwnd, indent=0):
    """Print window tree structure"""
    title = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    rect = win32gui.GetWindowRect(hwnd)
    
    prefix = "  " * indent
    print(f"{prefix}[{class_name}] '{title[:30]}' @ {rect}")
    
    # Enumerate child windows
    def enum_child(child_hwnd, extra):
        print_window_tree(child_hwnd, indent + 1)
        return True
    
    try:
        win32gui.EnumChildWindows(hwnd, enum_child, None)
    except:
        pass

# Find qBittorrent main window
def find_qbt_main():
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

hwnd = find_qbt_main()
if hwnd:
    print(f"qBittorrent window structure:\n")
    print_window_tree(hwnd)
else:
    print("qBittorrent not found")
