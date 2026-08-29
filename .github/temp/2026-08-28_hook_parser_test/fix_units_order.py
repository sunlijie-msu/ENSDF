# Fix 1: add 'eV' unit to Va08 strength comments (missing unit).
# Fix 2: reorder cL blocks to E$ -> J$ -> T$ -> S$ -> general (stable), keeping 2cL/3cL attached.
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(path, encoding='utf-8', newline='').read().split('\r\n')

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '
def is_cL(ln): return len(ln) >= 9 and ln[6:9] == 'cL '
def is_cont_cL(ln): return len(ln) >= 9 and ln[6:9] == 'cL ' and ln[5] != ' '

def rank(t):
    ident = t.split('$', 1)[0]           # e.g. 'J,T', 'S', 'E', or ''
    if not ident:
        return 4
    first = ident.split(',')[0].strip()
    order = {'E': 0, 'J': 1, 'T': 2, 'S': 3}
    if first in order:
        return order[first]
    return 5

# ---------- Fix 1: add eV to Va08 strength comments ----------
unit_fixed = []
for i, ln in enumerate(lines):
    if '|G{-|g}|G{-|a}/|G=' in ln and ' eV ' not in ln and '(1964Va08)' in ln:
        # insert ' eV' between value and '(1964Va08)'
        m = re.search(r'(\|G\{-\|a\}/\|G=)([^()]*)\(\(1964Va08\)\)', ln)
        # simpler: replace ') (1964Va08)' pattern? value like '0.14 ' then '(1964Va08)'
        new = re.sub(r'(=\S+\s)\(1964Va08\)', r'\1eV (1964Va08)', ln)
        if new == ln:
            # handle =0.14 (1964Va08) with single space
            new = re.sub(r'(=\S+) \(1964Va08\)', r'\1 eV (1964Va08)', ln)
        assert new != ln, f'no unit add at line {i+1}: {ln!r}'
        lines[i] = new
        unit_fixed.append((i + 1, ln.strip(), new.strip()))

# ---------- Fix 2: reorder cL blocks ----------
def collect_block(lines, i):
    """collect (unit, [lineno...]) list for level block starting after L at i."""
    j = i + 1
    units = []          # list of dicts {rank, lines:[str], lineno:int}
    cur = None
    while j < len(lines) and len(lines[j]) >= 9 and lines[j][6:9] == 'cL ':
        if lines[j][5] == ' ':   # new cL line (col6 blank)
            if cur: units.append(cur)
            cur = {'rank': None, 'lines': [lines[j]], 'lineno': j + 1}
        else:                    # continuation 2cL/3cL
            cur['lines'].append(lines[j])
        j += 1
    if cur: units.append(cur)
    for u in units:
        u['rank'] = rank(u['lines'][0][9:])
    return units, j

reordered = []
i = 0
while i < len(lines):
    if is_L(lines[i]):
        units, j = collect_block(lines, i)
        if len(units) > 1:
            # check if already ordered
            rseq = [u['rank'] for u in units]
            ordered = all(rseq[a] <= rseq[b] for a in range(len(rseq)) for b in range(a + 1, len(rseq)))
            if not ordered:
                # stable sort by rank
                units_sorted = sorted(units, key=lambda u: u['rank'])
                newlines = [ln for u in units_sorted for ln in u['lines']]
                # replace in lines
                lines[i + 1:j] = newlines
                reordered.append((i + 1, [u['lineno'] for u in units]))
                i = i + 1 + len(newlines)
                continue
        i = j
        continue
    i += 1

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(lines))

print(f'Units added: {len(unit_fixed)}')
for n, old, new in unit_fixed:
    print(f'   line {n}: {old}  ->  {new}')
print()
print(f'Blocks reordered: {len(reordered)}')
for start, lnos in reordered:
    print(f'   level-line {start}: {lnos}')
