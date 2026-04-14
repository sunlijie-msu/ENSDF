import sys
lines = open(r'd:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens', encoding='utf-8').readlines()
bad = []
for i, ln in enumerate(lines):
    raw = ln.rstrip('\r\n')
    if len(raw) >= 6 and raw[5] == 'X' and 'XREF=' in raw:
        n = len(raw)
        if n != 80:
            bad.append((i+1, n, raw))
print(f'Bad lines: {len(bad)}')
for b in bad:
    print(f'Line {b[0]}: {b[1]} chars: {b[2]}')
print('Done.')
