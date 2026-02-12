
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
with open(file_path, 'r') as f:
    lines = f.readlines()

# Spot checks (1-based line numbers)
spots = [
    (155, "9962", "L", "X"),
    (116, "7436", "L", "X"),
    (121, "3654", "G", "X"),
    (133, "2098", "G", "X"),
    (156, "2549", "G", "X")
]

all_pass = True
for ln, e, t, c in spots:
    line = lines[ln-1]
    res, msg = validate_line(line, e, t, c)
    if res:
        print(f"Line {ln}: PASS ({e} {t} flag={c})")
    else:
        print(f"Line {ln}: FAIL - {msg}")
        all_pass = False

if all_pass:
    print("\nRandom Spot Check: SUCCESS (100% pass rate)")
else:
    print("\nRandom Spot Check: FAILED")
    sys.exit(1)
