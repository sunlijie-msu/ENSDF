lines = open('A34/Cl34/raw/1977DA02_1983WA27.adp').read().splitlines()
bad = 0
for i, l in enumerate(lines):
    if l.startswith(' 34CL  G'):
        ri_prefix = l.ljust(80)[21] # index 21 = col 22
        if ri_prefix != ' ':
            print(f'Line {i+1}: col 22 violated: \'{ri_prefix}\' -> \'{l}\'')
            bad += 1
print(f'Total RI started early (col 22): {bad}')
