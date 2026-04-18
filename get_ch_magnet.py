import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://torrentkitty.net/',
}

codes = ['mudr-363ch', 'MUDR-363']

for code in codes:
    url = f'https://torrentkitty.net/search/{code}/'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        
        # Extract full magnet link
        magnet = re.search(r'data-magnet="(magnet:[^"]+)"', content)
        if magnet:
            full = magnet.group(1)
            # Decode URL encoding
            import urllib.parse
            decoded = urllib.parse.unquote(full)
            print(f'Code: {code}')
            print(f'Magnet: {decoded}')
            print()
    except Exception as e:
        print(f'Error {code}: {e}')
