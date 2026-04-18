import urllib.request
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/html',
}

code = 'MUDR-363'

# Try solidtorrents API
try:
    api_url = f'https://solidtorrents.to/api/search?q={code}'
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    print('SolidTorrents API results:')
    if 'results' in data:
        for r in data['results'][:5]:
            print(f"  {r.get('title','?')} [{r.get('size','?')}]")
            print(f"  Magnet: {r.get('magnet')[:80] if r.get('magnet') else 'N/A'}")
            print()
except Exception as e:
    print(f'SolidTorrents API error: {e}')

# Try to get full solidtorrents search page
try:
    url = f'https://solidtorrents.to/search?q={code}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    # Find all magnet links
    magnets = re.findall(r'href="(magnet:[^"&]+)"', html)
    # Find titles near magnets
    print(f'Found {len(magnets)} magnets in solidtorrents HTML')
    for m in magnets[:10]:
        print(m[:100])
except Exception as e:
    print(f'SolidTorrents HTML error: {e}')
