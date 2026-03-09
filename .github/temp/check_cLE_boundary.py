ENS = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
lines = open(ENS, encoding='utf-8').readlines()

def is_L(l):
    return len(l) >= 8 and l[5] == ' ' and l[6] == ' ' and l[7] == 'L'

def is_cLE(l):
    return len(l) >= 12 and l[6] == 'c' and l[7] == 'L' and l[9] == 'E' and l[10] == '$'

def L_energy(l):
    return l[9:19].strip()

boundary = None
for i, l in enumerate(lines):
    if is_L(l) and L_energy(l) == '6136.2':
        boundary = i
        break

print(f'L 6136.2 at line {boundary + 1}')

before = [(i, lines[i].rstrip()) for i in range(boundary) if is_cLE(lines[i])]
after  = [(i, lines[i].rstrip()) for i in range(boundary + 1, len(lines)) if is_cLE(lines[i])]

print(f'cL E$ before boundary: {len(before)}')
print(f'cL E$ after  boundary: {len(after)}')
for ln, txt in after:
    print(f'  Line {ln + 1}: {txt[:70]}')
