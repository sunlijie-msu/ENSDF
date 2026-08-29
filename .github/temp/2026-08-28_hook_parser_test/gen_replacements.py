# READ-ONLY generator: prints exact OLD/NEW strings for multi_replace_string_in_file.
# Does NOT write the .ens file (complies with diff-viewer requirement).
import re

path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n').replace('\r', '\n')
lines = t.split('\n')

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '

# ---- 1) eV additions on Va08 strength lines ----
va08_levels = ['9932','9981','10097','10169','10249','10317','10408',
               '10494','10587','10625','10670','10768','10791']
ev_edits = []
for i, ln in enumerate(lines):
    if is_L(ln) and ln[9:19].strip() in va08_levels:
        e = ln[9:19].strip()
        j = i + 1
        # find the strength cL line (may be after F L / other cL)
        while j < len(lines):
            if lines[j].startswith(' 34S  cL ') and '|G{-|g}|G{-|a}/|G=' in lines[j] and '(1964Va08)' in lines[j]:
                old = lines[j]
                # insert ' eV ' before '(1964Va08)'
                new = old.replace(' (1964Va08)', ' eV (1964Va08)', 1)
                # re-pad to 80
                new = new.rstrip().ljust(80)
                ev_edits.append((e, old, new))
                break
            if lines[j][5:9] == '  G ' or is_L(lines[j]):
                break
            j += 1

# ---- 2) block reorders ----
def rank(t):
    ident = t.split('$', 1)[0]
    if not ident: return 4
    first = ident.split(',')[0].strip()
    return {'E': 0, 'J': 1, 'T': 2, 'S': 3}.get(first, 5)

reorder_levels = ['10791','11358','11372','11381','11420','11458','11473',
                  '11490','11506','11545','11643']
reorder_edits = []
for i, ln in enumerate(lines):
    if is_L(ln) and ln[9:19].strip() in reorder_levels:
        e = ln[9:19].strip()
        j = i + 1
        # collect cL units (each unit = cL line + following 2cL/3cL)
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
        if any(rseq[a] > rseq[b] for a in range(len(rseq)) for b in range(a + 1, len(rseq))):
            old = lines[i+1:j]      # block lines only (after L)
            units_sorted = sorted(units, key=lambda u: rank(u[0][9:]))
            new = [ln2 for u in units_sorted for ln2 in u]
            reorder_edits.append((e, old, new))

# ---- print ----
print('################## eV EDITS ##################')
for e, old, new in ev_edits:
    print(f'=== L{e} ===')
    print(f'OLD|{old}|')
    print(f'NEW|{new}|')
print()
print('################## REORDER EDITS ##################')
for e, old, new in reorder_edits:
    print(f'=== L{e} ===')
    for o in old:
        print(f'OLD|{o}|')
    print('---')
    for n in new:
        print(f'NEW|{n}|')
    print()
