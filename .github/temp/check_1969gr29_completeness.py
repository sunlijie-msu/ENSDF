#!/usr/bin/env python
"""
Cross-check 1969Gr29 angular distribution coefficients (A2, A4) against source table
"""

# Source table from 1969Gr29 Table III
source = {
    1: {'Ep': 1072, 'trans': 'r → 0.15', 'A2': (-0.24, 23), 'A4': (-0.02, 25)},
    2: {'Ep': 1072, 'trans': 'r → 0.66', 'A2': (-0.04, 7), 'A4': (-0.03, 9)},
    3: {'Ep': 1072, 'trans': 'r → 1.23', 'A2': (0.09, 19), 'A4': (-0.23, 24)},
    4: {'Ep': 1165, 'trans': 'r → 2.37', 'A2': (0.02, 3), 'A4': (-0.06, 4)},
    5: {'Ep': 1165, 'trans': '2.37 → 0.15', 'A2': (0.11, 3), 'A4': (-0.29, 4)},
    6: {'Ep': 1266, 'trans': 'r → 0', 'A2': (-0.21, 13), 'A4': (-0.03, 15)},
    7: {'Ep': 1266, 'trans': 'r → 0.15', 'A2': (0.11, 13), 'A4': (0.00, 17)},
    8: {'Ep': 1266, 'trans': 'r → 0.46', 'A2': (-0.11, 16), 'A4': (0.09, 21)},
    9: {'Ep': 1266, 'trans': 'r → 0.66', 'A2': (-0.04, 6), 'A4': (0.00, 8)},
    10: {'Ep': 1266, 'trans': '0.66 → 0', 'A2': (0.31, 5), 'A4': (-0.07, 7)},
}

# Found entries (manually matched from ENSDF file)
found = [
    {'line': 303, 'A2': 0.11, 'A2_unc': 3, 'A4': -0.29, 'A4_unc': 4, 'source_num': 5},  # 1165, 2.37 → 0.15
    {'line': 1378, 'A2': 0.09, 'A2_unc': 19, 'A4': -0.23, 'A4_unc': 24, 'source_num': 3},  # 1072, r → 1.23
    {'line': 1383, 'A2': -0.04, 'A2_unc': 7, 'A4': -0.03, 'A4_unc': 9, 'source_num': 2},  # 1072, r → 0.66
    {'line': 1544, 'A2': 0.02, 'A2_unc': 3, 'A4': -0.06, 'A4_unc': 4, 'source_num': 4},  # 1165, r → 2.37
]

print('VERIFICATION OF 1969Gr29 ANGULAR DISTRIBUTION COEFFICIENTS')
print('=' * 120)
print()
print('FOUND ENTRIES (with value verification):')
print('-' * 120)
for f in found:
    s_num = f['source_num']
    s_data = source[s_num]
    s_a2_val, s_a2_unc = s_data['A2']
    s_a4_val, s_a4_unc = s_data['A4']
    
    print('Entry %d (Ep=%d keV, %s):' % (s_num, s_data['Ep'], s_data['trans']))
    print('  ENSDF Line %d: A2=%+.2f±%d, A4=%+.2f±%d' % 
          (f['line'], f['A2'], f['A2_unc'], f['A4'], f['A4_unc']))
    print('  SOURCE:        A2=%+.2f±%d, A4=%+.2f±%d' % 
          (s_a2_val, s_a2_unc, s_a4_val, s_a4_unc))
    
    # Check agreement
    a2_match = abs(f['A2'] - s_a2_val) < 0.01 and f['A2_unc'] == s_a2_unc
    a4_match = abs(f['A4'] - s_a4_val) < 0.01 and f['A4_unc'] == s_a4_unc
    
    if a2_match and a4_match:
        print('  ✓ MATCH: Values and uncertainties agree\n')
    else:
        print('  ❌ MISMATCH: Values do not match\n')

print('=' * 120)
print('MISSING ENTRIES:')
print('-' * 120)
found_nums = set(f['source_num'] for f in found)
missing = [n for n in range(1, 11) if n not in found_nums]
for s_num in sorted(missing):
    s_data = source[s_num]
    s_a2_val, s_a2_unc = s_data['A2']
    s_a4_val, s_a4_unc = s_data['A4']
    print('Entry %d (Ep=%d keV, %s): A2=%+.2f±%d, A4=%+.2f±%d' % 
          (s_num, s_data['Ep'], s_data['trans'], s_a2_val, s_a2_unc, s_a4_val, s_a4_unc))

print()
print('=' * 120)
print('SUMMARY:')
print('  Total entries in source table: 10')
print('  Found in ENSDF file: %d' % len(found))
print('  Missing: %d' % len(missing))
print('  Completeness: %d%%' % (100 * len(found) // 10))
print()
print('Missing entry numbers: %s' % missing)
