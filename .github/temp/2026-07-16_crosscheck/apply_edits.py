"""Apply level energy corrections to ENSDF file based on source revised.md"""
import sys

filepath = r'XUNDL\2026MAAA_CT11001_141Sm.ens'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Track changes
changes = []

# Map: old_line_substring -> new_line_substring (must uniquely match)
# Each tuple contains enough unique context for unambiguous matching
replacements = [
    # (old, new) - exact substrings
    ('141SM  L 4482.4    6  33/2', '141SM  L 4482.0    6  33/2'),
    ('141SM  L 4769.5    6  35/2', '141SM  L 4769.1    6  35/2'),
    ('141SM  L 5097.3    7  37/2', '141SM  L 5096.9    6  37/2'),
    ('141SM  L 5365.5    7  (35/2-)', '141SM  L 5366.2    6  (35/2-)'),
    ('141SM  L 5434.3    7  39/2', '141SM  L 5433.9    6  39/2'),
    ('141SM  L 5575.7    7  37/2                                                  D', '141SM  L 5576.3    6  37/2                                                  D'),
    ('141SM  L 5640.5    7  37/2(-)', '141SM  L 5641.1    6  37/2(-)'),
    ('141SM  L 6349.7    7  41/2                                                  D', '141SM  L 6350.3    7  41/2                                                  D'),
    ('141SM  L 6412.9    8  41/2(-)', '141SM  L 6413.4    7  41/2(-)'),
    ('141SM  L 6894.3    9  43/2(-)', '141SM  L 6894.8    7  43/2(-)'),
    ('141SM  L 7375.7    10 45/2                                                  D', '141SM  L 7376.3    7  45/2                                                  D'),
    ('141SM  L 7384.3    10 45/2(-)', '141SM  L 7384.9    7  45/2(-)'),
    ('141SM  L 8283.7    13 49/2', '141SM  L 8284.3    9  49/2'),
    ('141SM  L 8610.2    14 47/2(-)          0.39 PS   LT                         A', '141SM  L 8610.9    8  47/2(-)          0.39 PS   LT                         A'),
    ('141SM  L 12008.3   15 67/2(+)                                               E', '141SM  L 12009.0   11 67/2(+)                                               E'),
    ('141SM  L 13498.8   17 69/2(+)                                               C', '141SM  L 13499.5   12 69/2(+)                                               C'),
    ('141SM  L 14564.6   21 71/2(-)                                               B', '141SM  L 14565.2   12 71/2(-)                                               B'),
    ('141SM  L 15376.9   20 73/2(+)                                               C', '141SM  L 15377.5   12 73/2(+)                                               C'),
    # Intensity fixes
    ('141SM  G 772.0     6  2      1  (E2)                                        X', '141SM  G 772.0     6  2.0    1  (E2)                                        X'),
    ('141SM  G 1586.0    9  4      3  (E2)                                        X', '141SM  G 1586.0    9  4.0    3  (E2)                                        X'),
]

ok_count = 0
fail_count = 0

for old, new in replacements:
    count = content.count(old)
    if count == 0:
        print("NOT FOUND: " + repr(old))
        fail_count += 1
    elif count > 1:
        print("MULTIPLE (" + str(count) + "): " + repr(old))
        fail_count += 1
    else:
        content = content.replace(old, new, 1)
        print("OK: " + old[:60] + " -> " + new[:60])
        ok_count += 1

print("\nOK: " + str(ok_count) + ", FAIL: " + str(fail_count))

if fail_count == 0:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("File written successfully.")
else:
    print("File NOT written due to failures.")
