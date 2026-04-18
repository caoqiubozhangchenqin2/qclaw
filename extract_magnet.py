import re
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-71ec60f0\mudr363_search.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all magnet links
pattern = r'href="(magnet:[^"]+)"[^>]*>([^<]+)<'
magnets = re.findall(pattern, content)

print(f'Total magnets: {len(magnets)}')
for m, name in magnets[:20]:
    name = name.strip()
    if 'mudr' in name.lower() or '363' in name:
        print(f'Name: {name}')
        print(f'Link: {m}')
        print()
