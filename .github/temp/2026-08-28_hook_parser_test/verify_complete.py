# COMPREHENSIVE cross-check: every .ens level with S field vs all three source tables.
# Parses raw markdown tables directly. Reports EVERY mismatch.
import re, os

BASE = r'd:\X\ND\ENSDF\A34\S34'
ENS = os.path.join(BASE, 'new', 'S34_30si_a_g_a_n_resonances.ens')
VA08 = os.path.join(BASE, 'raw', '1964VA08_Table_1.md')
MC07 = os.path.join(BASE, 'raw', '1965MC07_Table_1.md')
WI01 = os.path.join(BASE, 'raw', '1967WI01_Table_1.md')

def num(v):
    # extract leading number from e.g. '2276(5)' or '3.892'
    m = re.match(r'([-+]?[\d.]+)', v.strip())
    return m.group(1) if m else None

def is_resnum(s):
    # markdown bold like '**1**'
    return s.replace('*', '').strip().isdigit()

# ---- parse Va08: col2 = E_alpha keV ----
va08 = {}  # E_alpha_keV -> res#
for ln in open(VA08, encoding='utf-8'):
    if not ln.startswith('|') or ln.strip().startswith('| :'):
        continue
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if len(c) >= 4 and is_resnum(c[0]):
        e = num(c[2])
        if e: va08[int(e)] = int(c[0].replace('*', ''))

# ---- parse Mc07: col3 = E_alpha keV ----
mc07 = {}  # E_alpha_keV -> res#
for ln in open(MC07, encoding='utf-8'):
    if not ln.startswith('|') or ln.strip().startswith('| :'):
        continue
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if len(c) >= 5 and is_resnum(c[0]):
        e = num(c[3])
        if e: mc07[int(e)] = int(c[0].replace('*', ''))

# ---- parse Wi01: field0=res, field1=prev, field2=Ea MeV ----
wi01 = {}   # E_alpha_keV -> (res#, prev_res_or_None)
for ln in open(WI01, encoding='utf-8'):
    if not ln.strip() or ln.startswith('Resonance'):
        continue
    f = ln.strip().split(',')
    if len(f) < 3 or not f[0].strip().isdigit():
        continue
    res = int(f[0].strip())
    prev = f[1].strip()
    prev = int(prev) if prev.isdigit() else None
    mev = f[2].strip()
    ekev = int(round(float(mev) * 1000)) if mev else None
    wi01[ekev] = (res, prev)

# Build level->classification by scanning ens file
errors = []
checked = 0
lines = open(ENS, encoding='utf-8', newline='').read().split('\r\n')

levels = []
i = 0
while i < len(lines):
    ln = lines[i]
    if len(ln) >= 20 and ln[5:9] == '  L ':
        e = ln[9:19].strip()
        s = ln[64:74].strip()
        flag = ln[76] if len(ln) >= 77 else ' '
        soth = None
        j = i + 1
        while j < len(lines) and len(lines[j]) >= 9 and lines[j][6:9] == 'cL ':
            t = lines[j][9:]
            m = re.search(r'S\$other:\s*(\d+)\s*\{I\d+\}', t)
            if m: soth = int(m.group(1))
            j += 1
        levels.append({'e': e, 's': s, 'flag': flag, 'soth': soth})
        i = j
    else:
        i += 1

for lv in levels:
    if not lv['s']:
        continue  # no S field
    checked += 1
    e, s, flag, soth = lv['e'], int(lv['s']), lv['flag'], lv['soth']
    exp_flag = None
    exp_soth = None
    src = None

    # special: average case
    if e == '10791':
        exp_flag = None
        exp_soth = None
        src = 'AVG (Va08+Mc07)'
        # check S$Average comment present
        # (checked separately)
    elif s in wi01:
        res, prev = wi01[s]
        if prev is not None:
            exp_soth = [k for k, v in mc07.items() if v == prev]
            exp_soth = exp_soth[0] if exp_soth else None
            src = f'Wi01+Mc07 (Wi01 res {res} = Mc07 res {prev})'
            if s != [k for k in wi01 if wi01[k][0] == res][0]:
                pass
        else:
            src = f'Wi01-only (res {res})'
    elif s in va08 and s not in mc07:
        exp_flag = 'V'
        src = f'Va08-only (res {va08[s]})'
    elif s in mc07:
        exp_flag = 'M'
        src = f'Mc07-only (res {mc07[s]})'
    else:
        errors.append(f'line? E={e} S={s}: S matches NO source!')
        continue

    # checks
    if e != '10791' and s in wi01 and wi01[s][1] is not None:
        # Wi01+Mc07: flag must be blank (no V/M), S$other must equal exp
        if flag not in (' ', 'N', 'G'):
            errors.append(f'E={e} S={s} [{src}]: unexpected col77 flag {flag!r}')
        if soth != exp_soth:
            errors.append(f'E={e} S={s} [{src}]: S$other={soth} expected {exp_soth}')
    elif e == '10791':
        if flag != ' ':
            errors.append(f'E={e} [{src}]: unexpected col77 flag {flag!r}')
    else:
        # Wi01-only / Va08-only / Mc07-only
        if exp_flag and flag != exp_flag:
            errors.append(f'E={e} S={s} [{src}]: col77 flag={flag!r} expected {exp_flag!r}')
        if exp_flag is None and flag not in (' ', 'N', 'G'):
            errors.append(f'E={e} S={s} [{src}]: unexpected col77 flag {flag!r}')
        if soth is not None:
            errors.append(f'E={e} S={s} [{src}]: S$other={soth} should be ABSENT')

print(f'Levels with S checked: {checked}')
print(f'ERRORS: {len(errors)}')
for er in errors:
    print('  ', er)

# summary of S$other coverage
soth_levels = [lv for lv in levels if lv['soth']]
print(f'\nLevels WITH S$other comment: {len(soth_levels)}')
for lv in soth_levels:
    print(f"   E={lv['e']} S={lv['s']} S$other={lv['soth']} flag={lv['flag']!r}")
