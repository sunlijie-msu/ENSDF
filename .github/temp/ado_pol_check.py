import re

# Parse 71As .ens
lines = open(r'XUNDL/2026LIAA_CV10930_71As.ens', encoding='utf-8').read().splitlines()

levels = []   # (E, Jstr)
gammas = []   # {Ei, Eg, M, ado, pol}

cur = None
for l in lines:
    if len(l) < 41:
        continue
    if l[7] == 'L' and l[5:7] == '  ':
        E = float(l[9:19].strip())
        J = l[22:39].strip()
        cur = E
        levels.append((E, J))
    elif l[7] == 'G' and l[5:7] == '  ':
        Eg = float(l[9:19].strip())
        M = l[32:41].strip()
        gammas.append({'Ei': cur, 'Eg': Eg, 'M': M, 'ado': None, 'pol': None, 'cG': None})
    elif l[6] == 'c' and l[7] == 'G' and cur is not None and gammas and gammas[-1]['cG'] is None and gammas[-1]['Ei'] == cur:
        txt = l[9:].strip()
        # only attach general comments ($ ...) per gamma
        if txt.startswith('$') and not txt.startswith('$From') and not txt.startswith('$As given'):
            gammas[-1]['cG'] = txt
            m = re.search(r'R\{-ADO\}=([\d.]+) \{I(\d+)\}', txt)
            if m:
                gammas[-1]['ado'] = float(m.group(1))
            m2 = re.search(r'POL=([+-])([\d.]+) \{I(\d+)\}', txt)
            if m2:
                gammas[-1]['pol'] = (m2.group(1), float(m2.group(2)))

# build level map
levmap = {E: J for E, J in levels}
Elist = sorted(levmap)

def parse_j(J):
    """Return (spin_value, parity) treating parentheses as uncertain but using value."""
    J = J.strip()
    if J == '':
        return None
    s = J.replace('(', '').replace(')', '')
    m = re.match(r'(\d+)/(\d+)', s)
    if not m:
        return None
    num, den = int(m.group(1)), int(m.group(2))
    parity = '+' if '+' in s else ('-' if '-' in s else None)
    return (num / den, parity)

def delj(Ji, Jf):
    """min |Ji - Jf| over spin values"""
    if Ji is None or Jf is None:
        return None
    return abs(Ji[0] - Jf[0])

def parity_change(Ji, Jf):
    if Ji is None or Jf is None:
        return None
    if Ji[1] is None or Jf[1] is None:
        return None
    return 'yes' if Ji[1] != Jf[1] else 'no'

def expected_ado(dj):
    """per rule: 1.3 for dj=2 or 0; 0.8 for dj=1"""
    if dj is None:
        return None
    if dj in (2.0, 0.0):
        return 1.3
    if dj == 1.0:
        return 0.8
    return None

def m_type(M):
    """electric/magnetic/unknown from multipolarity string"""
    if not M:
        return None
    M = M.replace('(', '').replace(')', '')
    if re.match(r'^E\d', M):
        return 'E'
    if re.match(r'^M\d', M):
        return 'M'
    # mixed like M1+E2 -> first component
    parts = re.split(r'\+', M)
    for p in parts:
        if re.match(r'^E\d', p):
            return 'E'
        if re.match(r'^M\d', p):
            return 'M'
    return None

def m_parity_change(M):
    """per selection rules: E1,M2 -> yes; M1,E2 -> no; M1+E2 no; E1+M2 yes"""
    if not M:
        return None
    M = M.replace('(', '').replace(')', '')
    if M in ('E1', 'M2', 'E1+M2', 'E2+M1'):
        return 'yes'
    if M in ('M1', 'E2', 'M1+E2', 'E2+M1', 'E1+M2'):
        return 'no' if M in ('M1', 'E2', 'M1+E2') else 'yes'
    return None

# find final level for each gamma
def find_final(Ei, Eg):
    Ef = Ei - Eg
    best, bd = None, 1e9
    for e in Elist:
        d = abs(e - Ef)
        if d < bd:
            bd, best = d, e
    if bd <= 1.0:
        return best, bd
    return None, bd

print('=== ADO / POL / MULTIPOLARITY CONSISTENCY CHECK ===')
n_ado = n_pol = n_m = 0
ado_bad = []
pol_bad = []
par_bad = []
for g in gammas:
    Ji = parse_j(levmap.get(g['Ei'], ''))
    F, res = find_final(g['Ei'], g['Eg'])
    Jf = parse_j(levmap.get(F, '')) if F is not None else None
    dj = delj(Ji, Jf)
    pc = parity_change(Ji, Jf)
    M = g['M']
    mt = m_type(M)
    # ADO check
    if g['ado'] is not None:
        n_ado += 1
        exp = expected_ado(dj)
        if exp is not None:
            # tolerance: closer to expected
            ok = (abs(g['ado'] - exp) <= 0.25)
            if not ok:
                ado_bad.append((g['Ei'], g['Eg'], M, dj, g['ado'], exp))
    # POL check
    if g['pol'] is not None:
        n_pol += 1
        sign, val = g['pol']
        if mt == 'E' and sign == '-':
            pol_bad.append((g['Ei'], g['Eg'], M, 'electric but POL negative', g['pol']))
        if mt == 'M' and sign == '+':
            pol_bad.append((g['Ei'], g['Eg'], M, 'magnetic but POL positive', g['pol']))
    # multipolarity vs parity change
    if M and pc is not None:
        n_m += 1
        mp = m_parity_change(M)
        if mp is not None and mp != pc:
            par_bad.append((g['Ei'], g['Eg'], M, 'parity change %s but %s' % (pc, M)))

print('transitions:', len(gammas))
print('with ADO:', n_ado, ' with POL:', n_pol, ' with M+Jpi:', n_m)
print()
print('ADO inconsistencies:', len(ado_bad))
for b in ado_bad:
    print('  Ei=%s Eg=%s M=%s dJ=%s R=%.2f exp=%.1f' % b)
print()
print('POL inconsistencies (%d):' % len(pol_bad))
for b in pol_bad:
    print('  Ei=%s Eg=%s M=%s %s pol=%s%.2f' % (b[0], b[1], b[2], b[3], b[4], b[5]))
print()
print('Multipolarity-vs-parity inconsistencies:', len(par_bad))
for b in par_bad:
    print('  Ei=%s Eg=%s M=%s %s' % b)
