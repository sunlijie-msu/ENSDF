path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

flags = {
    'B': ['2122', '4702', '4888', '7398', '8299', '8622'],
    'C': ['5326', '5683', '5694', '5758', '6128', '6422', '6832', '7547', '7659', '7732', '8142'],
    'V': ['3915', '4072', '4688', '4874', '5225', '5859', '6008', '6533'],
}

# --- flag additions ---
flag_repls = []
for fl, energies in flags.items():
    for en in energies:
        found = None
        for i, x in enumerate(ls):
            if x.startswith(' 34S   L ' + en + ' '):
                found = (i, x)
                break
        if found is None:
            print(f'FLAG {fl} L {en}: NOT FOUND')
            continue
        i, x = found
        if len(x) != 80:
            print(f'FLAG {fl} L {en}: len {len(x)}')
            continue
        if x[76] != ' ':
            print(f'FLAG {fl} L {en}: col77 occupied {x[76]!r}')
            continue
        new = x[:76] + fl + x[77:]
        flag_repls.append((fl, en, i, x, new))
        print(f'FLAG {fl} L {en:5} line {i+1}: col77 -> {fl} (col80={x[79]!r})')
        print('   OLD:', repr(x))
        print('   NEW:', repr(new))

print(f'total flags: {len(flag_repls)}')

# --- comment reformatting (weighted average: remove colon, use "and") ---
cmt_repls = []
for i, x in enumerate(ls):
    if 'weighted average of:' in x:
        old = x
        # transform text: "average of: X (R1); Y (R2)" -> "average of X (R1) and Y (R2)"
        body = x[:10]  # " 34S  cL E$" prefix = 10 chars? check
        # find "weighted average of:" position
        idx = x.index('weighted average of:')
        newtext = x[idx:].replace('weighted average of:', 'weighted average of')
        newtext = newtext.replace('; ', ' and ')
        newline = x[:idx] + newtext
        newline = newline.rstrip() + ' ' * (80 - len(newline.rstrip()))
        if len(newline) != 80:
            print(f'cmt line {i+1}: newline len {len(newline)}')
        cmt_repls.append((i, old, newline))
        print(f'CMT line {i+1}:')
        print('   OLD:', repr(old))
        print('   NEW:', repr(newline))

print(f'total comment reformats: {len(cmt_repls)}')

# verify uniqueness
print()
for fl, en, i, x, new in flag_repls:
    assert t.count(x) == 1, f'flag L {en} old not unique: {t.count(x)}'
for i, old, new in cmt_repls:
    assert t.count(old) == 1, f'cmt line {i+1} old not unique: {t.count(old)}'
print('all old strings unique')
