"""List G-records whose RI is documented as coming from {+31}P(|a,p|g) together
with their current column-77 flag, and print the exact line content so the flag
can be set.

Usage: python m_targets.py FILE
"""
import sys

raw = open(sys.argv[1], 'r', encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
lines = raw.split('\n')

recs = [(i, ln) for i, ln in enumerate(lines)
        if len(ln) > 7 and ln[6] == ' ' and ln[7] == 'G']
coms = [(i, ln) for i, ln in enumerate(lines)
        if len(ln) > 7 and ln[6] != ' ' and ln[7] == 'G']


def body(idx):
    txt = []
    for j, cl in coms:
        if j < idx:
            continue
        if any(idx < k < j for k, _ in recs):
            break
        txt.append(cl[8:].strip())
    return ' '.join(txt)


need, have = [], []
for idx, ln in recs:
    b = body(idx)
    flag = ln[76] if len(ln) > 76 else ' '
    if 'RI' in b and '{+31}P(|a,p|g)' in b:
        (have if flag == 'M' else need).append((idx + 1, flag, ln, b))

print('G-records with 31P-sourced RI and flag M   : %d' % len(have))
print('G-records with 31P-sourced RI and NO flag M: %d' % len(need))
print()
for ln_no, flag, ln, b in need:
    core = ln.rstrip()
    print('### line %d  flag=%r  len=%d  core_len=%d  spaces_to_col76=%d'
          % (ln_no, flag, len(ln), len(core), 76 - len(core)))
    print('CONTENT %s' % core)
print()
print('--- already M ---')
for ln_no, flag, ln, b in have:
    print('%6d | %s' % (ln_no, ln.rstrip()))
