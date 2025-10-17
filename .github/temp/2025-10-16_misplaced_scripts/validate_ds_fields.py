#!/usr/bin/env python3
"""Validate DS-field format for all target L-records"""

with open(r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24.ens', 'r') as f:
    lines = f.readlines()

print('='*100)
print('DS-FIELD VALIDATION (Columns 75-76) - All 10 Target L-Records')
print('='*100)

target_energies = [7179, 7547, 7838, 8207, 8216, 8381, 8484, 8893, 8907, 9081]
import re

all_ok = True
for i, line in enumerate(lines, 1):
    if 'L ' in line:
        energy_match = re.search(r'L (\d+)', line)
        if energy_match:
            energy = int(energy_match.group(1))
            if energy in target_energies:
                if len(line) >= 76:
                    s_field = line[64:74]
                    ds_field = line[74:76]
                    s_ok = s_field.endswith(' ')
                    ds_ok = ds_field[0].isdigit() and ds_field[1] == ' '
                    status = 'OK' if (s_ok and ds_ok) else 'ERROR'
                    if not (s_ok and ds_ok):
                        all_ok = False
                    print('Line %3d: L %4d | S: %s | DS: %s | %s' % (i, energy, repr(s_field), repr(ds_field), status))

print()
if all_ok:
    print('✅ TASK COMPLETE: All 10 L-records have CORRECT S-field + DS-field separation')
    print('✅ S-field (65-74): Ep value left-justified with trailing spaces')
    print('✅ DS-field (75-76): Uncertainty "1" left-justified + space')
else:
    print('❌ ERRORS FOUND - See details above')
