import urllib.request, re, urllib.parse, time

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}

def check_ch(dn):
    if not dn: return False
    dl = dn.lower()
    if dl.endswith('ch') and dl.count('ch') == 1: return True
    if '字幕' in dn or '中文字幕' in dn or 'chinese' in dl: return True
    return False

def check_uc(dn):
    if not dn: return False
    dl = dn.lower()
    if '-uc' in dl or dl.endswith('uc'): return True
    if 'uncensored' in dl: return True
    return False

def get_magnet(code):
    url = f'https://torrentkitty.net/search/{code}/'
    try:
        req = urllib.request.Request(url, headers=h)
        with urllib.request.urlopen(req, timeout=15) as r:
            c = r.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None, 'error', ''
    magnets = re.findall(r'href="(magnet:[^"]+)"', c)
    if not magnets:
        return None, 'none', ''
    results = []
    for raw in magnets:
        m = urllib.parse.unquote(raw)
        dn_match = re.search(r'dn=([^&]+)', m)
        dn = urllib.parse.unquote(dn_match.group(1)) if dn_match else ''
        is_ch = check_ch(dn)
        is_uc = check_uc(dn)
        if is_ch:
            results.append((3, dn, m))
        elif is_uc:
            results.append((2, dn, m))
        else:
            results.append((1, dn, m))
    results.sort(key=lambda x: -x[0])
    _, best_dn, best_m = results[0]
    tag = 'CH' if check_ch(best_dn) else ('UC' if check_uc(best_dn) else 'OK')
    return best_m, tag, best_dn

codes = [
    ('绫濑麻里央', 'MIDA-551'),
    ('九野雏乃', 'MIDA-523'),
    ('三木环奈', 'MIDA-520'),
    ('宮下玲奈', 'MIDA-518'),
    ('皆濑明里', 'MILK-277'),
    ('春野瑠瑠', 'NACT-080'),
    ('皆濑明里', 'FJIN-121'),
    ('木小夏×小野坂由香', 'SQTE-657'),
    ('鈴木真由', 'XMOM-107'),
    ('藤井蘭々', 'FNS-087'),
    ('松本一香', 'REBD-1005'),
    ('鈴木真夕', 'MILK-280'),
    ('三叶千春', 'DLDSS-458'),
    ('生田紗奈', 'FNS-156'),
    ('翼舞', 'FNS-185'),
    ('瀧本胡桃', 'MGOLD-052'),
    ('瀧本雫葉', 'ABF-317'),
]

print(f'Searching {len(codes)} codes (priority: CH > UC > normal)...\n')

bat_lines = []
for i, (name, code) in enumerate(codes):
    magnet, tag, dn = get_magnet(code)
    ch_mark = {'CH':'[CH]','UC':'[UC]','OK':'[  ]','error':'[!!]','none':'[XX]'}.get(tag, '[??]')
    print(f'[{i+1}/{len(codes)}] {ch_mark} {code}: {dn[:50]}')
    if magnet:
        bat_lines.append((code, tag, dn, magnet))
    time.sleep(0.3)

# Write bat file
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\dl_remaining.bat', 'w') as f:
    f.write('@echo off\n')
    for code, tag, dn, magnet in bat_lines:
        f.write(f'start "" "{magnet}"\n')
        f.write('timeout /t 3 /nobreak >nul\n')
    f.write('echo Done!\n')

# Save results
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\dl_remaining.txt', 'w', encoding='utf-8') as f:
    f.write('Remaining downloads (MIDA-551 onwards)\n\n')
    for code, tag, dn, magnet in bat_lines:
        f.write(f'{code} [{tag}] {dn}\n')
        f.write(f'  {magnet}\n\n')

print(f'\nBat: dl_remaining.bat ({len(bat_lines)} magnets)')
