import urllib.request, re, urllib.parse, json, time

h = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://torrentkitty.net/',
}

def search_torrent(code):
    """Search torrentkitty for a code, return best CH magnet."""
    url = f'https://torrentkitty.net/search/{code}/'
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            c = r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, f'fetch error: {e}'
    
    magnets = re.findall(r'href="(magnet:[^"]+)"', c)
    if not magnets:
        return None, 'no results'
    
    best = None
    best_is_ch = False
    
    for raw in magnets:
        m = urllib.parse.unquote(raw)
        # Decode dn
        dn_match = re.search(r'dn=([^&]+)', m)
        dn = urllib.parse.unquote(dn_match.group(1)) if dn_match else ''
        dn_lower = dn.lower()
        
        is_ch = ('ch' in dn_lower and ('chinese' in dn_lower or '字幕' in dn or dn_lower.count('ch') > 1)) or '中文字幕' in dn
        
        # Prefer CH, then larger (usually高清)
        if is_ch and not best_is_ch:
            best = m
            best_is_ch = True
        elif best is None:
            best = m
        elif is_ch == best_is_ch:
            # Same preference, pick larger (based on hash uniqueness - prefer first with unique hash)
            pass
    
    return best, ('CH' if best_is_ch else 'normal')

# Read hawa.txt
codes = []
with open(r'C:\Users\Administrator\Desktop\hawa.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and '：' in line:
            name = line.split('：')[0].strip()
            code = line.split('：')[-1].strip()
            codes.append((name, code))

print(f'Starting {len(codes)} codes...')

# Process all
all_results = []
for i, (name, code) in enumerate(codes):
    magnet, status = search_torrent(code)
    all_results.append((name, code, status, magnet))
    print(f'[{i+1}/{len(codes)}] {code}: {status} -> {"OK" if magnet else "FAIL"}')
    time.sleep(0.3)

# Save full results
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\results.txt', 'w', encoding='utf-8') as f:
    f.write(f'Scraped {len(codes)} codes from torrentkitty\n\n')
    for name, code, status, magnet in all_results:
        f.write(f'{name} [{code}]\n')
        f.write(f'  Status: {status}\n')
        if magnet:
            f.write(f'  Magnet: {magnet}\n')
        else:
            f.write(f'  Magnet: (not found)\n')
        f.write('\n')

print('\nDone! Results saved to results.txt')
print('\nSummary:')
for name, code, status, magnet in all_results:
    icon = 'CH' if status == 'CH' else ('OK' if magnet else 'X')
    print(f'  {icon} {code}')
