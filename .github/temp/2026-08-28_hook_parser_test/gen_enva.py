path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# current -> new integer energy (rounded), DE blank
changes = {
    '3914.1': '3914',
    '4072.4': '4072',
    '4687.5': '4688',
    '4875.1': '4875',
    '5227':   '5227',
    '5848':   '5848',
    '5993':   '5993',
    '6533':   '6533',
}

repls = []
for i, x in enumerate(ls):
    if not x.startswith(' 34S   L '):
        continue
    e = x[9:19].strip()
    if e in changes:
        old = x
        new_e = changes[e]
        if len(x) != 80:
            print(f'level {e}: line len {len(x)} != 80')
            continue
        # E field cols 10-19, DE cols 20-21 blank, col22 space, rest unchanged
        newline = x[:9] + new_e.ljust(10) + '  ' + x[21:]
        if len(newline) != 80:
            print(f'level {e}: newline len {len(newline)}')
            continue
        # verify old DE present
        de = x[19:21].strip()
        print(f'level {e}: DE={de!r} -> blank; new E={new_e}')
        repls.append((e, old, newline))
        print('  OLD:', repr(old))
        print('  NEW:', repr(newline))

print()
print('total replacements:', len(repls))
# verify uniqueness
for e, old, newline in repls:
    print(f'  {e}: old unique = {t.count(old) == 1}')
