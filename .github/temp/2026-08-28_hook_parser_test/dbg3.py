path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
ls = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n').split('\n')
l213 = ls[212]
print('line213 len', len(l213), 'sp', len(l213) - len(l213.rstrip()))
print('line213 content repr:', repr(l213.rstrip()))
# try various space counts
for n in [32, 33, 34, 35, 36]:
    c = ' 34S 2cL {+34}S levels higher than 3304 keV.' + ' ' * n
    if c == l213:
        print('c2 matches at', n, 'spaces')
