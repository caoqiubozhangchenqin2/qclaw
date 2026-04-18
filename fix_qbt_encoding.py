import os

# Fix qBittorrent config with proper encoding
cfg_path = os.path.expandvars(r'%APPDATA%\qBittorrent\qBittorrent.ini')
dl_path = r'G:\迅雷下载'

with open(cfg_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the SavePath line
content = content.replace(r'Session\DefaultSavePath=G:迅雷下载', f'Session\\DefaultSavePath={dl_path}')

# Also check for other possible patterns
if 'SavePath=' in content and dl_path not in content:
    import re
    content = re.sub(r'SavePath=.*', f'SavePath={dl_path}', content)
    content = re.sub(r'DefaultSavePath=.*', f'DefaultSavePath={dl_path}', content)

with open(cfg_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed! SavePath set to: {dl_path}")
