"""Count all RI$From(3He) lines."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

print('All cG RI$From(3He) lines:')
for i, l in enumerate(lines):
    if 'cG RI$From {+32}S({+3}He,p' in l:
        print(f'  Line {i+1}: {repr(l.rstrip()[:60])}')
        for k in range(i-1, max(0, i-10), -1):
            if len(lines[k]) > 8 and lines[k][6]==' ' and lines[k][7]=='G':
                print(f'    -> parent G: {repr(lines[k].rstrip()[:60])}')
                break

total = sum(1 for l in lines if 'cG RI$From {+32}S({+3}He,p' in l)
print(f'\nTotal: {total}')
