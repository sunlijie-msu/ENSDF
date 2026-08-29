# READ-ONLY: print exact OLD/NEW for removing the 5 'G x' records and adding cL comments.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
lines = open(path, encoding='utf-8', newline='').read().replace('\r\n','\n').replace('\r','\n').split('\n')

# levels with G x -> intensity value
targets = {'11220': 1300, '11381': 700, '11490': 1300, '11545': 2600, '11643': 750}

def is_L(ln): return len(ln) >= 9 and ln[5:9] == '  L '

def comment_pair(val):
    c1 = (' 34S  cL $1965Mc07 states that |g intensities =%d from this resonance to' % val).ljust(80)
    c2 = ' 34S 2cL 34S levels higher than 3304 keV.'.ljust(80)
    return c1, c2

for i, ln in enumerate(lines):
    if is_L(ln) and ln[9:19].strip() in targets:
        e = ln[9:19].strip()
        val = targets[e]
        # find G x line index
        gx = None
        j = i + 1
        while j < len(lines):
            if lines[j].startswith(' 34S   G x'):
                gx = j
                break
            if is_L(lines[j]):
                break
            j += 1
        if gx is None:
            print(f'L{e}: NO G x found!')
            continue
        # find end of block: include following 'cG RI$from 1965Mc07' (attached to G x)
        end = gx + 1
        if end < len(lines) and 'cG RI$from 1965Mc07' in lines[end]:
            end += 1
        old = lines[i+1:end]           # lines after L record up to (not incl) end
        c1, c2 = comment_pair(val)
        new = []
        # keep cL comment lines (up to gx), drop G x (+ optional cG), append new comment
        for k in range(i+1, gx):
            new.append(lines[k])
        new.append(c1)
        new.append(c2)
        print(f'=== L{e} (val={val}) ===')
        print('--- OLD ---')
        for o in old:
            ntrail = len(o) - len(o.rstrip())
            print(f'L{len(o)}[{o.rstrip()}]<sp={ntrail}>')
        print('--- NEW ---')
        for n in new:
            ntrail = len(n) - len(n.rstrip())
            print(f'L{len(n)}[{n.rstrip()}]<sp={ntrail}>')
        print()
