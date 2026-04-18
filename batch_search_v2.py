import urllib.request, re, urllib.parse, time

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}

def check_ch(dn):
    """Check if dn indicates Chinese subtitle version."""
    if not dn:
        return False
    dl = dn.lower()
    # mudr-363ch: lowercase ch at end
    if dl.endswith('ch') and dl.count('ch') == 1:
        return True
    if '字幕' in dn or '中文字幕' in dn or 'chinese' in dl:
        return True
    return False

def get_best_magnet(code):
    url = f'https://torrentkitty.net/search/{code}/'
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            c = r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, False, f'error: {e}'

    magnets = re.findall(r'href="(magnet:[^"]+)"', c)
    if not magnets:
        return None, False, 'no results'

    best = None
    best_ch = False
    best_dn = ''

    for raw in magnets:
        m = urllib.parse.unquote(raw)
        dn_match = re.search(r'dn=([^&]+)', m)
        dn = urllib.parse.unquote(dn_match.group(1)) if dn_match else ''
        is_ch = check_ch(dn)

        if is_ch and not best_ch:
            best = m
            best_ch = True
            best_dn = dn
        elif best is None:
            best = m
            best_dn = dn
            best_ch = is_ch

    return best, best_ch, best_dn

# Read hawa.txt
codes = []
with open(r'C:\Users\Administrator\Desktop\hawa.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and '：' in line:
            name = line.split('：')[0].strip()
            code = line.split('：')[-1].strip()
            codes.append((name, code))

print(f'Searching {len(codes)} codes...')

bat_lines = []
all_results = []

for i, (name, code) in enumerate(codes):
    magnet, best_ch, dn = get_best_magnet(code)
    status = 'CH' if best_ch else 'OK'
    all_results.append((name, code, status, dn, magnet))
    ch_mark = '[CH]' if best_ch else '[  ]'
    print(f'[{i+1}/{len(codes)}] {ch_mark} {code}: {dn[:50]}')
    if magnet:
        bat_lines.append(f'start "" "{magnet}"')
        bat_lines.append('timeout /t 3 /nobreak >nul')
    time.sleep(0.3)

# Write bat
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\open_all_v2.bat', 'w', encoding='utf-8') as f:
    f.write('@echo off\n')
    f.write('echo Starting all magnets...\n')
    for line in bat_lines:
        f.write(line + '\n')
    f.write('echo All done!\n')

# Write results
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\results_v2.txt', 'w', encoding='utf-8') as f:
    f.write(f'Scraped {len(codes)} codes (v2 - fixed CH detection)\n\n')
    for name, code, status, dn, magnet in all_results:
        f.write(f'{name} [{code}]\n')
        f.write(f'  Status: {status}\n')
        f.write(f'  Dn: {dn}\n')
        if magnet:
            f.write(f'  Magnet: {magnet}\n')
        else:
            f.write(f'  Magnet: (not found)\n')
        f.write('\n')

magnet_count = len([l for l in bat_lines if l.startswith('start')])
print(f'\nDone! {magnet_count} magnets -> open_all_v2.bat')
print('\nSummary:')
for name, code, status, dn, magnet in all_results:
    icon = 'CH' if status == 'CH' else ('OK' if magnet else 'X')
    print(f'  {icon} {code}')
