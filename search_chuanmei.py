import urllib.request, re, urllib.parse, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}
term = '传媒'
encoded_term = urllib.parse.quote(term)

url = f'https://torrentkitty.net/search/{encoded_term}/'
print(f'Searching: {url}\n')

try:
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=20) as r:
        c = r.read().decode('utf-8', errors='ignore')
    
    magnets = re.findall(r'href="(magnet:[^"]+)"', c)
    print(f'Found {len(magnets)} results:\n')
    
    for i, raw in enumerate(magnets[:20], 1):
        m = urllib.parse.unquote(raw)
        dn = re.search(r'dn=([^&]+)', m)
        name = urllib.parse.unquote(dn.group(1)) if dn else 'unknown'
        
        # Check for CH/UC markers
        ch = '[CH]' if 'ch' in name.lower() or '中文' in name else ''
        uc = '[UC]' if 'uc' in name.lower() or '无码' in name else ''
        
        # Extract hash
        hash_match = re.search(r'btih:([A-Fa-f0-9]+)', m)
        btih = hash_match.group(1) if hash_match else ''
        
        print(f'{i}. {ch}{uc} {name[:70]}')
        print(f'   Hash: {btih}')
        print()
        
except Exception as e:
    print(f'ERROR: {e}')
