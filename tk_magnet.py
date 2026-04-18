import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://torrentkitty.net/',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept': 'application/json, text/javascript, */*',
}

code = 'mudr-363ch'

# Try torrentkitty's internal API endpoints
for url in [
    f'https://torrentkitty.net/search/{code}/',
    f'https://torrentkitty.net/action/search?term={code}',
    f'https://torrentkitty.net/api/torrent/search?q={code}',
    f'https://torrentkitty.net/s/{code}/',
]:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        
        print(f'URL: {url}')
        print(f'  Length: {len(content)}')
        
        # Look for magnet links (many sites encode them in data attributes)
        import urllib.parse
        magnets = re.findall(r'data-magnet="([^"]+)"', content)
        if magnets:
            print(f'  Found {len(magnets)} data-magnet attrs')
            for m in magnets[:3]:
                decoded = urllib.parse.unquote(m)
                print(f'    {decoded}')
        
        import urllib.parse
        magnets2 = re.findall(r'magnet:[^\s<>"\']+', content)
        if magnets2:
            print(f'  Found {len(magnets2)} magnet links')
            for m in magnets2[:3]:
                decoded = urllib.parse.unquote(m)
                print(f'    {decoded}')
        
        # Look for JSON data
        json_matches = re.findall(r'\{[^{}]*"hash"[^{}]+\}', content[:5000], re.IGNORECASE)
        if json_matches:
            print(f'  Found {len(json_matches)} JSON blocks with hash')
            for j in json_matches[:2]:
                print(f'    {j[:200]}')
        
        # Look for JS API calls
        api_patterns = re.findall(r'(?:api|torrent|search)[^"\']*://[^\s"\']+', content, re.IGNORECASE)
        if api_patterns:
            print(f'  Found {len(api_patterns)} API URLs')
        
        print()
    except Exception as e:
        print(f'Error {url}: {e}')
