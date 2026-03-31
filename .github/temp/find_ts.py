with open('A34/Cl34/raw/34_20260325.mrg', 'r', errors='replace') as f:
    lines = f.readlines()
d = chr(36)
hits = [(i+1, l.rstrip()) for i,l in enumerate(lines) if 'T' + d in l and '---' not in l and l.strip()]
print('Count=' + str(len(hits)))
for ln, l in hits[:50]:
    print(str(ln) + ': ' + l[:130])
