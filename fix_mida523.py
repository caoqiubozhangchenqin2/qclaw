import urllib.request, re, urllib.parse
h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}
try:
    url = 'https://torrentkitty.net/search/MIDA-523/'
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=15) as r:
        c = r.read().decode('utf-8', errors='ignore')
    magnets = re.findall(r'href="(magnet:[^"]+)"', c)
    print(f'MIDA-523: {len(magnets)} results')
    for raw in magnets[:5]:
        m = urllib.parse.unquote(raw)
        dn = re.search(r'dn=([^&]+)', m)
        dn = urllib.parse.unquote(dn.group(1)) if dn else ''
        ch = 'CH' if dn.lower().endswith('ch') else ''
        uc = 'UC' if '-uc' in dn.lower() else ''
        print(f'  [{ch}{uc}] {dn}')
        print(f'         {m}')
except Exception as e:
    print(f'Error: {e}')
