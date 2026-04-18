import urllib.request, re, urllib.parse
h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}

# Check CH search results to understand the naming pattern
codes_ch = ['MUDR-363', 'NACT-080', 'FNS-087', 'DLDSS-458']
for code in codes_ch:
    url = f'https://torrentkitty.net/search/{code}/'
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=15) as r:
        c = r.read().decode('utf-8', errors='ignore')
    magnets = re.findall(r'href="(magnet:[^"]+)"', c)
    print(f'=== {code} ({len(magnets)} results) ===')
    for raw in magnets[:5]:
        m = urllib.parse.unquote(raw)
        dn_match = re.search(r'dn=([^&]+)', m)
        dn = urllib.parse.unquote(dn_match.group(1)) if dn_match else ''
        # Check various CH indicators
        ch_in_name = 'ch' in dn.lower()
        chinese_chars = any('\u4e00' <= c <= '\u9fff' for c in dn)
        dn_lower = dn.lower()
        would_be_ch_old = 'ch' in dn_lower and ('chinese' in dn_lower or '\u5b57\u5e55' in dn)
        would_be_ch_new = 'ch' in dn_lower
        print(f'  Old logic: {would_be_ch_old}, New logic: {would_be_ch_new}, Chinese: {chinese_chars} | {dn}')
    print()
