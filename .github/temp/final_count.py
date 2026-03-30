import sys
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()
flags = [l.rstrip() for l in lines if 'FLAG=' in l]
j = sum(1 for l in lines if 'J$From {+33}S(p,p):resonances based R-matrix' in l)
e3 = sum(1 for l in lines if 'cG E$From {+32}S' in l)
ri3 = sum(1 for l in lines if 'cG RI$From {+32}S' in l)
ec = sum(1 for l in lines if 'cG E$From {+24}Mg' in l)
print(f'Remaining FLAG= lines: {len(flags)}')
print(f'cL J$From expansions: {j}')
print(f'cG E$From(3He) expansions: {e3}')
print(f'cG RI$From(3He) expansions: {ri3}')
print(f'cG E$From(C/Al) expansions: {ec}')
print(f'Total new comments: {j+e3+ri3+ec}')
