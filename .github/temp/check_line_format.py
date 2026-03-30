"""Check actual line content vs expected for spot-check verification."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# Check a sample J$ line
j_positions = [i for i, l in enumerate(lines) if 'J$From {+33}S(p,p):resonances based R-matrix' in l]
sample_pos = j_positions[5]
actual = lines[sample_pos]
print(f'J$ line {sample_pos+1} repr: {repr(actual)}')
print(f'Length (with newline): {len(actual)}')
print(f'Length (stripped): {len(actual.rstrip())}')
expected_bare = ' 34CL cL J$From {+33}S(p,p):resonances based R-matrix analysis (1989Va15)'
print(f'Expected bare length: {len(expected_bare)}')
print(f'Match (stripped vs bare): {actual.rstrip() == expected_bare}')
print(f'Match (stripped vs ljust80): {actual.rstrip() == expected_bare.ljust(80)}')

# Check E$ line for 3He reaction
e_positions = [i for i, l in enumerate(lines) if 'cG E$From {+32}S' in l]
ep = e_positions[0]
ae = lines[ep]
print(f'\nE$(He) line {ep+1} repr: {repr(ae)}')
print(f'Length stripped: {len(ae.rstrip())}')
exp_e = ' 34CL cG E$From {+32}S({+3}He,p|g)'
print(f'Expected E$ bare length: {len(exp_e)}')
print(f'Match bare: {ae.rstrip() == exp_e}')
print(f'Match ljust80: {ae.rstrip() == exp_e.ljust(80)}')

# Check RI$ line
ri_positions = [i for i, l in enumerate(lines) if 'cG RI$From {+32}S' in l]
rp = ri_positions[0]
ar = lines[rp]
print(f'\nRI$(He) line {rp+1} repr: {repr(ar)}')
print(f'Length stripped: {len(ar.rstrip())}')
exp_ri = ' 34CL cG RI$From {+32}S({+3}He,p|g)'
print(f'Expected RI$ bare length: {len(exp_ri)}')
print(f'Match bare: {ar.rstrip() == exp_ri}')
