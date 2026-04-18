import urllib.request, re, urllib.parse
h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}

# Try different search URLs
terms = ['MUDR-363', 'mudr-363', 'mudr363', '363ch', 'MUDR363CH']
for term in terms:
    url = f'https://torrentkitty.net/search/{term}/'
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            c = r.read().decode('utf-8', errors='ignore')
        title = re.search(r'<title>(.*?)</title>', c)
        title_text = title.group(1) if title else 'no title'
        magnets = re.findall(r'href="(magnet:[^"]+)"', c)
        print(f'Term: {term} -> {len(magnets)} magnets, title: {title_text[:50]}')
        for raw in magnets[:3]:
            m = urllib.parse.unquote(raw)
            dn = re.search(r'dn=([^&]+)', m)
            name = urllib.parse.unquote(dn.group(1)) if dn else ''
            ch = 'CH' if 'ch' in name.lower() else '  '
            print(f'  [{ch}] {name}')
    except Exception as e:
        print(f'Term: {term} -> ERROR: {e}')
    print()
