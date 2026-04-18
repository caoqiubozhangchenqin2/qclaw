import json

paths = [
    r'C:\Users\Administrator\AppData\Roaming\Thunder\Preferences',
    r'C:\Users\Administrator\AppData\Roaming\Thunder\Local State',
]

for p in paths:
    try:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        print(f"=== {p} ===")
        print(content[:1000])
        print()
    except Exception as e:
        print(f"Error reading {p}: {e}")
