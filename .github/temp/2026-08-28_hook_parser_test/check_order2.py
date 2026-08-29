# READ-ONLY: check cL/cG comment ordering per level block + dump comments for review.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(path, encoding='utf-8', newline='').read().replace('\r\n','\n').split('\n')

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '
def is_cL(ln): return len(ln) >= 9 and ln[6:9] == 'cL ' and ln[5] == ' '
def is_cont(ln): return len(ln) >= 9 and ln[6:9] == 'cL ' and ln[5] != ' '

def rank(t):
    ident = t.split('$', 1)[0]
    if not ident: return 4
    first = ident.split(',')[0].strip()
    return {'E': 0, 'J': 1, 'T': 2, 'S': 3}.get(first, 5)

i = 0
violations = 0
while i < len(lines):
    if is_L(lines[i]):
        e = lines[i][9:19].strip()
        j = i + 1
        units = []
        cur = None
        while j < len(lines) and len(lines[j]) >= 9 and lines[j][6:9] == 'cL ':
            if lines[j][5] == ' ':
                if cur: units.append(cur)
                cur = [lines[j]]
            else:
                cur.append(lines[j])
            j += 1
        if cur: units.append(cur)
        rseq = [rank(u[0][9:]) for u in units]
        if any(rseq[a] > rseq[b] for a in range(len(rseq)) for b in range(a+1, len(rseq))):
            ids = [u[0][9:].split('$')[0] or 'general' for u in units]
            print(f'ORDER VIOLATION L{e}: {ids}')
            violations += 1
        i = j
        continue
    i += 1
print(f'cL ordering violations: {violations}')
