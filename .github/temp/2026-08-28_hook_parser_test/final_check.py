path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), '| lines:', len(ls), '| LF-only(should be 0):', b.count(b'\n') - b.count(b'\r\n'))
print('nonascii chars:', sum(1 for x in b if x > 127))
print('lines != 80:', [(i + 1, len(x)) for i, x in enumerate(ls) if len(x) != 80])
print('over80:', [(i + 1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
# check all 5 intensity blocks structure
print()
ok = 0
for i, x in enumerate(ls):
    if 'intensities = ' in x and 'from this resonance to' in x:
        nxt = ls[i + 1]
        good = len(x) == 80 and '{+34}S levels higher than 3304 keV.' in nxt and len(nxt) == 80
        ok += good
        print(i + 1, 'cL ok' if good else 'cL BAD', '|', x.rstrip()[:60], '| 2cL:', nxt.rstrip()[:40])
print('intensity blocks correct:', ok, '/ 5')
# check no '=  ' (double space) or '=NNNN' (missing space after = for word context)
import re
print()
print('word`=`missing-space (rule2 violation, Intensity=0.45):')
for i, x in enumerate(ls):
    for m in re.finditer(r'[A-Za-z]{2,}=[0-9]', x):
        print(' ', i + 1, repr(x.rstrip()))
