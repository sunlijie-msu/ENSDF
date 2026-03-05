import re

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'r') as f:
    content = f.read()

missing_ep = [1158, 1448, 1477, 1706, 1752]
map_eps = {
    1158: ('0.4', '2'),
    1448: ('1.4', '4'),
    1477: ('0.7', '3'),
    1706: ('4.8', '10'),
    1752: ('4.7', '20'),
}

print('Checking for |w|g values for missing E(p) values:')
print()

for ep in missing_ep:
    wg_val, unc = map_eps[ep]
    found_count = len(re.findall(re.escape(f'|w|g={wg_val}') + f' {{I{unc}}}' + ' \\(1983Wa27\\)', content))
    if found_count > 0:
        print(f'E(p)={ep}: |w|g={wg_val} - FOUND ({found_count} occurrence)')
    else:
        print(f'E(p)={ep}: |w|g={wg_val} - NOT FOUND')
