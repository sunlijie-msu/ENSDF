import csv
import re
from pathlib import Path

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Unbound.csv')
adopted_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens')
reaction_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens')


def parse_levels(path):
    levels = []
    for line in path.read_text(encoding='ascii').splitlines():
        if len(line) >= 19 and line[5:8] == '  L':
            energy = line[9:19].strip()
            if not energy:
                continue
            try:
                value = float(energy)
            except ValueError:
                continue
            levels.append((energy, value))
    out = []
    seen = set()
    for e, v in levels:
        if e not in seen:
            seen.add(e)
            out.append((e, v))
    return out

adopted = parse_levels(adopted_path)
reaction = parse_levels(reaction_path)
rows = list(csv.reader(csv_path.open(newline='')))

rounded_ei = [row[1] for row in rows[2:]]

print('Resolved Ei mapping:')
resolved = {}
for ei in rounded_ei:
    t = float(ei)
    a = [e for e,v in adopted if abs(v - t) < 1.1]
    r = [e for e,v in reaction if abs(v - t) < 1.6]
    chosen = None
    source = None
    if len(a) == 1:
        chosen = a[0]
        source = 'adopted'
    elif len(a) == 0 and len(r) == 1:
        chosen = r[0]
        source = 'reaction'
    elif len(a) == 0 and len(r) > 1:
        # choose nearest by absolute delta
        best = min(((abs(v - t), e) for e,v in reaction if abs(v - t) < 1.6), key=lambda x: x[0])
        chosen = best[1]
        source = 'reaction-nearest'
    elif len(a) > 1:
        best = min(((abs(v - t), e) for e,v in adopted if abs(v - t) < 1.1), key=lambda x: x[0])
        chosen = best[1]
        source = 'adopted-nearest'
    elif len(a) == 0 and len(r) == 0:
        source = 'NONE'
    resolved[ei] = chosen
    print(f'{ei:>4} -> {chosen} [{source}] | adopted={a[:5]} reaction={r[:5]}')

print('\nToken mapping for Other Ef:')
# combine adopted+reaction+raw bound values
bound_precise = {
    '2.18':'2181.10','2.38':'2375.7','2.58':'2580.4','2.61':'2611.05','2.72':'2721.1',
    '3.13':'3129.13','3.33':'3334.0','3.38':'3383.3','3.55':'3545.07','3.60':'3600.27',
    '3.63':'3631.8','3.65':'3646.3','3.66':'3660.0','3.77':'3773.84','3.79':'3791.7',
    '3.94':'3940.1','3.96':'3964.1','3.98':'3983.5','4.08':'4076.3','4.14':'4139.8',
    '4.15':'4147.8','4.33':'4325.91','4.35':'4354.3','4.42':'4417.4','4.45':'4446.6',
    '4.46':'4461.4','4.52':'4515.8','4.64':'4638.9','4.70':'4695.7','4.72':'4717.4',
    '4.82':'4824.5','4.94':'4941.9','4.96':'4957.3','5.00':'4995.6','5.17':'5171.6',
    '5.39':'5386.8','5.54':'5540.8'
}
# special ambiguous/high-energy tokens from reaction levels
reaction_special = {}
for token in ['4.606','4.610','4.61','13.80']:
    t = float(token)
    matches = [(e,v) for e,v in reaction if abs(v/1000.0 - t) < 0.006]
    reaction_special[token] = [e for e,v in matches]
    print(token, '->', reaction_special[token])
