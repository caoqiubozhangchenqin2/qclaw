import urllib.request, re, urllib.parse

h = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://torrentkitty.net/'}

def get_torrent_info(html, code):
    """Extract all torrents for a code from torrentkitty page HTML."""
    results = []
    
    # Find all magnet hrefs with their position
    magnet_pattern = r'href="(magnet:[^"]+)"'
    magnets = list(re.finditer(magnet_pattern, html))
    
    # Also find all table cells (td elements) to get names/sizes
    cells = re.findall(r'<td[^>]*>(.*?)</td>', html, re.DOTALL)
    cell_texts = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
    
    # Also get table row structure - each torrent is in a <tr>
    rows = re.findall(r'<tr>(.*?)</tr>', html, re.DOTALL)
    
    # Try to pair magnets with names using row structure
    if rows:
        for row in rows:
            # Get the magnet in this row
            m = re.search(r'href="(magnet:[^"]+)"', row)
            if m:
                raw_m = m.group(1)
                magnet = urllib.parse.unquote(raw_m)
                
                # Get all text content in row
                row_text = re.sub(r'<[^>]+>', ' ', row).strip()
                row_text = re.sub(r'\s+', ' ', row_text)
                
                # Extract dn from magnet
                dn_match = re.search(r'dn=([^&]+)', magnet)
                name = urllib.parse.unquote(dn_match.group(1)) if dn_match else ''
                
                # Check if CH
                is_ch = 'ch' in row_text.lower() or 'chinese' in row_text.lower() or '字幕' in row_text
                
                results.append({
                    'name': name,
                    'magnet': magnet,
                    'is_ch': is_ch,
                    'row_text': row_text[:100]
                })
    else:
        # No row structure, use cell-based approach
        for i, m in enumerate(magnets):
            raw_m = m.group(1)
            magnet = urllib.parse.unquote(raw_m)
            dn_match = re.search(r'dn=([^&]+)', magnet)
            name = urllib.parse.unquote(dn_match.group(1)) if dn_match else ''
            is_ch = 'ch' in name.lower() or 'chinese' in name.lower() or '字幕' in name
            results.append({
                'name': name,
                'magnet': magnet,
                'is_ch': is_ch,
                'row_text': name
            })
    
    return results

# Test with MUKA-003
url = 'https://torrentkitty.net/search/MUKA-003/'
with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=15) as r:
    c = r.read().decode('utf-8', errors='ignore')

print(f'Page length: {len(c)}')
results = get_torrent_info(c, 'MUKA-003')
print(f'Found {len(results)} torrents')
for r in results:
    ch_mark = 'CH' if r['is_ch'] else '  '
    print(f'  [{ch_mark}] {r["name"]}')
    print(f'         {r["magnet"][:80]}...')
