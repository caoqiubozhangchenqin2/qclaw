import urllib.request, re, urllib.parse

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}

url = 'https://torrentkitty.net/search/MUKA-003/'
with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=15) as r:
    c = r.read().decode('utf-8', errors='ignore')

print(f'Length: {len(c)}')

# Check for magnet patterns
patterns = [
    ('data-magnet', r'data-magnet="([^"]+)"'),
    ('href magnet', r'href="(magnet:[^"]+)"'),
    ('magnet plain', r'magnet:[a-zA-Z0-9:?&=\-%;]+'),
    ('tr class=row', r'<tr[^>]*class="[^"]*row[^"]*"[^>]*>(.*?)</tr>'),
    ('tr id=torrent', r'<tr[^>]*id="torrent[^"]*"[^>]*>(.*?)</tr>'),
    ('detail opendownload', r'[Dd]etail[Oo]pen[DD]ownload'),
    ('onclick magnet', r"onclick[^)]*magnet"),
    ('a class=action', r'<a[^>]*class="[^"]*action[^"]*"[^>]*>[^<]*</a>'),
]

for name, pattern in patterns:
    matches = re.findall(pattern, c)
    print(f'{name}: {len(matches)} found')
    if matches:
        print(f'  First: {matches[0][:100]}')

# Show a snippet of the page around 'MUKA'
idx = c.lower().find('muka')
if idx > 0:
    print(f'\nPage snippet around MUKA:')
    print(c[max(0,idx-200):idx+500])
