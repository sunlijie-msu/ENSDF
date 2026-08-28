# Enumerate all F L FLAG=X lines and their preceding (corresponding) L record.
ENS = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(ENS, encoding='utf-8').read().splitlines()

cur_l = None  # (line_no, energy, has_col77)
flags = []
for i, ln in enumerate(lines):
    if len(ln) >= 20 and ln[5:9] == '  L ':
        cur_l = (i + 1, ln[9:19].strip(), ln[76] if len(ln) >= 77 else ' ')
    elif ln.startswith(' 34S F L FLAG='):
        flag = ln.strip().split('=')[-1]
        flags.append((i + 1, flag, cur_l))
    elif ln[6:9] == 'cL ' or (len(ln) >= 8 and ln[5] == 'F'):
        # cL comments and F L records stay associated with current L
        pass
    elif ln[5:9] == '  G ' or (len(ln) >= 8 and ln[7] == 'G' and ln[5] == ' '):
        pass

print('Total F L FLAG lines:', len(flags))
from collections import Counter
print('By letter:', Counter(f[1] for f in flags))
print()
for lineno, flag, l in flags:
    col77 = l[2] if l else '?'
    print(f"line {lineno}: FLAG={flag}  -> L record at line {l[0] if l else '?'}  E={l[1] if l else '?'}  col77 currently={col77!r}")
