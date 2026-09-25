"""Scan an adopted ENSDF file for gammas whose multipolarity is constrained by the
level scheme alone: both initial and final level have single-valued J and single
value of parity, and the initial level has a lifetime (T field).

Output: for every such gamma, the allowed multipolarity family.

Usage: python scan_mult_from_scheme.py <adopted.ens> [--all]
"""
import re
import sys

LEVEL_TOL = 1.5  # keV, tolerance when matching E(level)-E(gamma) to a level


def parse(path):
    lines = open(path, newline='').read().splitlines()
    levels, gammas = [], []
    cur_lvl, cur_gam = None, None
    for i, ln in enumerate(lines, 1):
        if len(ln) < 20 or ln.startswith(' ' * 6):
            pass
        field = ln[7:8]
        c6 = ln[5:6]
        if ln[6:7] == 'c':            # comment
            continue
        if field == 'L' and ln[5:7] == '  ':
            cur_lvl = {
                'line': i,
                'e': ln[9:19].strip(),
                'j': ln[22:39].strip(),
                't': ln[39:49].strip(),
            }
            levels.append(cur_lvl)
        elif field == 'G' and ln[5:7] == '  ':
            cur_gam = {
                'line': i,
                'e': ln[9:19].strip(),
                'ri': ln[22:29].strip(),
                'm': ln[32:41].strip(),
                'fl': None,
                'lvl': cur_lvl,
            }
            gammas.append(cur_gam)
        elif field == 'G' and c6 != ' ' and cur_gam is not None:
            m = re.search(r'FL=([0-9.]+)', ln[9:])
            if m:
                cur_gam['fl'] = m.group(1)
    return lines, levels, gammas


def jpi(j):
    j = j.replace(' ', '')
    m = re.fullmatch(r'(\d+)([+-])', j)
    return (int(m.group(1)), m.group(2)) if m else None


def family(dj, dpi):
    lmin = max(1, abs(dj))
    out = []
    for L in (lmin, lmin + 1):
        electric = (L % 2 == 1) == (dpi == 'yes')
        out.append(('E' if electric else 'M') + str(L))
    if out[1][0] == out[0][0]:
        return out[0]
    return out[0] + '+' + out[1]


def multipoles(mstr):
    """Return list of (label, L, character) parsed from an M field."""
    out = []
    for m in re.finditer(r'([EM])(\d)', mstr):
        out.append((m.group(0), int(m.group(2)), m.group(1)))
    for m in re.finditer(r'(?<![EM0-9])D(?!\d)', mstr):
        out.append(('D', 1, '?'))
    for m in re.finditer(r'(?<![EM])(?<![MQ])Q(?!\d)', mstr):
        out.append(('Q', 2, '?'))
    return out


def forbidden(mstr, dj, dpi):
    """List multipoles in the M field that the level scheme forbids.

    E(L) changes parity for odd L, M(L) changes parity for even L.
    """
    bad = []
    for label, L, ch in multipoles(mstr):
        odd = L % 2 == 1
        if ch == 'E':
            ok = odd == (dpi == 'yes')
        elif ch == 'M':
            ok = odd != (dpi == 'yes')
        else:
            ok = True
        if not ok or L < max(1, abs(dj)):
            bad.append(label)
    return bad


def main():
    path = sys.argv[1]
    show_all = '--all' in sys.argv
    lines, levels, gammas = parse(path)

    lv = []
    for L in levels:
        try:
            lv.append((float(L['e']), L))
        except ValueError:
            pass

    def find(energy):
        best, bd = None, LEVEL_TOL
        for e, L in lv:
            d = abs(e - energy)
            if d <= bd:
                best, bd = L, d
        return best, bd

    rows, unresolved = [], 0
    for g in gammas:
        try:
            ge = float(g['e'])
        except ValueError:
            continue
        init = g['lvl']
        if init is None:
            continue
        fin = None
        if g['fl']:
            fin, _ = find(float(g['fl']))
        else:
            fin, _ = find(float(init['e']) - ge) if init['e'] else (None, 0)
        if fin is None:
            unresolved += 1
            continue
        ji, jf = jpi(init['j']), jpi(fin['j'])
        if not ji or not jf:
            continue
        dj, dpi = ji[0] - jf[0], ('no' if ji[1] == jf[1] else 'yes')
        rows.append((init, fin, g, dj, dpi, family(dj, dpi)))

    print('file            :', path)
    print('levels / gammas :', len(levels), len(gammas))
    print('unresolved final level (E_lvl - E_g not matching a level):', unresolved)
    print('gammas with unique J*pi at BOTH ends :', len(rows))
    withT = [r for r in rows if r[0]['t'] and r[0]['t'] != 'STABLE']
    withT = [r for r in withT if not r[0]['t'].startswith('GT') and r[0]['t'] != 'STABLE']
    print('  ... and initial level has T field  :', len(withT))
    print()

    def dump(rs, title):
        print('=' * 100)
        print(title)
        print('=' * 100)
        print(f"{'E_level':>10} {'Jpi':>6} {'T':>9} | {'Eg':>10} {'RI':>7} {'M(now)':>12} "
              f"| {'E_final':>9} {'Jpi_f':>6} | dJ dpi | allowed")
        for init, fin, g, dj, dpi, fam in rs:
            print(f"{init['e']:>10} {init['j']:>6} {init['t']:>9} | {g['e']:>10} "
                  f"{g['ri']:>7} {g['m']:>12} | {fin['e']:>9} {fin['j']:>6} | "
                  f"{dj:>2} {dpi:>3} | {fam}")
        print()
    blank = [r for r in withT if not r[2]['m']]
    dump(blank, 'A. T available + unique Jpi both ends + MULTIPOLARITY FIELD EMPTY')
    bad = [r for r in withT if forbidden(r[2]['m'], r[3], r[4])]
    dump(bad, 'B. ... MULTIPOLARITY LISTED BUT FORBIDDEN BY THE LEVEL SCHEME')
    if show_all:
        dump(withT, 'C. All candidates (T available, unique Jpi both ends)')


if __name__ == '__main__':
    main()
