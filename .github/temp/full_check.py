import re

lines = open(r'XUNDL/2026LIAA_CV10930_71As.ens', encoding='utf-8').read().splitlines()
levels = []
gammas = []
cur = None
for l in lines:
    if len(l) < 41:
        continue
    if l[7] == 'L' and l[5:7] == '  ':
        E = float(l[9:19].strip())
        cur = E
        levels.append((E, l[22:39].strip()))
    elif l[7] == 'G' and l[5:7] == '  ':
        gammas.append({'Ei': cur, 'Eg': float(l[9:19].strip()), 'M': l[32:41].strip(), 'ado': None, 'pol': None, 'done': False})
    elif l[6] == 'c' and l[7] == 'G':
        txt = l[9:].strip()
        if gammas and not gammas[-1]['done'] and ('R{-ADO}' in txt or 'POL=' in txt):
            if 'R{-ADO}' in txt:
                m = re.search(r'R\{-ADO\}=([\d.]+) \{I(\d+)\}', txt)
                if m:
                    gammas[-1]['ado'] = float(m.group(1))
            if 'POL=' in txt:
                m2 = re.search(r'POL=([+-])([\d.]+) \{I(\d+)\}', txt)
                if m2:
                    gammas[-1]['pol'] = (m2.group(1), float(m2.group(2)))
            # a cG line may contain both; mark done only when this is a per-gamma general comment
            if txt.startswith('$') and not txt.startswith('$From') and not txt.startswith('$As'):
                gammas[-1]['done'] = True

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

def m_type(M):
    if not M:
        return None
    Mx = M.replace('(', '').replace(')', '')
    for p in re.split(r'\+', Mx):
        if re.match(r'^E\d', p):
            return 'E'
        if re.match(r'^M\d', p):
            return 'M'
    return None

print('=== FULL CHECK ===')
print('%-4s %-8s %-8s %-10s %-6s %-7s %-8s %-6s %s' % ('g#','Ei','Eg','M','dJ','ADO','POL','type','verdict'))
for i, g in enumerate(gammas, 1):
    Ji = parse_j(levmap.get(g['Ei'], ''))
    F, res = find_final(g['Ei'], g['Eg'])
    Jf = parse_j(levmap.get(F, '')) if F is not None else None
    dj = abs(Ji[0] - Jf[0]) if Ji and Jf else None
    M = g['M']
    mt = m_type(M)
    exp = 1.3 if dj in (2.0, 0.0) else (0.8 if dj == 1.0 else None)
    verdicts = []
    if g['ado'] is not None and exp is not None:
        if abs(g['ado'] - exp) > 0.25:
            verdicts.append('ADO?')
    if g['pol'] is not None and mt:
        sign = g['pol'][0]
        if mt == 'E' and sign == '-':
            verdicts.append('POL?')
        if mt == 'M' and sign == '+':
            verdicts.append('POL?')
    verdict = ','.join(verdicts) if verdicts else 'OK'
    pols = ('%s%.2f' % g['pol']) if g['pol'] else '-'
    ados = ('%.2f' % g['ado']) if g['ado'] is not None else '-'
    print('%-4d %-8s %-8s %-10s %-6s %-7s %-8s %-6s %s' % (i, g['Ei'], g['Eg'], M, str(dj), ados, pols, mt or '-', verdict))
