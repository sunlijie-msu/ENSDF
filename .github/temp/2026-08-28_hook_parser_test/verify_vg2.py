# READ-ONLY: confirm final old/new substrings keep lines at exactly 80.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

edits = [
    ('|G{-|g}=0.84 eV',          11, '|G{-|g}=0.84 eV (1964Va08)'),
    ('|G{-|g}=1.3 eV {IGT}',      5, '|G{-|g}>1.3 eV (1964Va08)'),
    ('|G{-|g}=0.7 eV {IGT}',      5, '|G{-|g}>0.7 eV (1964Va08)'),
    ('|G{-|g}=0.73 eV',          11, '|G{-|g}=0.73 eV (1964Va08)'),
]
for sub, n, rep in edits:
    old = sub + ' ' * n
    # find the line containing sub, simulate replacement
    for i, x in enumerate(ls):
        if sub in x:
            newline = x.replace(old, rep, 1)
            print(f'line {i+1}: sub={sub!r} old-match={old in x} newlen={len(newline)} newline={newline.rstrip()!r}')
            break
