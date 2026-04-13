"""
Read-only analysis: derive L-transfer field (cols 56-64) from Jπ for each L-record.
Physics: 36S(p,d)35S — neutron pickup from J=0+ target.
  L=0 → Jπ = 1/2+
  L=1 → Jπ = 1/2- or 3/2-
  L=2 → Jπ = 3/2+ or 5/2+
  L=3 → Jπ = 5/2- or 7/2-
  L=4 → Jπ = 7/2+ or 9/2+
  Parentheses in Jπ → parentheses in L (tentative)
  No parentheses in Jπ → no parentheses in L (firm)
"""

filepath = r"D:\X\ND\ENSDF\A35\S35\new\S35_36s_p_d.ens"

# Map Jπ string → (L_digit, tentative)
# Jπ is extracted from cols 23-39 (17-char field), stripped
JP_TO_L = {
    # Firm assignments
    "1/2+":         ("0", False),
    "3/2+":         ("2", False),
    "5/2+":         ("2", False),
    "7/2+":         ("4", False),
    "9/2+":         ("4", False),
    "1/2-":         ("1", False),
    "3/2-":         ("1", False),
    "5/2-":         ("3", False),
    "7/2-":         ("3", False),
    "1/2-,3/2-":    ("1", False),  # both from L=1
    "3/2+,5/2+":    ("2", False),  # both from L=2
    # Tentative assignments
    "(1/2+)":       ("0", True),
    "(3/2+)":       ("2", True),
    "(5/2+)":       ("2", True),
    "(7/2+)":       ("4", True),
    "(9/2+)":       ("4", True),
    "(1/2-)":       ("1", True),
    "(3/2-)":       ("1", True),
    "(5/2-)":       ("3", True),
    "(7/2-)":       ("3", True),
    "(1/2-,3/2-)":  ("1", True),
    "(3/2+,5/2+)":  ("2", True),
}

def make_L_field(L_digit, tentative):
    """Generate 9-char L field string."""
    if tentative:
        s = f"({L_digit})"   # 3 chars
        return s + " " * 6   # 3 + 6 = 9
    else:
        return L_digit + " " * 8  # 1 + 8 = 9

with open(filepath, "r") as f:
    lines = f.readlines()

print(f"{'#':>3} {'E-field':12} {'Jπ':14} {'Deduced L':10} {'L field repr':12}")
print("-" * 60)

changes = []
skipped = []

for i, raw_line in enumerate(lines):
    line = raw_line.rstrip("\n")
    if len(line) != 80:
        continue
    # Check if it's a data L-record (col 6 is blank/space, col 8 is 'L')
    if line[5] != " " or line[7] != "L" or line[6] != " " or line[8] != " ":
        continue

    jp_raw = line[22:39]  # cols 23-39 (0-indexed: 22-38), 17 chars
    jp_stripped = jp_raw.strip()
    cur_L = line[55:64]   # cols 56-64 (0-indexed: 55-64), 9 chars
    E_field = line[9:19].strip()  # energy

    if not jp_stripped:
        skipped.append((i+1, E_field, "no Jπ → no L assigned"))
        continue

    if jp_stripped not in JP_TO_L:
        skipped.append((i+1, E_field, f"UNMAPPED Jπ={jp_stripped!r}"))
        continue

    L_digit, tentative = JP_TO_L[jp_stripped]
    new_L_field = make_L_field(L_digit, tentative)

    if len(new_L_field) != 9:
        print(f"ERROR: L field length {len(new_L_field)} != 9 for Jπ={jp_stripped}")
        continue

    # Verify current L field is blank
    if cur_L.strip() != "":
        print(f"WARNING: Line {i+1}, E={E_field}: L field already has content: {cur_L!r}")

    new_line = line[:55] + new_L_field + line[64:]
    if len(new_line) != 80:
        print(f"ERROR: Line {i+1}: new line length {len(new_line)} != 80!")
        continue

    L_repr = f"L=({L_digit})" if tentative else f"L={L_digit}"
    print(f"{i+1:>3} {E_field:12} {jp_stripped:14} {L_repr:10} |{new_L_field}|")
    changes.append((line, new_line, i+1, E_field))

print()
print(f"Total L-records to update: {len(changes)}")
print()
if skipped:
    print("Skipped records:")
    for ln, E, reason in skipped:
        print(f"  Line {ln}: E={E} — {reason}")

print()
print("=== FULL LINE VERIFICATION (sample: first 5) ===")
for old, new, ln, E in changes[:5]:
    print(f"Line {ln} (E={E}):")
    print(f"  OLD:{old!r}")
    print(f"  NEW:{new!r}")
    assert len(old) == 80, f"OLD line length error: {len(old)}"
    assert len(new) == 80, f"NEW line length error: {len(new)}"
    diff_positions = [j for j in range(80) if old[j] != new[j]]
    print(f"  Changed at cols: {[p+1 for p in diff_positions]}")
    print()

# Verify all old lines are unique
old_lines = [c[0] for c in changes]
if len(old_lines) != len(set(old_lines)):
    print("WARNING: Duplicate old lines detected! Non-unique oldStrings.")
else:
    print(f"Uniqueness check: all {len(old_lines)} old lines are unique. ✓")
