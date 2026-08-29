import re
raw = open(r'd:\X\ND\ENSDF\.github\temp\fdiff2.txt', 'rb').read()
for enc in ['utf-16', 'utf-8-sig', 'utf-8']:
    try:
        d = raw.decode(enc)
        break
    except UnicodeDecodeError:
        continue
lines = d.splitlines()
adds = [l for l in lines if l.startswith('+') and not l.startswith('+++')]
dels = [l for l in lines if l.startswith('-') and not l.startswith('---')]
print('adds', len(adds), 'dels', len(dels))
for l in adds + dels:
    print(l[:120])
