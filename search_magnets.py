# 磁力搜索脚本 - 2026-05-03
# 从 tt.txt 读取番号，搜索磁力链接

import urllib.request
import urllib.parse
import json
import re
import time
import codecs

# 读取番号列表
with codecs.open(r'C:\Users\Administrator\Desktop\tt.txt', 'r', 'utf-8') as f:
    titles = [line.strip() for line in f if line.strip()]

print(f"共 {len(titles)} 个番号，开始搜索...")

results = []

for title in titles:
    code = title.split()[0]  # 取番号部分
    name = ' '.join(title.split()[1:]) if len(title.split()) > 1 else ''
    
    # 方法1: hao4k2 搜索
    url = f"https://hao4k2.com/magnet/search?keyword={urllib.parse.quote(code)}&page=1"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # 提取磁力链接
        magnets = re.findall(r'href="(magnet:[^"]+)"', html)
        magnets = list(set(magnets))  # 去重
        
        if magnets:
            # 提取 hash
            hashes = []
            for m in magnets[:5]:  # 取前5个
                hash_match = re.search(r'btih:([a-fA-F0-9]{40})', m)
                if hash_match:
                    hashes.append(hash_match.group(1).upper())
            
            # 判断版本
            version = ''
            if '无码' in html or 'uncensored' in html.lower() or 'UC' in html.upper():
                version = 'UC'
            elif '中文字' in html or '字幕' in html:
                version = 'CH'
            
            print(f"[OK] {code} {name} -> {len(hashes)} hashes, 版本: {version or '?'}")
            
            for h in hashes[:3]:  # 每番号最多3个hash
                results.append({
                    'code': code,
                    'name': name,
                    'hash': h,
                    'version': version,
                    'magnet': f"magnet:?xt=urn:btih:{h}"
                })
        else:
            print(f"[EMPTY] {code} {name} -> 无结果")
        
    except Exception as e:
        print(f"[ERR] {code} {name} -> {e}")
    
    time.sleep(0.5)

# 保存结果
print(f"\n搜索完成，共找到 {len(results)} 个磁力链接")
for r in results:
    print(f"  {r['code']} [{r['version']}] {r['hash']}")

# 生成迅雷批量文件
bat_content = '@echo off\nREM 磁力批量下载 - 2026-05-03\n'
for r in results:
    bat_content += f'start thunder://{str(base64.b64encode(r["magnet"].encode()).decode())}a_\n'

with open(r'C:\Users\Administrator\Desktop\magnets_20260503.bat', 'w', encoding='utf-8') as f:
    f.write(bat_content)

print(f"\n已生成 magnets_20260503.bat")
