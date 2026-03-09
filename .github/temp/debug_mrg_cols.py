mrg_lines = open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg', encoding='utf-8').readlines()

# Find a known line and print exact positions
for line in mrg_lines:
    if '1983Wa27--->B' in line and '950.77' in line:
        raw = line.rstrip('\n')
        print(f"Line length: {len(raw)}")
        print(f"Chars: {repr(raw[:90])}")
        for i in range(35, 80):
            print(f"  pos {i:3d}: {repr(raw[i])}")
        break
