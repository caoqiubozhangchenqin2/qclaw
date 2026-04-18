import urllib.request, re, urllib.parse, time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://torrentkitty.net/',
}

# Read codes from hawa.txt
codes = []
with open(r'C:\Users\Administrator\Desktop\hawa.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and '：' in line:
            code = line.split('：')[-1].strip()
            name = line.split('：')[0].strip()
            codes.append((name, code))

print(f'Loaded {len(codes)} codes')
print()

results = []

for name, code in codes:
    # Try the exact code search first - look for CH in results
    try:
        url = f'https://torrentkitty.net/search/{code}/'
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            c = r.read().decode('utf-8', errors='ignore')
        
        # Find all result rows with their magnet
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', c, re.DOTALL)
        ch_found = None
        first_magnet = None
        
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            cell_texts = []
            for cell in cells:
                clean = re.sub(r'<[^>]+>', '', cell).strip()
                if clean:
                    cell_texts.append(clean)
            
            # Check if this row has our code
            row_text = ' '.join(cell_texts).lower()
            code_lower = code.lower()
            if code_lower in row_text or code_lower.replace('-', '') in row_text.replace('-', ''):
                # Extract magnet from this row
                magnet_match = re.search(r'data-magnet="([^"]+)"', row)
                if magnet_match:
                    m = urllib.parse.unquote(magnet_match.group(1))
                    # Check if CH
                    if 'ch' in row_text or 'chinese' in row_text:
                        ch_found = m
                        break
                    elif first_magnet is None:
                        first_magnet = m
        
        magnet = ch_found if ch_found else first_magnet
        status = 'CH' if ch_found else ('found' if first_magnet else 'none')
        results.append((name, code, status, magnet[:100] if magnet else ''))
        print(f'{name} [{code}]: {status}')
        
    except Exception as e:
        results.append((name, code, f'error: {e}', ''))
        print(f'{name} [{code}]: error')

print()
print('=== SUMMARY ===')
for name, code, status, magnet in results:
    print(f'{code}: {status}')

# Save magnets to file
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\magnets.txt', 'w', encoding='utf-8') as f:
    for name, code, status, magnet in results:
        if magnet:
            # Get full magnet from search
            f.write(f'{name} [{code}]\n')
            f.write(f'  Status: {status}\n')
            f.write(f'  Magnet: {magnet}\n\n')
