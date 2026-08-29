# READ-ONLY: verify exact oldStrings for Va08 partial-width edits, compute new lengths.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

# (substring, trailing spaces to consume, replacement)
edits = [
    ('|G{-|g}=0.84 eV',          11, '|G{-|g}=0.84 eV (1964Va08)'),
    ('|G{-|g}=1.3 eV {IGT}',      4, '|G{-|g}>1.3 eV (1964Va08)'),
    ('|G{-|g}=0.7 eV {IGT}',      4, '|G{-|g}>0.7 eV (1964Va08)'),
    ('|G{-|g}=0.73 eV',          11, '|G{-|g}=0.73 eV (1964Va08)'),
]
for sub, n, rep in edits:
    old = sub + ' ' * n
    cnt = t.count(sub)
    print(f'sub={sub!r} cnt={cnt} old-match={old in t} len_old={len(sub)} len_new={len(rep)} net={len(rep)-len(sub)}')
