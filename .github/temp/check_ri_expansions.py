"""Check which G records have RI$ From (3He)."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

print('G records with cG RI$From(3He):')
for i, l in enumerate(lines):
    if 'cG RI$From {+32}S({+3}He,p' in l:
        for k in range(i-1, max(0, i-8), -1):
            if len(lines[k]) > 8 and lines[k][6]==' ' and lines[k][7]=='G':
                e = lines[k][9:19].strip()
                print(f'  G {e}: RI$ at line {i+1}')
                break
