import win32gui
import win32con
import time

def find_thunder_window():
    """Find Thunder main window"""
    result = []
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        if 'thunder' in title.lower() or '迅雷' in title or 'xunlei' in title.lower():
            result.append((hwnd, title, class_name))
        elif 'thunder' in class_name.lower() or 'xunlei' in class_name.lower():
            result.append((hwnd, title, class_name))
        return True
    win32gui.EnumWindows(callback, None)
    return result

def find_child_windows(hwnd, keywords):
    """Find child windows matching keywords"""
    result = []
    def callback(child_hwnd, _):
        title = win32gui.GetWindowText(child_hwnd)
        class_name = win32gui.GetClassName(child_hwnd)
        for kw in keywords:
            if kw.lower() in title.lower() or kw.lower() in class_name.lower():
                result.append((child_hwnd, title, class_name))
                break
        return True
    win32gui.EnumChildWindows(hwnd, callback, None)
    return result

def click_button(hwnd):
    """Click a button by sending messages"""
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    # Send click message
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)

def main():
    print("Finding Thunder windows...")
    windows = find_thunder_window()
    if not windows:
        print("No Thunder window found!")
        return
    
    for hwnd, title, class_name in windows:
        print(f"Found: hwnd={hwnd}, title='{title}', class='{class_name}'")
        
        # Find child windows with button-like names
        keywords = ['立即下载', 'download', 'button', 'btn', 'download']
        children = find_child_windows(hwnd, keywords)
        print(f"Child windows matching keywords: {len(children)}")
        for child_hwnd, child_title, child_class in children:
            print(f"  Child: hwnd={child_hwnd}, title='{child_title}', class='{child_class}'")

if __name__ == '__main__':
    main()
