
import sys

def validate_line(line, expected_energy, expected_rec_type, expected_col77):
    # Energy in 10-19
    energy = line[9:19].strip()
    rec_type = line[7]
    col77 = line[76]
    
    if energy != expected_energy:
        return False, f"Energy mismatch: {energy} != {expected_energy}"
    if rec_type != expected_rec_type:
        return False, f"Record type mismatch: {rec_type} != {expected_rec_type}"
    if col77 != expected_col77:
        return False, f"Col 77 mismatch: '{col77}' != '{expected_col77}'"
    return True, "OK"

file_path = "XUNDL/2026WIAA_CN10950_32P.ens"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Corrected line numbers (1-based)
spots = [
    (74, "4899", "L", "X"),      # Level 4899
    (101, "7436", "L", "X"),     # Level 7436
    (121, "3654", "G", "X"),     # Gamma 3654
    (133, "2098", "G", "X"),     # Gamma 2098 (check this one specifically)
    (156, "2549", "G", "X"),     # Gamma 2549
    (182, "12186", "L", "X"),    # Last Level
    (183, "4773", "G", "X")      # Last Gamma
]

# Verify energy 2098
# Looking at the feed:
# line 131: 32P   L 8932      4                                                        X   
# line 132: 32P   G 2098      2  6      2                                              X   
# Wait, let me check the file content again for line numbering.
# I will print the line content in the spot check for debugging.

all_pass = True
for ln, e, t, c in spots:
    if ln > len(lines):
        print(f"Line {ln}: FAIL - line number out of range (Total lines: {len(lines)})")
        all_pass = False
        continue
    line = lines[ln-1]
    res, msg = validate_line(line, e, t, c)
    if res:
        print(f"Line {ln}: PASS ({e} {t} flag={c})")
    else:
        print(f"Line {ln}: FAIL - {msg}")
        print(f"   Content: {line.strip()}")
        all_pass = False

if all_pass:
    print("\nRandom Spot Check: SUCCESS (100% pass rate)")
else:
    print("\nRandom Spot Check: FAILED")
    sys.exit(1)
