# Post-transformation double check:
#  1) each expected L record has the right col-77 flag
#  2) zero F L FLAG lines remain
#  3) all data lines are exactly 80 chars
#  4) the four 1975DeZS levels still carry col-77 'D'
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(path, encoding='utf-8').read().splitlines()

expected = {  # E(level): flag letter
    '2127.564': 'A', '3304.212': 'A',
    '11357': 'B', '11371': 'B', '11380': 'B', '11398': 'B', '11405': 'B',
    '11419': 'B', '11457': 'B', '11849': 'B', '11866': 'B',
    '11434': 'C', '11636': 'C', '11669': 'C', '11751': 'C', '12136': 'C', '12150': 'C',
    '11444': 'D', '11921': 'D',
}
new4 = {'10382': 'D', '10386': 'D', '10443': 'D', '10482': 'D'}

found = {}
bad_len = []
flag_lines = 0
for i, ln in enumerate(lines):
    if len(ln) != 80 and not (ln.strip() == '' and i == len(lines) - 1):
        bad_len.append((i + 1, len(ln)))
    if ln.startswith(' 34S F L FLAG='):
        flag_lines += 1
    if len(ln) >= 77 and ln[5:9] == '  L ':
        e = ln[9:19].strip()
        found[e] = ln[76]

print('1) col-77 flags on expected L records:')
ok = True
for e, flag in expected.items():
    got = found.get(e)
    status = 'OK' if got == flag else f'MISMATCH (got {got!r})'
    if got != flag:
        ok = False
    print(f'   E={e:>10}  expected={flag}  got={got!r}  {status}')

print('2) F L FLAG lines remaining:', flag_lines)
print('3) non-80 lines:', bad_len if bad_len else 'none')
print('4) 1975DeZS levels still col77 D:')
for e, flag in new4.items():
    got = found.get(e)
    status = 'OK' if got == flag else f'LOST (got {got!r})'
    if got != flag:
        ok = False
    print(f'   E={e:>6}  expected={flag}  got={got!r}  {status}')

print()
print('OVERALL:', 'PASS' if (ok and flag_lines == 0 and not bad_len) else 'FAIL')
