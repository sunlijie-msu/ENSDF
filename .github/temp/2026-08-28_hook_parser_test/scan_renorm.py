path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# parse: group G records by preceding L record
levels = []  # (lineno_0based, level_energy, list of (g_energy, ri_str, ri_val, gline_index))
cur = None
for i, x in enumerate(ls):
    if x.startswith(' 34S   L '):
        e = x[9:19].strip()
        cur = (i, e, [])
        levels.append(cur)
    elif x.startswith(' 34S   G ') and cur is not None:
        g = x[9:19].strip()
        ri_raw = x[22:29].strip()
        ri_val = None
        if ri_raw and ri_raw.replace('.','').isdigit():
            ri_val = float(ri_raw)
        cur[2].append((g, ri_raw, ri_val, i))

print('=== levels with gamma RI ===')
for lineno, e, gs in levels:
    ris = [(g, rv) for g, rr, rv, i in gs if rv is not None]
    if not ris:
        continue
    mx = max(rv for _, rv in ris)
    flag = '  <-- RENORM NEEDED (max>100)' if mx > 100 else ''
    print(f'L {e:8} line {lineno+1:3} | ' + ', '.join(f'{g}={rv:g}' for g, rv in ris) + f' | max={mx:g}{flag}')
