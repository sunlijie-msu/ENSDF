# Robust line-ending-agnostic check: missing units + cL ordering violations.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read()
lines = t.replace('\r\n', '\n').replace('\r', '\n').split('\n')

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '
def is_cL(ln): return len(ln) >= 9 and ln[6:9] == 'cL '
def rank(t):
    ident = t.split('$', 1)[0]
    if not ident: return 4
    first = ident.split(',')[0].strip()
    return {'E': 0, 'J': 1, 'T': 2, 'S': 3}.get(first, 5)

missing_units = [i + 1 for i, ln in enumerate(lines)
                 if '|G{-|g}|G{-|a}/|G=' in ln and ' eV ' not in ln and '(1964Va08)' in ln]
print('Va08 strength lines MISSING eV:', len(missing_units), missing_units)

i = 0
viol = []
while i < len(lines):
    if is_L(lines[i]):
        j = i + 1
        units = []
        cur = None
        while j < len(lines) and is_cL(lines[j]):
            if lines[j][5] == ' ':
                if cur: units.append(cur)
                cur = [lines[j]]
            else:
                cur.append(lines[j])
            j += 1
        if cur: units.append(cur)
        rseq = [rank(u[0][9:]) for u in units]
        if any(rseq[a] > rseq[b] for a in range(len(rseq)) for b in range(a + 1, len(rseq))):
            e = lines[i][9:19].strip()
            viol.append((i + 1, e, [ (u[0][9:].split('$')[0] or 'general') for u in units ]))
        i = j
        continue
    i += 1

print('Ordering violations:', len(viol))
for start, e, ids in viol:
    print(f'   L{e} line {start}: {ids}')
