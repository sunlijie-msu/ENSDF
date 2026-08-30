path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

def pad(s):
    return s + ' ' * (80 - len(s))

# level -> Va21 "other" value
others = {
    '2122': '2127',
    '5326': '5318',
    '5683': '5680',
    '5694': '5687',
    '5758': '5759',
    '6422': '6423',
}

repls = []
for en, val in others.items():
    li = None
    for i, x in enumerate(ls):
        if x.startswith(' 34S   L ' + en + ' '):
            li = i
            break
    if li is None:
        print(f'L {en}: NOT FOUND')
        continue
    Lrec = ls[li]
    nxt = ls[li+1]
    # insert after L record
    new_comment = pad(f' 34S  cL E$other: {val} (1971Va21).')
    if nxt.startswith(' 34S   L '):
        # L record followed directly by next level (no comment)
        old = Lrec + '\n' + nxt
        new = Lrec + '\n' + new_comment + '\n' + nxt
        print(f'L {en}: insert after L (before next L)')
    else:
        old = Lrec + '\n' + nxt
        new = Lrec + '\n' + new_comment + '\n' + nxt
        print(f'L {en}: insert after L (before {nxt[:20]!r})')
    repls.append((en, old, new))
    print('  OLD:', repr(old[:100]))
    print('  NEW:', repr(new[:100]))

print()
print('insertions:', len(repls))
for en, old, new in repls:
    assert t.count(old) == 1, f'L {en} old not unique: {t.count(old)}'
    print(f'=== L {en} ===')
    print('OLD:', repr(old))
    print('NEW:', repr(new))
print('all unique OK')
