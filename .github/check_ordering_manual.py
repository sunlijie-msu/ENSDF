#!/usr/bin/env python3
"""Check energy ordering for L-records and G-records under each level"""

ens_file = 'A35/Cl35/raw/2001VO24.ens'

with open(ens_file, 'r') as f:
    lines = f.readlines()

# Extract L-records
l_records = []
for idx, line in enumerate(lines, 1):
    if len(line) >= 8 and line[7] == 'L':
        try:
            energy = int(line[9:19].strip())
            l_records.append((idx, energy))
        except:
            pass

# Check L-record ordering
print('L-RECORD ENERGY ORDERING:')
print('='*60)
l_ordered = True
for i in range(len(l_records)-1):
    line1, e1 = l_records[i]
    line2, e2 = l_records[i+1]
    status = 'OK' if e1 <= e2 else 'ERROR'
    print(f'{status}: E[{i}]={e1:5d} <= E[{i+1}]={e2:5d}')
    if e1 > e2:
        l_ordered = False

print()
print('L-Record Ordering:', 'CORRECT ✓' if l_ordered else 'INCORRECT ✗')
print()

# Extract G-records by level
g_by_level = {}
current_level = None
for idx, line in enumerate(lines, 1):
    if len(line) >= 8 and line[7] == 'L':
        try:
            energy = int(line[9:19].strip())
            current_level = energy
            if current_level not in g_by_level:
                g_by_level[current_level] = []
        except:
            pass
    elif len(line) >= 8 and line[7] == 'G' and current_level is not None:
        try:
            energy = int(line[9:19].strip())
            g_by_level[current_level].append((idx, energy))
        except:
            pass

# Check G-record ordering within each level
print('G-RECORD ORDERING BY LEVEL:')
print('='*60)
g_ordered = True
for level in sorted(g_by_level.keys()):
    gammas = g_by_level[level]
    level_ordered = True
    for i in range(len(gammas)-1):
        line1, e1 = gammas[i]
        line2, e2 = gammas[i+1]
        if e1 > e2:
            level_ordered = False
            g_ordered = False
    
    status = 'OK' if level_ordered else 'ERROR'
    print(f'{status}: Level E={level:5d} keV has {len(gammas):2d} gammas (ordered: {level_ordered})')
    if not level_ordered:
        for i, (line_no, energy) in enumerate(gammas):
            print(f'      G{i+1}: E={energy:5d}')

print()
print('G-Record Ordering:', 'CORRECT ✓' if g_ordered else 'INCORRECT ✗')
print()
print('OVERALL RESULT:', 'ALL ORDERING CHECKS PASS ✓' if (l_ordered and g_ordered) else 'ORDERING ISSUES ✗')
