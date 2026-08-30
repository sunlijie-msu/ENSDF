path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

def pad(s):
    return s + ' ' * (80 - len(s))

# 1) general comment insertion before L$ line
# build 3 E$ flag-definition comments
gen_comments = [
    pad(' 34S  cL E(B)$From 1963Br05.'),
    pad(' 34S  cL E(C)$From 1972Cr08.'),
    pad(' 34S  cL E(V)$From 1971Va21. Energy values from 1973EnVA.'),
]
for c in gen_comments:
    print('GEN:', repr(c))
# find L$ general line
lidx = None
for i, x in enumerate(ls):
    if x.startswith(' 34S  cL L$From 1972Cr08, unless otherwise noted.'):
        lidx = i
        break
print('L$ line at', lidx + 1, 'prev:', repr(ls[lidx-1]))
prev = ls[lidx-1]
assert prev.startswith(' 34S 2c  Deduced Q values')
ins_old = prev + '\n' + ls[lidx]
ins_new = prev + '\n' + '\n'.join(gen_comments) + '\n' + ls[lidx]
print('insert old unique:', t.count(ins_old) == 1)

# 2) remove redundant E$ comments per level
remove = {
    'B': ['2122', '4702', '4888', '8299', '8622'],
    'C': ['5326', '5683', '5694', '5758', '6422', '6832', '7547', '7659', '7732', '8142'],
    'V': ['3915', '4072', '4688', '4874', '5225', '5859', '6008', '6533'],
}
red_patterns = [
    'cL E$from 1963Br05',
    'cL E$from 1972Cr08',
    'cL E$level measured by 1971Va21 (energy value from 1973EnVA)',
]
repls = []
for fl, ens in remove.items():
    for en in ens:
        li = None
        for i, x in enumerate(ls):
            if x.startswith(' 34S   L ' + en + ' '):
                li = i
                break
        if li is None:
            print(f'L {en}: NOT FOUND')
            continue
        # next line is the E$ comment?
        nxt = ls[li+1]
        matched = None
        for pat in red_patterns:
            if pat in nxt and nxt.startswith(' 34S  cL '):
                matched = pat
                break
        if matched is None:
            print(f'L {en}: no redundant E$ comment (next={nxt[:40]!r})')
            continue
        old = ls[li] + '\n' + nxt
        new = ls[li]
        repls.append((en, fl, li, old, new, nxt.rstrip()[:50]))
        print(f'L {en} ({fl}): remove [{nxt.rstrip()[:45]}]')

print()
print('removals:', len(repls))
for en, fl, li, old, new, c in repls:
    assert t.count(old) == 1, f'L {en} old not unique'
print('all unique OK')

# write old/new to file for reference
with open(r'd:\X\ND\ENSDF\.github\temp\2026-08-28_hook_parser_test\bcv_repls.txt', 'w', encoding='utf-8') as f:
    f.write('INSERT\n')
    f.write(repr(ins_old) + '\n')
    f.write(repr(ins_new) + '\n')
    f.write('REMOVE\n')
    for en, fl, li, old, new, c in repls:
        f.write(repr(old) + '\n')
        f.write(repr(new) + '\n')
print('written to bcv_repls.txt')
