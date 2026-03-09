lines = open('A34/Cl34/raw/1977DA02_1983WA27.adp').read().splitlines()
bad = 0
for i, l in enumerate(lines):
    if l.startswith(' 34CL  G'):
        dri = l.ljust(80)[29:31]
        if len(dri.strip()) > 0 and dri[0] == ' ':
            print(f'Line {i+1}: right-justified DRI: \'{dri}\' -> \'{l}\'')
            bad += 1
print(f'Total bad right-justified DRI: {bad}')
