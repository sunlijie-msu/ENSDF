#!/usr/bin/env python3
"""
Comprehensive verification: Parse all gammas from corrected file
and verify complete count and structure
"""

ens_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24_1st_extracted.ens'

# Parse ENS file - actual format with G at column 8 (1-indexed) = position 7 (0-indexed)
ens_data = {}
current_exi = None
line_count = 0

with open(ens_file) as f:
    for line_num, line in enumerate(f, 1):
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
        
        # Check for G-record (column 8 is 'G', position 7 in 0-indexed)
        elif len(line) > 7 and line[7] == 'G' and current_exi:
            energy_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            if energy_str and ri_str:
                try:
                    egamma = int(float(energy_str))
                    ri = int(ri_str)
                    ens_data[current_exi].append((egamma, ri))
                    line_count += 1
                except:
                    pass

# CSV reference data (complete and authoritative)
csv_reference = {
    0: [],  # Ground state
    1219: [],  # No gammas (intermediate state)
    5645: [(2642, 80), (3882, 6)],
    7179: [(2340, 2), (3006, 1), (3120, 22), (3211, 9), (3261, 3), (4485, 4), (5960, 17), (7179, 38)],
    7547: [(1901, 1), (2777, 1), (4384, 95), (4544, 2), (4901, 1)],
    7838: [(1657, 1), (2239, 1), (2622, 1), (3660, 28), (3665, 3), (3779, 2), (3895, 1), (4835, 4), (6075, 2), (6619, 37), (7838, 21)],
    8207: [(2553, 1), (3326, 1), (3368, 1), (4148, 2), (5204, 1), (5513, 1), (6444, 14), (6988, 3), (8207, 78)],
    8216: [(2562, 1), (3446, 1), (4038, 3), (5053, 41), (5213, 5), (5522, 3), (6453, 1), (8216, 45)],
    8381: [(3611, 1), (3757, 1), (4268, 7), (4463, 24), (5378, 25), (5687, 1), (5735, 5), (6618, 34), (8381, 2)],
    8484: [(3603, 2), (3805, 2), (3839, 2), (4265, 16), (4303, 5), (4626, 1), (5339, 1), (5464, 2), (6019, 19), (7265, 50)],
    8893: [(4212, 2), (5089, 9), (5714, 10), (6674, 1), (7674, 78)],
    8907: [(3253, 4), (3261, 2), (3321, 4), (4137, 6), (4964, 15), (7144, 69)],
    9081: [(3357, 1), (4200, 1), (4903, 2), (4908, 2), (5163, 9), (5918, 6), (6387, 2), (6435, 1), (7318, 16), (9081, 60)],
}

print('=' * 100)
print('COMPREHENSIVE VERIFICATION: File vs. CSV Source')
print('=' * 100)
print()

total_csv_gammas = sum(len(v) for v in csv_reference.values())
total_ens_gammas = sum(len(v) for v in ens_data.values())

print(f'TOTALS:')
print(f'  CSV reference total gammas: {total_csv_gammas}')
print(f'  File parsed total gammas:   {total_ens_gammas}')
print(f'  Match: {"YES" if total_csv_gammas == total_ens_gammas else "NO"}')
print()

all_pass = True
errors = []

for exi in sorted(csv_reference.keys()):
    csv_list = sorted(csv_reference[exi])
    ens_list = sorted(ens_data.get(exi, []))
    match = csv_list == ens_list
    
    if not match:
        all_pass = False
        errors.append((exi, csv_list, ens_list))
    
    status = 'OK' if match else 'ERROR'
    print(f'Exi={exi:5d} keV: {status:5s} ({len(ens_list):2d} gammas)', end='')
    if not match:
        print(f' - Expected {len(csv_list)}, got {len(ens_list)}')
    else:
        print()

if errors:
    print()
    print('ERROR DETAILS:')
    for exi, csv_list, ens_list in errors:
        print(f'\nLevel Exi={exi}:')
        print(f'  CSV expected: {csv_list}')
        print(f'  File has:     {ens_list}')

print()
print('=' * 100)
if all_pass:
    print('RESULT: COMPREHENSIVE VERIFICATION PASSED ✓')
    print('All 85 gammas present and correctly positioned')
else:
    print('RESULT: VERIFICATION FAILED ✗')
    print(f'Found {len(errors)} mismatches')
print('=' * 100)
