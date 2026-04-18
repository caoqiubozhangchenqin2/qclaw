import winreg, os, glob, json

# Check Thunder Profiles dir
profile_path = r"C:\Users\Administrator\AppData\Roaming\Thunder\Profiles"
if os.path.exists(profile_path):
    print("=== Thunder Profiles ===")
    for root, dirs, files in os.walk(profile_path):
        for fn in files:
            fp = os.path.join(root, fn)
            try:
                sz = os.path.getsize(fp)
                if sz < 100000:
                    print(f"  {fp} ({sz} bytes)")
                    if fn.endswith('.json'):
                        try:
                            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(500)
                            print(f"    Content: {content[:200]}")
                        except: pass
            except: pass
else:
    print("No Profiles dir found")

# Also search all Thunder-related files for download settings
print("\n=== Searching for Thunder download settings ===")
thunder_roots = [
    r"C:\Users\Administrator\AppData\Roaming\Thunder",
    r"C:\Users\Administrator\AppData\Local\Thunder",
    r"C:\ProgramData\Thunder",
]
for root in thunder_roots:
    if not os.path.exists(root):
        continue
    for root2, dirs, files in os.walk(root):
        for fn in files:
            if fn.lower() in ['preferences', 'config', 'setting', 'download']:
                fp = os.path.join(root2, fn)
                print(f"  Found: {fp}")
                try:
                    sz = os.path.getsize(fp)
                    print(f"    Size: {sz}")
                except: pass
