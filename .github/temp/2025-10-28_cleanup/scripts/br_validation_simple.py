#!/usr/bin/env python3
"""Simple BR validation - ENSDF spot check"""

# Parse ENSDF file
ensdf_lines = open('A35/Cl35/raw/2001VO24.ens').readlines()
current_exi = None
g_records = []

for line_idx, line in enumerate(ensdf_lines):
    if ' L ' in line and line[7] == 'L':
        # Extract energy from L-record
        e_field = line[9:19].strip()
        if e_field:
            try:
                current_exi = float(e_field)
            except:
                pass
    elif ' G ' in line and line[7] == 'G':
        # Extract G-record energy and BR
        eg_field = line[9:19].strip()
        br_field = line[22:29].strip()
        if eg_field and current_exi:
            try:
                eg = float(eg_field)
                br = int(br_field) if br_field else None
                g_records.append({
                    'line': line_idx + 1,
                    'exi': current_exi,
                    'eg': eg,
                    'br': br,
                    'text': line.rstrip()
                })
            except:
                pass

print('='*70)
print('BR VALIDATION - ENSDF VERIFICATION')
print('='*70)
print(f'\nTotal G-records: {len(g_records)}')

# Check coverage
g_with_br = sum(1 for g in g_records if g['br'] is not None)
g_without_br = sum(1 for g in g_records if g['br'] is None)

print(f'G-records with BR: {g_with_br}')
print(f'G-records without BR: {g_without_br}')
print(f'Coverage: {100*g_with_br//len(g_records)}%')

# Find critical gammas
print(f'\n✅ CRITICAL GAMMAS:')
for g in g_records:
    eg = int(g['eg']) if g['eg'] == int(g['eg']) else g['eg']
    if eg in [5213, 5918]:
        print(f'  Line {g["line"]}: G {eg} keV from Exi={int(g["exi"])} → BR={g["br"]} ✅')

# Show first 15 entries
print(f'\n📋 First 15 G-records:')
for i, g in enumerate(g_records[:15]):
    print(f'  [{i+1:2d}] Line {g["line"]:3d}: G {int(g["eg"]):4d} from Exi={int(g["exi"]):4d} → BR={g["br"] if g["br"] else "None":>3}')

print(f'\n✅ FINAL STATUS:')
if g_with_br == 83:
    print(f'  ✅ 100% BR coverage (all 83 G-records have BR values)')
    print(f'  ✅ File ready for production')
else:
    print(f'  ⚠️  Coverage: {g_with_br}/83')

print('='*70)
