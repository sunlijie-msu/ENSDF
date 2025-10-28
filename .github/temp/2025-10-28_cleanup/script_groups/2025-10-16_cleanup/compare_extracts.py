#!/usr/bin/env python3
"""
Compare the two extracted ENS files against the authoritative CSV data
"""

import sys

# Reference data from CSV analysis (85 total gammas)
csv_data = {
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

def parse_ens_file(filename):
    """Parse ENS file and extract L and G records"""
    data = {}
    current_exi = None
    
    with open(filename, 'r') as f:
        for line in f:
            if len(line) < 10:
                continue
            
            # Check for L-record (column 8 is 'L')
            if len(line) > 7 and line[7] in ('L', 'l'):
                # Extract energy from columns 10-19
                energy_str = line[9:19].strip()
                if energy_str:
                    try:
                        current_exi = int(float(energy_str))
                        if current_exi not in data:
                            data[current_exi] = []
                    except ValueError:
                        current_exi = None
            
            # Check for G-record (column 8 is 'G')
            elif len(line) > 7 and line[7] in ('G', 'g') and current_exi is not None:
                # Extract energy from columns 10-19
                energy_str = line[9:19].strip()
                # Extract RI from columns 23-29
                ri_str = line[22:29].strip() if len(line) > 28 else ""
                
                if energy_str and ri_str:
                    try:
                        egamma = int(float(energy_str))
                        ri = int(ri_str)
                        data[current_exi].append((egamma, ri))
                    except ValueError:
                        pass
    
    return data

# Parse both files
file1 = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24_1st_extracted.ens'
file2 = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24_2nd_extract.ens'

print("=" * 120)
print("COMPARING ENS EXTRACTS AGAINST AUTHORITATIVE CSV DATA")
print("=" * 120)

ens1_data = parse_ens_file(file1)
ens2_data = parse_ens_file(file2)

print(f"\nFile 1 (2001VO24_1st_extracted.ens): {sum(len(v) for v in ens1_data.values())} gammas")
print(f"File 2 (2001VO24_2nd_extract.ens):   {sum(len(v) for v in ens2_data.values())} gammas")
print(f"CSV (authoritative source):          {sum(len(v) for v in csv_data.values())} gammas\n")

print("=" * 120)
print("LEVEL-BY-LEVEL COMPARISON")
print("=" * 120)

all_exi = sorted(set(list(csv_data.keys()) + list(ens1_data.keys()) + list(ens2_data.keys())))

for exi in all_exi:
    csv_gammas = sorted(csv_data.get(exi, []))
    ens1_gammas = sorted(ens1_data.get(exi, []))
    ens2_gammas = sorted(ens2_data.get(exi, []))
    
    status1 = "✓" if ens1_gammas == csv_gammas else "✗"
    status2 = "✓" if ens2_gammas == csv_gammas else "✗"
    
    print(f"\n{'─' * 120}")
    print(f"Exi = {exi} keV: CSV has {len(csv_gammas)} gammas")
    print(f"  File 1: {status1} {len(ens1_gammas)} gammas")
    print(f"  File 2: {status2} {len(ens2_gammas)} gammas")
    
    if ens1_gammas != csv_gammas or ens2_gammas != csv_gammas:
        print(f"\n  CSV (authoritative):")
        for eg, ri in csv_gammas:
            print(f"    G {eg:5d}  RI={ri:3d}")
        
        if ens1_gammas != csv_gammas:
            print(f"\n  File 1 DIFFERENCES:")
            missing_in_1 = set(csv_gammas) - set(ens1_gammas)
            extra_in_1 = set(ens1_gammas) - set(csv_gammas)
            if missing_in_1:
                print(f"    Missing: {missing_in_1}")
            if extra_in_1:
                print(f"    Extra:   {extra_in_1}")
        
        if ens2_gammas != csv_gammas:
            print(f"\n  File 2 DIFFERENCES:")
            missing_in_2 = set(csv_gammas) - set(ens2_gammas)
            extra_in_2 = set(ens2_gammas) - set(csv_gammas)
            if missing_in_2:
                print(f"    Missing: {missing_in_2}")
            if extra_in_2:
                print(f"    Extra:   {extra_in_2}")

print(f"\n{'=' * 120}")
print("SUMMARY")
print(f"{'=' * 120}")

file1_correct = all(sorted(ens1_data.get(exi, [])) == sorted(csv_data.get(exi, [])) for exi in all_exi)
file2_correct = all(sorted(ens2_data.get(exi, [])) == sorted(csv_data.get(exi, [])) for exi in all_exi)

print(f"\nFile 1 matches CSV: {file1_correct}")
print(f"File 2 matches CSV: {file2_correct}")

if not file1_correct:
    print("\nFile 1 issues found - differences exist")
if not file2_correct:
    print("\nFile 2 issues found - differences exist")
