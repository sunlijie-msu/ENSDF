# Analyze cL comment ordering per level block + find strength comments missing units.
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(path, encoding='utf-8', newline='').read().split('\r\n')

# identifier rank: E$=0, J$=1, T$=2, S$=3, general($...)=4
def rank(t):
    # t = text after 'cL ' (col 10+)
    if t.startswith('E$'): return 0, 'E$'
    if t.startswith('J$'): return 1, 'J$'
    if t.startswith('T$'): return 2, 'T$'
    if t.startswith('S$'): return 3, 'S$'
    if t.startswith('$'):  return 4, 'general'
    return 5, '?' + t[:4]

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '
def is_cL(ln): return len(ln) >= 9 and ln[6:9] == 'cL '

i = 0
print('=== cL ordering per level ===')
while i < len(lines):
    ln = lines[i]
    if is_L(ln):
        e = ln[9:19].strip()
        j = i + 1
        blk = []
        while j < len(lines) and len(lines[j]) >= 9 and lines[j][6:9] == 'cL ':
            t = lines[j][9:]
            blk.append((j + 1, lines[j][6], t))  # (lineno, cont char, text)
            j += 1
        if blk:
            seq = [rank(t) for _, _, t in blk]
            # check ordering violation: any earlier rank > later rank
            viol = []
            for a in range(len(seq)):
                for b in range(a + 1, len(seq)):
                    if seq[a][0] > seq[b][0]:
                        viol.append((seq[a][1], seq[b][1]))
            print(f'L {e}: n={len(blk)}')
            for (lnno, cont, t) in blk:
                r, rname = rank(t)
                print(f'   {lnno} {cont}cL {rname:8s} {t[:60]}')
            if viol:
                print(f'   *** ORDER VIOLATION: {viol}')
        i = j
        continue
    i += 1

print()
print('=== Va08 strength comments missing eV ===')
for i, ln in enumerate(lines):
    if '|G{-|g}|G{-|a}/|G=' in ln and ' eV ' not in ln and '(1964Va08)' in ln:
        print(f'   line {i+1}: {ln.strip()}')
