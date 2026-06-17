"""Set L-record col 77 comment flag for band membership.
QB1=A, QB2=B, QB3=C, QB4=D, QB3a=E."""

ENSDF_FILE = r"d:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens"

# Band definitions: (flag, [level_energies_as_in_file])
BANDS = {
    'A': [8610.9, 7142.9, 5903.4, 4859.4, 4067.0, 3317.8, 2418.7, 1899.3, 810.6, 175.9],
    'B': [14565.2, 12954.2, 11500.1, 10191.5, 9027.4, 7987.2, 7048.9, 6207.5, 5459.3],
    'C': [15377.5, 13499.5, 11913.5, 10585.1, 9476.6, 8557.8, 7774.1, 7094.2, 6467.1, 5817.0],
    'D': [8348.1, 7376.3, 6350.3, 5576.3, 5433.9, 5096.9, 4769.1, 4482.0, 3623.9],
    'E': [6413.4, 5940.2, 5594.7, 5341.0],
}

# Read file
with open(ENSDF_FILE, 'r') as f:
    lines = f.readlines()

# Build level energy set for quick lookup
level_targets = {}
for flag, energies in BANDS.items():
    for e in energies:
        level_targets[e] = flag

print(f"Target levels: {len(level_targets)}")
print("Looking up L-records...")

replacements = []

for i, line in enumerate(lines):
    raw = line.rstrip('\n').rstrip('\r')
    if len(raw) < 80:
        continue
    # L-record: col 8 = 'L', col 7 = ' '
    if raw[7] != 'L' or raw[6] != ' ':
        continue
    
    # Extract level energy from cols 10-19
    e_field = raw[9:19].strip()
    try:
        lev_e = float(e_field)
    except ValueError:
        continue
    
    if lev_e in level_targets:
        flag = level_targets[lev_e]
        # Check current col 77 (index 76)
        current = raw[76] if len(raw) > 76 else ' '
        
        if current == flag:
            print(f"Line {i+1}: Level {lev_e:>8.1f} already flag {flag}")
            continue
        
        # Build new line: replace col 77 with flag
        new_raw = raw[:76] + flag + raw[77:]
        
        print(f"Line {i+1}: Level {lev_e:>8.1f} flag '{current}' -> '{flag}'  [{BANDS[flag].index(lev_e)+1}/{len(BANDS[flag])}]")
        print(f"  OLD: {raw}")
        print(f"  NEW: {new_raw}")
        print(f"  OLD len={len(raw)}, NEW len={len(new_raw)}")
        
        replacements.append({
            'line': i + 1,
            'lev_e': lev_e,
            'flag': flag,
            'old': raw,
            'new': new_raw,
        })

print(f"\nTotal replacements: {len(replacements)}")

# Verify flag counts
for flag in ['A', 'B', 'C', 'D', 'E']:
    count = sum(1 for r in replacements if r['flag'] == flag)
    expected = len(BANDS[flag])
    print(f"Flag {flag}: {count}/{expected}")
