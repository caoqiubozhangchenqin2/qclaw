import urllib.request, re, urllib.parse

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}
url = 'https://torrentkitty.net/search/mudr-363ch/'
with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=15) as r:
    c = r.read().decode('utf-8', errors='ignore')

magnets = re.findall(r'data-magnet="([^"]+)"', c)
if magnets:
    for m in magnets:
        d = urllib.parse.unquote(m)
        print(d)
else:
    # Try alternative patterns
    alt = re.findall(r'href="(magnet:[^"]+)"', c)
    for m in alt:
        d = urllib.parse.unquote(m)
        print(d[:150])
