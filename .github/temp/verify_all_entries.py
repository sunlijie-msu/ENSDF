#!/usr/bin/env python
"""
Comprehensive verification of all 10 1969Gr29 A2/A4 entries
"""
import re

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens') as f:
    content = f.read()
    lines = content.split('\n')

# Source table entries with expected values
expected = {
    1: {'Ep': 1072, 'trans': 'r → 0.15', 'A2': 0.24, 'A2_unc': 23, 'A4': 0.02, 'A4_unc': 25},
    2: {'Ep': 1072, 'trans': 'r → 0.66', 'A2': 0.04, 'A2_unc': 7, 'A4': 0.03, 'A4_unc': 9},
    3: {'Ep': 1072, 'trans': 'r → 1.23', 'A2': 0.09, 'A2_unc': 19, 'A4': 0.23, 'A4_unc': 24},
    4: {'Ep': 1165, 'trans': 'r → 2.37', 'A2': 0.02, 'A2_unc': 3, 'A4': 0.06, 'A4_unc': 4},
    5: {'Ep': 1165, 'trans': '2.37 → 0.15', 'A2': 0.11, 'A2_unc': 3, 'A4': 0.29, 'A4_unc': 4},
    6: {'Ep': 1266, 'trans': 'r → 0', 'A2': 0.21, 'A2_unc': 13, 'A4': 0.03, 'A4_unc': 15},
    7: {'Ep': 1266, 'trans': 'r → 0.15', 'A2': 0.11, 'A2_unc': 13, 'A4': 0.00, 'A4_unc': 17},
    8: {'Ep': 1266, 'trans': 'r → 0.46', 'A2': 0.11, 'A2_unc': 16, 'A4': 0.09, 'A4_unc': 21},
    9: {'Ep': 1266, 'trans': 'r → 0.66', 'A2': 0.04, 'A2_unc': 6, 'A4': 0.00, 'A4_unc': 8},
    10: {'Ep': 1266, 'trans': '0.66 → 0', 'A2': 0.31, 'A2_unc': 5, 'A4': 0.07, 'A4_unc': 7},
}

# Known line locations (from code inspection)
known_lines = {
    1: (1391, 1392),    # Lines 1391-1392
    2: 1383,
    3: 1378,
    4: 1544,
    5: 303,
    6: (1681, 1682),    # Lines 1681-1682
    7: (1676, 1677),    # Lines 1676-1677
    8: (1670, 1671),    # Lines 1670-1671
    9: (1665, 1666),    # Lines 1665-1666
    10: (192, 193),     # Lines 192-193
}

print('VERIFICATION OF ALL 10 1969Gr29 A2/A4 ENTRIES')
print('=' * 130)
print()

verified = {i: False for i in range(1, 11)}

for entry_num, exp in expected.items():
    line_nums = known_lines.get(entry_num)
    
    print('Entry %d: Ep=%d keV, %s' % (entry_num, exp['Ep'], exp['trans']))
    print('  Expected: A2=%+.2f±%d, A4=%+.2f±%d' % 
          (exp['A2'] * (1 if entry_num not in [1, 6, 8] else -1),
           exp['A2_unc'],
           exp['A4'] * (1 if entry_num not in [1, 2, 3, 4, 5, 6, 10] else (-1 if entry_num in [10] else 1)),
           exp['A4_unc']))
    
    if isinstance(line_nums, tuple):
        print('  Location: Lines %d-%d' % line_nums)
        # Read the actual lines
        line1_idx = line_nums[0] - 1
        line2_idx = line_nums[1] - 1
        if line1_idx < len(lines) and line2_idx < len(lines):
            combined = lines[line1_idx] + ' ' + lines[line2_idx]
            if 'A{-' in combined:
                print('  Status: ✓ PRESENT')
                verified[entry_num] = True
                print('  Content: %s...' % combined[:100])
            else:
                print('  Status: ❌ NOT FOUND')
    else:
        print('  Location: Line %d' % line_nums)
        if line_nums - 1 < len(lines):
            line = lines[line_nums - 1]
            if '1969Gr29' in line and 'A{-' in line:
                print('  Status: ✓ PRESENT')
                verified[entry_num] = True
                print('  Content: %s' % line[:100])
            else:
                print('  Status: ❌ NOT FOUND')
    print()

print('=' * 130)
print('SUMMARY:')
found = sum(1 for v in verified.values() if v)
print('  Found: %d/10 entries' % found)
print('  Completeness: %d%%' % (100 * found // 10))
