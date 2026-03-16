"""Debug: Find L-records in Cl34_33s_p_g.ens at target energies."""

targets = [1887.29, 2157.9, 2181.1, 2375.7, 2611.03, 2721.3, 3545.08,
           3600.28, 3631.7, 3773.72, 3983.0, 4076.2, 4139.7, 4354.2,
           4417.3, 4515.7, 6169.4, 6208.2, 6229.5]

f = open(r'A34\Cl34\new\Cl34_33s_p_g.ens')
lines = [l.rstrip('\n') for l in f.readlines()]
f.close()
print(f'Total lines: {len(lines)}')

ei = None
for i, line in enumerate(lines):
    if len(line) < 8:
        continue
    cont = line[5]
    rtype = line[7]
    if cont == ' ' and rtype == 'L':
        e_str = line[9:19].strip()
        try:
            e = float(e_str)
            if any(abs(e - t) < 0.5 for t in targets):
                print(f'L{i+1:4d}  col5=[{cont}] col8=[{rtype}] E={e}  raw=[{line[:60]}]')
                ei = e
        except:
            pass
    elif cont == ' ' and rtype == 'G' and ei is not None:
        eg_str = line[9:19].strip()
        print(f'  G{i+1:4d} Eg={eg_str:<12} RI={line[22:29]!r} DRI={line[29:31]!r}')
    elif rtype == ' ' and cont == 'c':
        # cG comment? col6=c, col7=G
        pass
    elif line[5:7] == 'cG' or line[5:7] == 'cg':
        # cG comment line
        if ei is not None:
            print(f'  cG{i+1:3d}: {line[:80]}')
