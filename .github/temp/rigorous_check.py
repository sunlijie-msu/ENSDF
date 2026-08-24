import csv, re

rows = list(csv.DictReader(open(r'XUNDL/2026LIAA_CV10930_71As_Table_I.csv', encoding='utf-8-sig')))
def norm(s):
    return (s or '').replace('\u2212', '-').strip()

lines = open(r'XUNDL/2026LIAA_CV10930_71As.ens', encoding='utf-8').read().splitlines()
levels = []
gammas = []
cur = None
for l in lines:
    if len(l) < 41:
        continue
    if l[7] == 'L' and l[5:7] == '  ':
        cur = float(l[9:19].strip())
        levels.append((cur, l[22:39].strip()))
    elif l[7] == 'G' and l[5:7] == '  ':
        gammas.append({'Ei': cur, 'Eg': float(l[9:19].strip()), 'M': l[32:41].strip(), 'ado': None, 'adu': None, 'pol': None})
    elif l[6] == 'c' and l[7] == 'G':
        txt = l[9:].strip()
        if gammas:
            m = re.search(r'R\{-ADO\}=([\d.]+) \{I(\d+)\}', txt)
            if m and gammas[-1]['ado'] is None:
                gammas[-1]['ado'] = float(m.group(1))
                dec = len(m.group(1).split('.')[1]) if '.' in m.group(1) else 0
                gammas[-1]['adu'] = float(m.group(2)) * (10 ** -dec)
            m2 = re.search(r'POL=([+-])([\d.]+) \{I(\d+)\}', txt)
            if m2 and gammas[-1]['pol'] is None:
                gammas[-1]['pol'] = (m2.group(1), float(m2.group(2)))

levmap = {E: J for E, J in levels}
Elist = sorted(levmap)

def parse_j(J):
    J = J.strip()
    if not J:
        return None
    s = J.replace('(', '').replace(')', '')
    m = re.match(r'(\d+)/(\d+)', s)
    if not m:
        return None
    parity = '+' if '+' in s else ('-' if '-' in s else None)
    return (int(m.group(1)) / int(m.group(2)), parity)

def find_final(Ei, Eg):
    Ef = Ei - Eg
    best, bd = None, 1e9
    for e in Elist:
        d = abs(e - Ef)
        if d < bd:
            bd, best = d, e
    return (best, bd) if bd <= 1.0 else (None, bd)

print('=== ADO CHECK (>2 sigma) ===')
n = 0
for i, g in enumerate(gammas, 1):
    if g['ado'] is None:
        continue
    Ji = parse_j(levmap.get(g['Ei'], ''))
    F, _ = find_final(g['Ei'], g['Eg'])
    Jf = parse_j(levmap.get(F, '')) if F is not None else None
    dj = abs(Ji[0] - Jf[0]) if Ji and Jf else None
    exp = 1.3 if dj in (2.0, 0.0) else (0.8 if dj == 1.0 else None)
    if exp is None:
        continue
    diff = abs(g['ado'] - exp)
    unc = g['adu'] or 0.1
    if diff > 2 * unc:
        n += 1
        print('g#%d Ei=%s Eg=%s M=%s dJ=%s ADO=%.2f(%.2f) exp=%.1f diff=%.2f nsig=%.1f' % (i, g['Ei'], g['Eg'], g['M'], dj, g['ado'], g['adu'], exp, diff, diff / unc))
print('total ADO >2sigma:', n)

print()
print('=== POL CHECK ===')
np_ = 0
for i, g in enumerate(gammas, 1):
    if g['pol'] is None or not g['M']:
        continue
    sign, val = g['pol']
    Mx = g['M'].replace('(', '').replace(')', '')
    typ = None
    if re.match(r'^E\d', Mx):
        typ = 'E'
    elif re.match(r'^M\d', Mx):
        typ = 'M'
    if typ == 'E' and sign == '-':
        np_ += 1
        print('g#%d Ei=%s Eg=%s M=%s electric but POL %s%.2f' % (i, g['Ei'], g['Eg'], g['M'], sign, val))
    if typ == 'M' and sign == '+':
        np_ += 1
        print('g#%d Ei=%s Eg=%s M=%s magnetic but POL %s%.2f' % (i, g['Ei'], g['Eg'], g['M'], sign, val))
print('total POL issues:', np_)

print()
print('=== PARITY CHECK ===')
npar = 0
for i, g in enumerate(gammas, 1):
    if not g['M']:
        continue
    Ji = parse_j(levmap.get(g['Ei'], ''))
    F, _ = find_final(g['Ei'], g['Eg'])
    Jf = parse_j(levmap.get(F, '')) if F is not None else None
    if not Ji or not Jf or Ji[1] is None or Jf[1] is None:
        continue
    actual = 'yes' if Ji[1] != Jf[1] else 'no'
    Mx = g['M'].replace('(', '').replace(')', '')
    if 'E1' in Mx and 'E2' not in Mx and 'M1' not in Mx:
        req = 'yes'
    elif 'M2' in Mx and 'M1' not in Mx and 'E2' not in Mx:
        req = 'yes'
    elif 'E2' in Mx or 'M1' in Mx:
        req = 'no'
    else:
        continue
    if req != actual:
        npar += 1
        print('g#%d Ei=%s Eg=%s M=%s parity change %s vs req %s' % (i, g['Ei'], g['Eg'], g['M'], actual, req))
print('total parity issues:', npar)
