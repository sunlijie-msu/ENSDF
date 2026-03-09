lines = open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp', encoding='utf-8').readlines()
print(f'adp total lines: {len(lines)}')
marker = 'cG RI$from'
hits = [(i+1, l.rstrip()) for i,l in enumerate(lines) if marker in l]
print(f'cG RI$from lines: {len(hits)}')
for ln, txt in hits:
    print(f'  L{ln}: {txt}')
