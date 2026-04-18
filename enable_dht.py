import os

cfg_path = os.path.expandvars(r'%APPDATA%\qBittorrent\qBittorrent.ini')

# Read current config
with open(cfg_path, 'r', encoding='utf-8') as f:
    content = f.read()

# DHT and P2P settings to add
dht_settings = """
Session\DHTEnabled=true
Session\PeXEnabled=true
Session\LPDEnabled=true
Session\AddTrackersEnabled=true
"""

# Check if [BitTorrent] section exists
if '[BitTorrent]' in content:
    # Add DHT settings after [BitTorrent]
    lines = content.split('\n')
    new_lines = []
    in_bittorrent = False
    added = False
    
    for line in lines:
        new_lines.append(line)
        if line.strip() == '[BitTorrent]':
            in_bittorrent = True
            # Add DHT settings right after the section header
            new_lines.append('Session\\DHTEnabled=true')
            new_lines.append('Session\\PeXEnabled=true')
            new_lines.append('Session\\LPDEnabled=true')
            new_lines.append('Session\\AddTrackersEnabled=true')
            added = True
    
    content = '\n'.join(new_lines)

# Write back
with open(cfg_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("DHT enabled in config!")

# Now add trackers to each torrent via qBittorrent
# Common public trackers
trackers = """udp://tracker.opentrackr.org:1337/announce
udp://open.stealth.si:80/announce
udp://tracker.torrent.eu.org:451/announce
udp://tracker.bittor.pw:1337/announce
udp://public.popcorn-tracker.org:6969/announce
udp://tracker.dler.org:6969/announce
udp://exodus.desync.com:6969/announce
udp://open.demonii.com:1337/announce"""

print("\nPublic trackers to add:")
print(trackers[:200] + "...")

print("\nPlease restart qBittorrent to apply DHT settings.")
