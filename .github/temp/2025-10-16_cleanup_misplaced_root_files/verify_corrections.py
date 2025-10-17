#!/usr/bin/env python3
"""
Spot-check corrected ENS file against CSV source
"""

ens_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24_1st_extracted.ens'

# Parse ENS file - File 1 format with G at column 8
ens_data = {}
current_exi = None

with open(ens_file) as f:
    for line in f:
        if len(line) < 10:
            continue
        
        # Check for L-record (column 8, 1-indexed = position 7 in 0-indexed Python)
        if len(line) > 7 and line[7] == 'L':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    current_exi = int(float(energy_str))
                    if current_exi not in ens_data:
                        ens_data[current_exi] = []
                except:
                    pass
        
        # Check for G-record (column 8 is 'G', position 7 in 0-indexed)
        elif len(line) > 7 and line[7] == 'G' and current_exi:
            energy_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            if energy_str and ri_str:
                try:
                    egamma = int(float(energy_str))
                    ri = int(ri_str)
                    ens_data[current_exi].append((egamma, ri))
                except:
                    pass

# CSV reference data (authoritative)
csv_gammas = {
    7547: [(1901, 1), (2777, 1), (4384, 95), (4544, 2), (4901, 1)],
    8216: [(2562, 1), (3446, 1), (4038, 3), (5053, 41), (5213, 5), (5522, 3), (6453, 1), (8216, 45)],
    8381: [(3611, 1), (3757, 1), (4268, 7), (4463, 24), (5378, 25), (5687, 1), (5735, 5), (6618, 34), (8381, 2)],
    8907: [(3253, 4), (3261, 2), (3321, 4), (4137, 6), (4964, 15), (7144, 69)],
    9081: [(3357, 1), (4200, 1), (4903, 2), (4908, 2), (5163, 9), (5918, 6), (6387, 2), (6435, 1), (7318, 16), (9081, 60)],
}

print('=' * 90)
print('SPOT-CHECK VERIFICATION: Corrected File vs. CSV Source')
print('=' * 90)
print()

all_pass = True
for exi in sorted(csv_gammas.keys()):
    csv_list = sorted(csv_gammas[exi])
    ens_list = sorted(ens_data.get(exi, []))
    match = csv_list == ens_list
    status = 'OK' if match else 'ERROR'
    all_pass = all_pass and match
    print(f'Level Exi={exi}: {status} ({len(ens_list)} gammas)')
    if not match:
        print(f'  CSV expected:  {csv_list}')
        print(f'  File contains: {ens_list}')

print()
print('=' * 90)
if all_pass:
    print('RESULT: All spot-checks PASS - Corrections verified!')
else:
    print('RESULT: Spot-check FAILED - Errors remain')
print('=' * 90)
