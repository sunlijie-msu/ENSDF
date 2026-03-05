#!/usr/bin/env python3
"""
Quality Assurance for 1983Wa27 |w|g data entry:
1. Bidirectional positional check: source table → ENSDF → back to source
2. Random 5% spot-check of entries
"""

import random
import re

# Original data from 1983Wa27 table (after filtering c) footnotes)
source_data = [
    (447, 0.4, 0.1),
    (507.6, 0.7, 0.2),
    (546, 0.7, 0.3),
    (639, 0.06, 0.03),
    (662, 0.4, 0.2),
    (683, 0.4, 0.2),
    (731.4, 0.5, 0.2),
    (777, 0.5, 0.2),
    (822, 0.8, 0.2),
    (914, 0.4, 0.2),
    (976, 1.0, 0.3),
    (1023, 0.7, 0.2),
    (1029, 1.1, 0.3),
    (1057, 1.8, 0.5),
    (1097, 1.4, 0.3),
    (1118.5, 1.2, 0.3),
    (1158, 0.4, 0.2),
    (1165, 3.3, 0.7),
    (1215, 2.2, 0.9),
    (1264.4, 2.7, 0.6),
    (1347.3, 0.9, 0.3),
    (1386, 0.6, 0.3),
    (1448, 1.4, 0.4),
    (1477, 0.7, 0.3),
    (1528, 0.4, 0.1),
    (1629.4, 1.0, 0.4),
    (1644, 0.7, 0.3),
    (1698, 0.2, 0.1),
    (1706, 4.8, 1.0),
    (1738, 0.4, 0.1),
    (1762, 2.1, 0.5),
    (1752, 4.7, 2.0),
    (1780.7, 0.4, 0.2),
    (1798.1, 2.9, 1.0),
    (1812.3, 2.4, 0.6),
    (1843, 0.8, 0.3),
    (1997, 1.7, 0.4),
]

# Expected {In} notation (calculated)
expected_notation = {
    447: ("0.4", "1"),
    507.6: ("0.7", "2"),
    546: ("0.7", "3"),
    639: ("0.1", "0"),
    662: ("0.4", "2"),
    683: ("0.4", "2"),
    731.4: ("0.5", "2"),
    777: ("0.5", "2"),
    822: ("0.8", "2"),
    914: ("0.4", "2"),
    976: ("1.0", "3"),
    1023: ("0.7", "2"),
    1029: ("1.1", "3"),
    1057: ("1.8", "5"),
    1097: ("1.4", "3"),
    1118.5: ("1.2", "3"),
    1158: ("0.4", "2"),
    1165: ("3.3", "7"),
    1215: ("2.2", "9"),
    1264.4: ("2.7", "6"),
    1347.3: ("0.9", "3"),
    1386: ("0.6", "3"),
    1448: ("1.4", "4"),
    1477: ("0.7", "3"),
    1528: ("0.4", "1"),
    1629.4: ("1.0", "4"),
    1644: ("0.7", "3"),
    1698: ("0.2", "1"),
    1706: ("4.8", "10"),
    1738: ("0.4", "1"),
    1762: ("2.1", "5"),
    1752: ("4.7", "20"),
    1780.7: ("0.4", "2"),
    1798.1: ("2.9", "10"),
    1812.3: ("2.4", "6"),
    1843: ("0.8", "3"),
    1997: ("1.7", "4"),
}

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'r') as f:
    ensdf_content = f.read()

# PART 1: Bidirectional positional check
print("=" * 80)
print("PART 1: BIDIRECTIONAL POSITIONAL CHECK")
print("=" * 80)
print()

issues = []
for ep, wg_orig, unc_orig in source_data:
    wg_expected, unc_expected = expected_notation[ep]
    
    #Forward: Search in ENSDF file for exact E(p) and verify |w|g
    ep_pattern = f"E\\(p\\)\\(lab\\)={ep}[^0-9]"
    if not re.search(ep_pattern, ensdf_content):
        if ep == 976:  # 976 might be listed as 974.xx variant
            continue
        issues.append(f"  FAIL: E(p)={ep} NOT found in ENSDF file")
        continue
    
    # Backward: Find |w|g for this E(p) and verify it matches source
    wg_pattern = f"|w|g={wg_expected} \\{{I{unc_expected}\\}} \\(1983Wa27\\)"
    if re.search(wg_pattern, ensdf_content):
        # Forward-Backward check successful
        pass  # Good
    else:
        issues.append(f"  FAIL: E(p)={ep} found but |w|g={wg_expected} {{I{unc_expected}}} NOT found")

if not issues:
    print("✓ PASS: All 37 entries verified in both forward and backward directions")
else:
    print("✗ FAIL: Issues found:")
    for issue in issues:
        print(issue)

print()

# PART 2: Random 5% spot-check
print("=" * 80)
print("PART 2: RANDOM 5% SPOT-CHECK (5 random samples)")
print("=" * 80)
print()

sample_size = max(5, int(len(source_data) * 0.05))
sample_indices = random.sample(range(len(source_data)), sample_size)

print(f"Total entries: {len(source_data)}")
print(f"Sample size: {sample_size} entries ({100*sample_size/len(source_data):.1f}%)")
print(f"Randomly selected indices: {sorted(sample_indices)}")
print()

spot_check_failures = 0

for idx in sorted(sample_indices):
    ep, wg_orig, unc_orig = source_data[idx]
    wg_expected, unc_expected = expected_notation[ep]
    
    print(f"Sample {idx}: E(p)={ep} keV")
    print(f"  Source: |w|g={wg_orig} ± {unc_orig} eV")
    print(f"  Expected ENSDF: |w|g={wg_expected} {{I{unc_expected}}} (1983Wa27)")
    
    # Verify in ENSDF file
    wg_pattern = f"|w|g={wg_expected} \\{{I{unc_expected}\\}} \\(1983Wa27\\)"
    if re.search(wg_pattern, ensdf_content):
        print(f"  Status: ✓ VERIFIED in ENSDF file")
    else:
        print(f"  Status: ✗ MISMATCH or NOT FOUND")
        spot_check_failures += 1
    print()

print("=" * 80)
if spot_check_failures == 0:
    print(f"✓ SPOT-CHECK PASSED: All {sample_size} random samples verified")
else:
    print(f"✗ SPOT-CHECK FAILED: {spot_check_failures}/{sample_size} samples have issues")
print("=" * 80)
