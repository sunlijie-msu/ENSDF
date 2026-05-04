"""Show exact content of all target lines."""
with open(r'A34\Cl34\new\Cl34_adopted.ens', encoding='utf-8') as f:
    lines = f.readlines()

targets = [243, 244, 627, 628, 639, 663, 814, 836, 982, 983, 1027,
           1055, 1175, 1223, 1308, 1309, 1326, 2272, 2475, 2516, 2682, 2903, 2909]

for t in targets:
    line = lines[t-1]
    print(f'{t:5d} len={len(line.rstrip(chr(10)+chr(13))):3d}: {repr(line.rstrip()[:80])}')
