"""Show exact content of lines around the 5762.8 comment."""
with open(r'A34\Cl34\new\Cl34_adopted.ens', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1305, 1315):
    line = lines[i]
    print(f'{i+1:5d} len={len(line.rstrip(chr(10)+chr(13))):3d}: {repr(line.rstrip()[:80])}')
