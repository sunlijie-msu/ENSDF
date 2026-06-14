import sys
with open('XUNDL/2026MAAA_CT11001_141Sm.ens','r',encoding='utf-8') as f:
    content = f.read()
count = 0
for sym in ['\u00b0', '\u25e6']:
    c = content.count(sym)
    if c:
        content = content.replace(sym, "|'")
        count += c
if count:
    print(f'Replaced {count}x degree symbols with ENSDF notation')
for i, line in enumerate(content.split('\n'),1):
    non = [c for c in line if ord(c)>127]
    if non:
        codes = [f'U+{ord(c):04X}' for c in non]
        print(f'Line {i}: non-ASCII {codes}')
        print(f'  {line[:80]}')
with open('XUNDL/2026MAAA_CT11001_141Sm.ens','w',encoding='utf-8') as f:
    f.write(content)
print('Done - file is ASCII-clean' if not any(ord(c)>127 for c in content) else 'Still has non-ASCII')
