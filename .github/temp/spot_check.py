"""Spot-check the flag expansion results."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

# Count new comment lines added
j_lines = [l for l in lines if 'J$From {+33}S(p,p):resonances based R-matrix' in l]
cg_e_lines = [l for l in lines if 'cG E$From {+32}S({+3}He,p' in l]
cg_ri_lines = [l for l in lines if 'cG RI$From {+32}S({+3}He,p' in l]
cl_e_from_lines = [l for l in lines if 'cL E$From {+32}S({+3}He,p' in l]

print(f'Total cL J$ (flag b) expansions: {len(j_lines)}')
print(f'Total cG E$From(3He) (flag A) expansions: {len(cg_e_lines)}')
print(f'Total cG RI$From(3He) (flag B) expansions: {len(cg_ri_lines)}')
print(f'Total cL E$From(3He) (flag a) - should be 0 (deleted only): {len(cl_e_from_lines)}')

# Remaining FLAG=
flag_count = sum(1 for l in lines if 'FLAG=' in l)
print(f'\nRemaining FLAG= lines: {flag_count}')

# Show 5 sample J$ lines with their preceding L-record
print('\n=== Sample J$ expansions ===')
for i, line in enumerate(lines):
    if 'J$From {+33}S(p,p):resonances based R-matrix' in line:
        # Find preceding L data record
        for k in range(i-1, max(0, i-8), -1):
            if len(lines[k]) > 8 and lines[k][6]==' ' and lines[k][7]=='L':
                e = lines[k][9:19].strip()
                print(f'  L {e}: line {i+1}: {repr(line.rstrip()[:60])}')
                break
        # Only show up to 5
        if sum(1 for l in lines[:i+1] if 'J$From {+33}S(p,p):resonances' in l) >= 5:
            break

# Show 5 sample E$ expansions
print('\n=== Sample cG E$From expansions ===')
count = 0
for i, line in enumerate(lines):
    if 'cG E$From {+32}S({+3}He,p' in line:
        print(f'  Line {i+1}: {repr(line.rstrip()[:60])}')
        count += 1
        if count >= 5:
            break

# Show 5 sample RI$ expansions
print('\n=== Sample cG RI$From expansions ===')
count = 0
for i, line in enumerate(lines):
    if 'cG RI$From {+32}S({+3}He,p' in line:
        print(f'  Line {i+1}: {repr(line.rstrip()[:60])}')
        count += 1
        if count >= 5:
            break
