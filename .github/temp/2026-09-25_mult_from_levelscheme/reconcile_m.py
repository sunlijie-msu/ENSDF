"""Data reconciliation: move M (multipolarity) values from 34.adp into the adopted .ens.

Scope: only G-record M fields that are EMPTY in the target but present in the source.
Matching: adopted L-record -> source L-record by nearest E(level); within that block,
G-records by exact Egamma string.

Usage: python reconcile_m.py <target.ens> <source.adp>
"""
import re
import sys

TOL = 5.0  # keV, L-record matching tolerance


def parse(path):
    lines = open(path, newline='').read().splitlines()
    levels, gammas = [], []
    cur = None
    for i, ln in enumerate(lines, 1):
        if len(ln) < 20 or ln[6:7] == 'c':
            continue
        if ln[7:8] == 'L' and ln[5:7] == '  ':
            cur = {'line': i, 'e': ln[9:19].strip(), 'j': ln[22:39].strip(),
                   't': ln[39:49].strip(), 'gammas': []}
            levels.append(cur)
        elif ln[7:8] == 'G' and ln[5:7] == '  ':
            g = {'line': i, 'e': ln[9:19].strip(), 'ri': ln[22:29].strip(),
                 'm': ln[32:41].strip(), 'flag': ln[76:77], 'fl': None,
                 'lvl': cur}
            gammas.append(g)
            if cur is not None:
                cur['gammas'].append(g)
        elif ln[7:8] == 'G' and ln[5:7] != '  ' and gammas:
            mm = re.search(r'FL=([0-9.]+)', ln[9:])
            if mm:
                gammas[-1]['fl'] = mm.group(1)
    return lines, levels, gammas


def jpi(j):
    m = re.fullmatch(r'(\d+)([+-])', j.replace(' ', ''))
    return (int(m.group(1)), m.group(2)) if m else None


def nearest(levels, energy):
    best, bd = None, TOL
    for L in levels:
        try:
            e = float(L['e'])
        except ValueError:
            continue
        if abs(e - energy) < bd:
            best, bd = L, abs(e - energy)
    return best


def main():
    tgt_path, src_path = sys.argv[1], sys.argv[2]
    _, t_levels, t_gammas = parse(tgt_path)
    _, s_levels, s_gammas = parse(src_path)

    cands = []
    for g in t_gammas:
        if g['m']:
            continue
        init = g['lvl']
        if init is None:
            continue
        try:
            ge = float(g['e'])
            le = float(init['e'])
        except ValueError:
            continue
        fin = nearest(t_levels, float(g['fl'])) if g['fl'] else nearest(t_levels, le - ge)
        if fin is None:
            continue
        ji, jf = jpi(init['j']), jpi(fin['j'])
        if not ji or not jf:
            continue
        cands.append((init, fin, g))

    print('candidates: target G-records with EMPTY M and definite Jpi at both ends =', len(cands))
    print()
    # how many source gammas carry an M at all
    src_m = [g for g in s_gammas if g['m']]
    print('source G-records with a non-empty M field:', len(src_m), 'of', len(s_gammas))
    print()
    hdr = f"{'line':>5} {'E_lvl':>10} {'Jpi':>5} {'T':>9} {'Eg':>10} {'flag':>4} | " \
          f"{'E_final':>9} {'Jpi_f':>5} | {'source M':>10}"
    print(hdr)
    print('-' * len(hdr))
    plan = []
    for init, fin, g in cands:
        sl = nearest(s_levels, float(init['e']))
        sm = ''
        where = ''
        if sl is not None:
            for sg in sl['gammas']:
                if sg['e'] == g['e'] and sg['m']:
                    sm, where = sg['m'], f"src line {sg['line']}"
                    break
        if sm:
            plan.append((g, init, fin, sm))
        print(f"{g['line']:>5} {init['e']:>10} {init['j']:>5} {init['t']:>9} "
              f"{g['e']:>10} {g['flag']:>4} | {fin['e']:>9} {fin['j']:>5} | "
              f"{sm if sm else '-':>10} {where}")
    print()
    print('MOVE candidates (source M found):', len(plan))
    for g, init, fin, sm in plan:
        print(f"  line {g['line']:>5}  E_lvl {init['e']:>10}  Eg {g['e']:>10}  "
              f"flag {g['flag']}  ->  M = {sm}")
    print()
    print('=' * 90)
    print('LOOSE LOOKUP: nearest source gamma (any dE) in the matched source level block,')
    print('             only listed when it carries an M and the exact-string match failed')
    print('=' * 90)
    exact = {(g['line']) for g, _, _, _ in plan}
    for init, fin, g in cands:
        if g['line'] in exact or not g['m'] == '':
            continue
        sl = nearest(s_levels, float(init['e']))
        if sl is None:
            continue
        best, bd = None, None
        try:
            ge = float(g['e'])
        except ValueError:
            continue
        for sg in sl['gammas']:
            if not sg['m']:
                continue
            try:
                d = abs(float(sg['e']) - ge)
            except ValueError:
                continue
            if bd is None or d < bd:
                best, bd = sg, d
        if best is not None:
            print(f"tgt line {g['line']:>5} E_lvl {init['e']:>10} Eg {g['e']:>10} "
                  f"-> src line {best['line']:>5} E_lvl {sl['e']:>10} "
                  f"Eg {best['e']:>10} M {best['m']:>10}  dE={bd:.3f}")
    print()
    print('NOTE: target G-record with FL= continuation records keep their col 77 flag '
          'and any intensity; only cols 33-41 change.')


if __name__ == '__main__':
    main()
