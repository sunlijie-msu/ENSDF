"""Verify FLAG=C expansions and perform systematic spot-check."""
import random

with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# 1. Check FLAG=C expansions (cG E$ from Mg/Al reactions)
print('=== FLAG=C E$ expansions ===')
for i, l in enumerate(lines):
    if 'cG E$From {+24}Mg' in l or 'cG E$From {+27}Al' in l:
        for k in range(i-1, max(0, i-8), -1):
            if len(lines[k]) > 8 and lines[k][6]==' ' and lines[k][7]=='G':
                print(f'  G {lines[k][9:19].strip()}: E$ at line {i+1}')
                print(f'    text: {repr(l.rstrip()[:60])}')
                break

# 2. Check that no FLAG= lines remain
remaining_flags = [(i+1, l.rstrip()) for i, l in enumerate(lines) if 'FLAG=' in l]
print(f'\nRemaining FLAG= lines: {len(remaining_flags)}')

# 3. Comprehensive spot-check: verify 15% of expansions
# Total expansions = 140 J$ + 16 E$A + 7 RI$B + 2 E$C + 6 a_delete + 18 AB_delete + others = ~200
# Spot check 30 random J$ expansions

print('\n=== Random spot-check: 30 J$ expansions ===')
j_positions = [i for i, l in enumerate(lines) if 'J$From {+33}S(p,p):resonances based R-matrix' in l]
print(f'Total J$ expansions found: {len(j_positions)}')

random.seed(42)
sample = random.sample(j_positions, min(30, len(j_positions)))
sample.sort()
errors = []
for pos in sample:
    # Verify J$ line content
    l = lines[pos]
    expected = ' 34CL cL J$From {+33}S(p,p):resonances based R-matrix analysis (1989Va15)'
    actual = l.rstrip()
    if actual != expected.ljust(80):
        errors.append(f'Line {pos+1}: expected {expected[:40]}... got {repr(actual[:40])}')

print(f'Checked: {len(sample)} samples')
print(f'Errors: {len(errors)}')
for e in errors:
    print(f'  {e}')

# 4. Verify E$ From(3He) line format
print('\n=== E$From(3He) line format check ===')
e_positions = [i for i, l in enumerate(lines) if 'cG E$From {+32}S({+3}He,p' in l]
expected_e = ' 34CL cG E$From {+32}S({+3}He,p|g)'.ljust(80)
for pos in e_positions:
    actual = lines[pos].rstrip()
    if actual != expected_e:
        print(f'  Line {pos+1} mismatch: got {repr(actual[:50])}')
print(f'All {len(e_positions)} cG E$From(3He) lines: ', 'OK' if all(lines[pos].rstrip()==expected_e for pos in e_positions) else 'ISSUES')

# 5. Verify RI$ From(3He) line format
print('\n=== RI$From(3He) line format check ===')
ri_positions = [i for i, l in enumerate(lines) if 'cG RI$From {+32}S({+3}He,p' in l]
expected_ri = ' 34CL cG RI$From {+32}S({+3}He,p|g)'.ljust(80)
for pos in ri_positions:
    actual = lines[pos].rstrip()
    if actual != expected_ri:
        print(f'  Line {pos+1} mismatch: got {repr(actual[:50])}')
print(f'All {len(ri_positions)} cG RI$From(3He) lines: ', 'OK' if all(lines[pos].rstrip()==expected_ri for pos in ri_positions) else 'ISSUES')

print('\n=== Summary ===')
print(f'Total FLAG= remaining: {len(remaining_flags)}')
print(f'J$ expansions: {len(j_positions)}')
print(f'E$From(3He) expansions: {len(e_positions)}')
print(f'RI$From(3He) expansions: {len(ri_positions)}')
