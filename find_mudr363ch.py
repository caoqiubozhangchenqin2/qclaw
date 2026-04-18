import urllib.request, re, urllib.parse
h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}
url = 'https://torrentkitty.net/search/mudr-363ch/'
with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=15) as r:
    c = r.read().decode('utf-8', errors='ignore')

magnets = re.findall(r'href="(magnet:[^"]+)"', c)
print(f'Found {len(magnets)} magnets for mudr-363ch:')
for i, raw in enumerate(magnets):
    m = urllib.parse.unquote(raw)
    dn = re.search(r'dn=([^&]+)', m)
    name = urllib.parse.unquote(dn.group(1)) if dn else '(no name)'
    ch = 'CH' if 'ch' in name.lower() else '  '
    print(f'[{ch}] {name}')
    print(f'    {m}')
    print()
