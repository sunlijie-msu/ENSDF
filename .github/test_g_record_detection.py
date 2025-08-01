#!/usr/bin/env python3
"""
Test G-record identification logic
"""

def is_level_record(line):
    """True if line is an L-record (level record) - NOT a comment"""
    if len(line) < 9:
        return False
    # Position 8 = 'L', position 9 = ' ', and not a comment line
    return (line[7] == 'L' and line[8] == ' ' and 
            (len(line) <= 6 or (line[5] == ' ' and line[6] != 'c')))

def is_gamma_record(line):
    """True if line is a G-record (gamma record) - NOT a comment"""
    if len(line) < 9:
        return False
    # Position 8 = 'G', position 9 = ' ', and not a comment line
    return (line[7] == 'G' and line[8] == ' ' and 
            (len(line) <= 6 or (line[5] == ' ' and line[6] != 'c')))

def extract_gamma_energy(line):
    """Extract gamma energy from G-record line (columns 10-19)"""
    try:
        energy_field = line[9:19].strip()
        if energy_field:
            return float(energy_field.split()[0])
        return 999999.0
    except (ValueError, IndexError):
        return 999999.0

# Test lines from the S35 file
test_lines = [
    " 35S   L 4189.280  21 1/2-             35 FS     LT                             ",
    " 35S X L XREF=FHI(4190*)JK(4186*)L                                              ",
    " 35S  cL T$from |t<50 fs ((d,p|g), 1972Fr11, DSAM).                             ",
    " 35S  cL J$ L(pol d,p)=1 and L-1/2 from analyzing powers.                       ",
    " 35S   G 387         7.7     LT [M1,E2]                                         ",
    " 35S   G 597         7.7     LT [E1]                                            ",
    " 35S   G 631.32    24 2.8    LT                                             &   ",
    " 35S  cG E,RI$from (n,|g) E=thermal                                             ",
    " 35S   G 768         7.7     LT [M2]                                            ",
    " 35S   G 1250.61   5 8.4     10 [E1]                                            ",
    " 35S  cG E,RI$from (n,|g) E=thermal                                             ",
    " 35S   G 1471        9.6     LT [M2]                                            ",
    " 35S   G 1840.2    12 91     10 [M1,E2]                                         ",
    " 35S  cG RI$weighted average of 87 {I16} from (n,|g) E=thermal and 92 {I10} from",
    " 35S 2cG (d,p|g)                                                                ",
    " 35S  cG E$from (n,|g) E=thermal                                                ",
    " 35S  dG $RI$1972Dz13 gives 3.6 {I8}.                                           ",
    " 35S   G 2196        15      LT [M3]                                            ",
    " 35S   G 2616.8    13 9.5    28 [E1]                                            ",
    " 35S  cG E,RI$from (n,|g) E=thermal                                             ",
    " 35S  dG $RI$1972Dz13 gives 1.3 {I4}.                                           ",
    " 35S   G 4188.95   5 100     10 [E1]                                            ",
    " 35S  cG RI$from (d,p|g). Other: 100 {I11} from (n,|g) E=thermal                ",
    " 35S  cG E$from (n,|g) E=thermal                                                ",
    " 35S  dG $RI$1985Ke08 gives 24 {I2}.                                            "
]

print("Testing G-record identification:")
print("Position: 12345678901234567890")
print("         1         2")
print()

gamma_records = []
for i, line in enumerate(test_lines):
    if is_level_record(line):
        print(f"Line {i+1:2d}: L-RECORD  '{line[:20]}...'")
    elif is_gamma_record(line):
        energy = extract_gamma_energy(line)
        gamma_records.append((i+1, energy))
        print(f"Line {i+1:2d}: G-RECORD  Energy: {energy:8.2f} keV  '{line[:30]}...'")
    else:
        record_type = "COMMENT" if 'c' in line[5:7] else "OTHER"
        print(f"Line {i+1:2d}: {record_type:8s}  '{line[:30]}...'")

print(f"\nFound G-records with energies: {[e for _, e in gamma_records]}")
print(f"Correct order: {sorted([e for _, e in gamma_records])}")
print(f"Currently in order: {[e for _, e in gamma_records] == sorted([e for _, e in gamma_records])}")
