import urllib.request
import re
import urllib.parse
import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://torrentkitty.net/',
}

code = 'MUDR-363'
url = f'https://torrentkitty.net/search/{code}/'

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html_content = resp.read().decode('utf-8', errors='ignore')

print(f'Page length: {len(html_content)}')
print()

# Find all data-magnet attributes
magnets = re.findall(r'data-magnet="(magnet:[^"]+)"', html_content)
print(f'Found {len(magnets)} magnet links via data-magnet:')
for i, m in enumerate(magnets):
    decoded = urllib.parse.unquote(m)
    # Extract name from dn param
    name_match = re.search(r'dn=([^&]+)', decoded)
    name = urllib.parse.unquote(name_match.group(1)) if name_match else 'unknown'
    size_match = re.search(r'size">([^<]+)<', html_content)
    print(f'{i+1}. {name}')
    print(f'   {decoded[:120]}...')
    print()

# Also look for result table rows
print()
print('=== Searching result table ===')
# Find table rows with torrent info
rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_content, re.DOTALL)
for row in rows[:10]:
    if 'MUDR' in row or 'mudr' in row.lower():
        # Extract text from row
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        for cell in cells:
            clean = re.sub(r'<[^>]+>', '', cell).strip()
            if clean and len(clean) > 3:
                print(f'  Cell: {clean[:80]}')
        print()
