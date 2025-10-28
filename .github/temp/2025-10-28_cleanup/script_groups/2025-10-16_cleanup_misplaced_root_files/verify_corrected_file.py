#!/usr/bin/env python3
"""
Verify corrected ENSDF file against CSV source
"""

ens_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24_1st_extracted_CORRECTED.ens'

# Authoritative data from CSV (all 85 gammas)
csv_reference = {
    5645: [(2642, 80), (3882, 6)],
    7179: [(2340, 2), (3006, 1), (3120, 22), (3211, 9), (3261, 3), (4485, 4), (5960, 17), (7179, 38)],
    7547: [(1901, 1), (2777, 1), (4384, 95), (4544, 2), (4901, 1)],
    7838: [(1657, 1), (2239, 1), (2622, 1), (3660, 28), (3665, 3), (3779, 2), (3895, 1), (4835, 4), (6075, 2), (6619, 37), (7838, 21)],
    8207: [(2553, 1), (3326, 1), (3368, 1), (4148, 2), (5204, 1), (5513, 1), (6444, 14), (6988, 3), (8207, 78)],
    8216: [(2562, 1), (3446, 1), (4038, 3), (5053, 41), (5213, 5), (5522, 3), (6453, 1), (8216, 45)],
    8381: [(3611, 1), (3757, 1), (4268, 7), (4463, 24), (5378, 25), (5687, 1), (5735, 5), (6618, 34), (8381, 2)],
    8484: [(2830, 6), (3603, 7), (3860, 1), (4516, 1), (4566, 5), (5481, 7), (5790, 20), (5838, 3), (6721, 46), (8484, 4)],
    8893: [(3294, 1), (4780, 9), (4950, 4), (5730, 29), (6199, 37), (7130, 19), (8893, 1)],
    8907: [(3253, 4), (3261, 2), (3321, 4), (4137, 6), (4964, 15), (7144, 69)],
    9081: [(3357, 1), (4200, 1), (4903, 2), (4908, 2), (5163, 9), (5918, 6), (6387, 2), (6435, 1), (7318, 16), (9081, 60)],
}

# Parse ENS file with G at column 8 (position 7 in 0-indexed)
ens_data = {}
current_exi = None

with open(ens_file) as f:
    for line in f:
        if len(line) < 10:
            continue
        
        # Check for L-record (column 8, position 7 in 0-indexed)
        if len(line) > 7 and line[7] == 'L':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    current_exi = int(float(energy_str))
                    if current_exi not in ens_data:
                        ens_data[current_exi] = []
                except:
                    pass
        
        # Check for G-record
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

# Compare
print('=' * 100)
print('VERIFICATION: Corrected File vs. CSV Source')
print('=' * 100)
print()

total_csv = sum(len(v) for v in csv_reference.values())
total_ens = sum(len(v) for v in ens_data.values())

print(f'TOTALS: CSV={total_csv} gammas, File={total_ens} gammas')
print(f'Match: {"YES ✓" if total_csv == total_ens else "NO ✗"}')
print()

all_pass = True
for exi in sorted(csv_reference.keys()):
    csv_list = sorted(csv_reference[exi])
    ens_list = sorted(ens_data.get(exi, []))
    match = csv_list == ens_list
    all_pass = all_pass and match
    
    status = '✓' if match else '✗'
    print(f'{status} Exi={exi:5d}: {len(ens_list):2d} gammas')

print()
print('=' * 100)
if all_pass and total_csv == total_ens:
    print('✓✓✓ VERIFICATION PASSED - File is correct and ready! ✓✓✓')
else:
    print('✗✗✗ VERIFICATION FAILED ✗✗✗')
print('=' * 100)
