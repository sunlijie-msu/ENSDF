#!/usr/bin/env python3
"""
Generate corrected ENSDF file from CSV source with proper ENSDF formatting
"""

# Authoritative data from CSV analysis (all 85 gammas with correct Egamma = Exi - Exf)
levels_data = {
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

output = []

# Header records
output.append(" 35CL    2001Vo24                      2001Vo24                             ")
output.append(" 35CL cL S$LABEL=E{-p}(lab) (keV)                                          ")
output.append(" 35CL PN                                                                7  ")

# Generate L and G records for each level
for exi in sorted(levels_data.keys()):
    gammas = levels_data[exi]
    
    # L-record: format is " NUCID  L ENERGY"
    # Columns: 1-5 NUCID, 6-7 spaces, 8 L, 9 space, 10-19 energy
    if exi == 0:
        # Ground state - special formatting
        l_record = " 35CL  L 0"
    else:
        # Format: " NUCID  L EEEE.E" with energy left-justified at column 10-19
        energy_str = str(exi)
        l_record = f" 35CL  L {energy_str}"
    
    # Pad to 80 characters
    l_record = l_record.ljust(80)
    output.append(l_record)
    
    # G-records for this level (already sorted in ascending order by CSV)
    for egamma, ri in sorted(gammas):
        # G-record format: " NUCID  G EEEE.E    RI"
        # Columns: 1-5 NUCID, 6-7 spaces, 8 G, 9 space, 10-19 energy, 20-21 space, 22-29 RI
        energy_str = str(egamma)
        ri_str = str(ri)
        g_record = f" 35CL  G {energy_str}         {ri_str}"
        
        # Pad to 80 characters
        g_record = g_record.ljust(80)
        output.append(g_record)

# Footer record
footer = " 35CL  c 0"
footer = footer.ljust(80)
output.append(footer)

# Write output file
output_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24_1st_extracted_CORRECTED.ens'
with open(output_file, 'w') as f:
    for line in output:
        f.write(line[:80] + '\n')  # Ensure exactly 80 chars per line

print(f"Generated corrected ENSDF file: {output_file}")
print(f"Total lines: {len(output)}")

# Count gammas
total_gammas = sum(len(gammas) for gammas in levels_data.values())
print(f"Total gammas: {total_gammas}")
print()

# Display structure preview
for exi in sorted(levels_data.keys()):
    print(f"Level {exi:5d} keV: {len(levels_data[exi]):2d} gammas")
