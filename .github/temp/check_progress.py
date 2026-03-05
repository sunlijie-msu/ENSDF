#!/usr/bin/env python3
"""
Script to verify which |w|g entries from 1983Wa27 have been added
"""

# Map of E_p -> (wg_val, unc_int)
entries_map = {
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

import re

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'r') as f:
    content = f.read()

found = []
missing = []

for ep in entries_map.keys():
    wg_val, unc_int = entries_map[ep]
    pattern = f"|w|g={wg_val} {{I{unc_int}}} \\(1983Wa27\\)"
    if re.search(pattern, content):
        found.append(ep)
    else:
        missing.append(ep)

print(f"Already added: {len(found)} entries")
print(f"Still missing: {len(missing)} entries")
print()
print("Missing E(p) values:")
for ep in sorted(missing):
    wg_val, unc_int = entries_map[ep]
    print(f"  {ep:7.1f}: |w|g={wg_val} {{I{unc_int}}}")
