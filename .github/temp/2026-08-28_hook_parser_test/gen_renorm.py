path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# level -> {gamma_energy: (old_ri, new_ri)}
renorm = {
    11165: {'7860': ('130', '100'), '9036': ('17', '13.1'), '11163': ('100', '76.9')},
    11220: {'7915': ('130', '100'), '9091': ('150', '48.4'), '11218': ('100', '32.3')},
    11233: {'7928': ('410', '100'), '9104': ('15', '3.7'), '11231': ('100', '24.4')},
    11358: {'8053': ('280', '100'), '9229': ('49', '17.5'), '11356': ('100', '35.7')},
    11372: {'8067': ('740', '43.5'), '9243': ('1700', '100'), '11370': ('100', '5.9')},
    11381: {'8076': ('270', '100'), '9252': ('890', '33.0'), '11379': ('100', '37.0')},
    11545: {'8240': ('160', '100'), '9416': ('96', '60.0'), '11543': ('100', '62.5')},
}

# comment rescale: (old_value, new_value) for "intensities = NNNN"
comments = {
    11220: ('1300', '419'),
    11381: ('700', '259'),
    11545: ('2600', '1625'),
}

problems = []
g_repls = []
for lev, gs in renorm.items():
    for en, (old_ri, new_ri) in gs.items():
        # find line
        found = None
        for i, x in enumerate(ls):
            if x.startswith(' 34S   G ' + en + ' '):
                found = (i, x)
                break
        if found is None:
            problems.append(f'G {en} (lev {lev}): NOT FOUND')
            continue
        i, line = found
        if len(line) != 80:
            problems.append(f'G {en}: len {len(line)}')
            continue
        cur_ri = line[22:29].strip()
        if cur_ri != old_ri:
            problems.append(f'G {en}: RI={cur_ri!r} != expected {old_ri!r}')
            continue
        # rebuild: RI field cols 23-29 (idx 22-28) = new_ri left-justified
        newline = line[:22] + new_ri.ljust(7) + line[29:]
        if len(newline) != 80:
            problems.append(f'G {en}: newline len {len(newline)}')
            continue
        g_repls.append((en, lev, i, line, newline, old_ri, new_ri))

print(f'G replacements: {len(g_repls)}')
if problems:
    print('PROBLEMS:')
    for p in problems:
        print('  ', p)

# comment replacements - scoped by level block
c_repls = []
# find L-record line indices
l_idx = [i for i, x in enumerate(ls) if x.startswith(' 34S   L ')]
for lev, (old_v, new_v) in comments.items():
    marker = 'intensities = ' + old_v
    # find the L record for this level
    li = None
    for i in l_idx:
        if ls[i][9:19].strip() == str(lev):
            li = i
            break
    if li is None:
        print(f'comment lev {lev}: L record not found')
        continue
    nxt = min([i for i in l_idx if i > li], default=len(ls))
    found = None
    for i in range(li, nxt):
        if marker in ls[i] and ls[i].startswith(' 34S  cL $'):
            found = i
            break
    if found is None:
        print(f'comment lev {lev}: intensity line not found in block')
        continue
    x = ls[found]
    newline = x.replace(marker, 'intensities = ' + new_v)
    c_repls.append((lev, found, x, newline, old_v, new_v))
print(f'comment replacements: {len(c_repls)}')

# verify uniqueness of all old G lines
for en, lev, i, line, newline, old_ri, new_ri in g_repls:
    assert t.count(line) == 1, f'G {en} not unique: {t.count(line)}'

print()
print('=== G replacements ===')
for en, lev, i, line, newline, old_ri, new_ri in g_repls:
    print(f'G {en} (lev {lev}) line {i+1}: RI {old_ri}->{new_ri}')
    print('  OLD', repr(line))
    print('  NEW', repr(newline))

print()
print('=== comment replacements (full block context) ===')
# rebuild comment blocks with L-record anchor for uniqueness
for lev, (old_v, new_v) in comments.items():
    l_idx = [i for i, x in enumerate(ls) if x.startswith(' 34S   L ')]
    li = next(i for i in l_idx if ls[i][9:19].strip() == str(lev))
    # find the cL intensity line within block
    nxt = min([i for i in l_idx if i > li], default=len(ls))
    ci = next(i for i in range(li, nxt) if 'intensities = ' + old_v in ls[i])
    # block = L record through the 2cL continuation after the comment
    block_end = ci + 2 if ci + 1 < nxt and ls[ci+1].startswith(' 34S 2cL ') else ci
    block_old = ls[li:block_end + 1]
    block_new = [x.replace('intensities = ' + old_v, 'intensities = ' + new_v) for x in block_old]
    oldb = '\n'.join(block_old)
    newb = '\n'.join(block_new)
    print(f'lev {lev}: block unique={t.count(oldb)==1}, lines {li+1}-{block_end+1}')
    print('  OLD BLOCK:')
    for x in block_old:
        print('   ', repr(x))
    print('  NEW BLOCK:')
    for x in block_new:
        print('   ', repr(x))
    print()
