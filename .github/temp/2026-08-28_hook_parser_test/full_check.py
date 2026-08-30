path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# Mc07 Table 2: res# -> (gamma energies to ground/2127/3304, Mc07 ratios γ0,γ1,γ2,γH)
# file level -> (res, g0,g1,g2 energies)
MC = {
    10791: (1,  {'g0':'10789','g1':'8662','g2':'7486'}, (1,0.2,0.05,None)),
    11025: (9,  {'g0':'11023','g1':'8896','g2':'7720'}, (1,0.14,0.17,None)),
    11088: (11, {'g0':'11086','g1':'8959','g2':'7783'}, (1,0.44,0.47,None)),
    11142: (13, {'g0':'11140','g1':'9013','g2':'7837'}, (1,0.18,0.09,None)),
    11165: (14, {'g0':'11163','g1':'9036','g2':'7860'}, (1,0.17,1.3,None)),
    11220: (17, {'g0':'11218','g1':'9091','g2':'7915'}, (1,1.5,3.1,13)),
    11233: (18, {'g0':'11231','g1':'9104','g2':'7928'}, (1,0.15,4.1,None)),
    11315: (21, {'g0':'11313','g1':'9186','g2':'8010'}, (1,0.38,0.67,None)),
    11323: (22, {'g0':'11321','g1':'9194','g2':'8018'}, (1,0.65,0.48,None)),
    11358: (23, {'g0':'11356','g1':'9229','g2':'8053'}, (1,0.49,2.8,None)),
    11372: (24, {'g0':'11370','g1':'9243','g2':'8067'}, (1,17,7.4,None)),
    11381: (25, {'g0':'11379','g1':'9252','g2':'8076'}, (1,0.89,2.7,7)),
    11420: (28, {'g0':'11418','g1':'9291','g2':'8115'}, (1,0.19,0.05,None)),
    11490: (32, {'g0':'11488','g1':'9361','g2':'8185'}, (1,0.46,0.56,13)),
    11545: (34, {'g0':'11543','g1':'9416','g2':'8240'}, (1,0.96,1.6,26)),
    11643: (36, {'g0':'11641','g1':'9514','g2':'8338'}, (1,0.25,0.20,7.5)),
}

def get_ri(en):
    for x in ls:
        if x.startswith(' 34S   G ' + en + ' '):
            r = x[22:29].strip()
            return float(r) if r and r.replace('.','').isdigit() else None
    return None

print('=== Full Mc07 Table 2 ratio cross-check (all 16 resonances) ===')
print('For each: file RI normalized to strongest=100; check γ0:γ1:γ2:γH ratios vs Mc07')
allok = True
for lev, (res, gs, ratios) in MC.items():
    r0, r1, r2, rH = (get_ri(gs['g0']), get_ri(gs['g1']), get_ri(gs['g2']), None)
    m0, m1, m2, mH = ratios
    # normalize Mc07 to strongest=100
    mx = max(x for x in (m0, m1, m2) if x is not None)
    s = 100.0 / mx
    want = {'g0': m0*s, 'g1': m1*s, 'g2': m2*s}
    got = {'g0': r0, 'g1': r1, 'g2': r2}
    # tolerance 0.2 (rounding to 1 decimal)
    tol = 0.2
    ok = all(abs(got[k]-want[k]) < tol for k in ('g0','g1','g2') if got[k] is not None)
    allok = allok and ok
    print(f'  res {res:2} lev {lev}: file γ0={r0} γ1={r1} γ2={r2} | want(strong=100) γ0={want["g0"]:.1f} γ1={want["g1"]:.1f} γ2={want["g2"]:.1f} {"OK" if ok else "**MISMATCH**"}')
print('ALL 16 MATCH:', allok)

# check γH comments match rescaled
print()
print('=== γH comment values ===')
for lev, (res, gs, ratios) in MC.items():
    if ratios[3] is None:
        continue
    # find comment
    for x in ls:
        if 'intensities =' in x and x.startswith(' 34S  cL $') and f'states that |g intensities' in x:
            pass
    # scope by level
print()
# γH check via comment text
for lev, (res, gs, ratios) in MC.items():
    mH = ratios[3]
    if mH is None:
        continue
    m0,m1,m2 = ratios[:3]
    mx = max(m0,m1,m2); s = 100.0/mx
    wantH = mH * s
    # find intensity comment in this level block
    l_idx = [i for i,x in enumerate(ls) if x.startswith(' 34S   L ')]
    li = next(i for i in l_idx if ls[i][9:19].strip()==str(lev))
    nxt = min([i for i in l_idx if i>li], default=len(ls))
    found = None
    for i in range(li, nxt):
        if 'intensities =' in ls[i]:
            found = ls[i]
            break
    if found:
        import re
        m = re.search(r'intensities = (\d+)', found)
        got = int(m.group(1)) if m else None
        print(f'  res {res} lev {lev}: comment intensities={got} want={wantH:.0f} {"OK" if abs(got-wantH)<1 else "MISMATCH"}')
    else:
        print(f'  res {res} lev {lev}: no intensity comment')
