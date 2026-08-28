# Show exact reprs of boundary lines in target region + new lines to insert
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()

# Find lines containing key level energies
for i, ln in enumerate(lines):
    if any(k in ln for k in ['L 10316', 'G 10314', 'L 10385', 'E(|a)(lab)=2790',
                              'L 10407', 'G 10405', 'L 10447', 'E(|a)(lab)=2860',
                              'L 10493']):
        print(i + 1, repr(ln), len(ln))
