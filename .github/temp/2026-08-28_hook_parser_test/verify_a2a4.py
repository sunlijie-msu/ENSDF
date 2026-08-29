# READ-ONLY: verify exact oldStrings (full A2,A4 pair + trailing spaces) exist, print counts.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

# no-source pairs -> add ' (1967Wi01).'
NOSRC = ['A{-2}=-0.400, A{-4}=+0.007',
         'A{-2}=-0.405, A{-4}=-0.043',
         'A{-2}=-0.242, A{-4}=-0.020',
         'A{-2}=-0.127, A{-4}=-0.068',
         'A{-2}=-0.195, A{-4}=-0.022',
         'A{-2}=-0.321, A{-4}=-0.080',
         'A{-2}=-0.420, A{-4}=-0.009']
# with-source pairs -> append '.'
WITHSRC = ['A{-2}=-0.289, A{-4}=-0.039 (1967Wi01)',
           'A{-2}=+0.099, A{-4}=-0.042 (1967Wi01)',
           'A{-2}=+0.339, A{-4}=+0.001 (1967Wi01)',
           'A{-2}=+0.645, A{-4}=-0.068 (1967Wi01)',
           'A{-2}=-0.457, A{-4}=-0.029 (1967Wi01)',
           'A{-2}=+0.188, A{-4}=+0.025 (1967Wi01)']

print('--- no-source (consume 12 trailing spaces) ---')
for p in NOSRC:
    old = p + ' ' * 12
    print(f'MATCH={old in t}  {p!r}+12sp')
print('--- with-source (consume 1 trailing space) ---')
for p in WITHSRC:
    old = p + ' '
    print(f'MATCH={old in t}  {p!r}+1sp')

# double-check each full pair appears exactly once
for p in NOSRC + WITHSRC:
    cnt = t.count(p)
    if cnt != 1:
        print(f'COUNT-ISSUE: {p!r} appears {cnt} times')
print('done')
