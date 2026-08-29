path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('lines!=80:', [(i + 1, len(x)) for i, x in enumerate(ls) if len(x) != 80][:15])
print()
print('=== top block lines 5-15 ===')
for i in range(4, 15):
    print(i + 1, 'len', len(ls[i]), '|', ls[i].rstrip())
print()
# re-scan for residual isotope/unit issues in top block
import re
print('=== residual isotope tokens (top 30 lines) ===')
for i, x in enumerate(ls[:30]):
    if re.search(r'(?<!\{\+)\b\d{1,3}[A-Z][a-z]?\b', x):
        print(' ', i + 1, repr(x.rstrip()))
print('=== residual unit cm2 ===')
for i, x in enumerate(ls[:30]):
    if 'cm2' in x or 'cm{+2}' not in x:
        pass
    if re.search(r'(?<!\{)cm2\b', x):
        print(' ', i + 1, repr(x.rstrip()))
