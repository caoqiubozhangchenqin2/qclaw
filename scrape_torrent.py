import urllib.request
import re
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

code = 'MUDR-363'
urls_to_try = [
    f'https://torrentgalaxy.to/torrents.php?search={code}',
    f'https://solidtorrents.to/search?q={code}',
    f'https://torrentkitty.net/search/{code}/',
    f'https://nyaa.si/?f=0&c=0_0&q={code}',
]

for url in urls_to_try:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Look for magnet links
        magnets = re.findall(r'href="(magnet:[^"]+)"', html)
        # Look for torrent names
        titles = re.findall(r'<(?:a|span|div)[^>]*(?:class|id)="[^"]*(?:title|name|result)[^"]*"[^>]*>([^<]{4,80})</(?:a|span|div)>', html, re.IGNORECASE)
        
        # Filter for our code
        ch_links = []
        for m, t in zip(magnets[:5], titles[:5]):
            t_clean = re.sub(r'<[^>]+>', '', t).strip()
            if code.lower() in t_clean.lower() or any(x in t_clean.lower() for x in ['ch', 'chinese', '字幕']):
                ch_links.append((t_clean, m))
        
        print(f'URL: {url}')
        print(f'  Magnets found: {len(magnets)}')
        if ch_links:
            for t, m in ch_links:
                print(f'  CH: {t[:60]} -> {m[:80]}')
        print()
    except Exception as e:
        print(f'Error {url}: {e}')
