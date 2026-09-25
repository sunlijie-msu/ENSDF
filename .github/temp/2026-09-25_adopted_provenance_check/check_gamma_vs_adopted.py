"""Compare each gamma of an S34 individual dataset with the adopted gamma of the SAME
transition (initial level and final level), to audit 'From the Adopted Gammas' claims.

Final level: F G FL= continuation if present, else E(level) - Egamma matched to the
dataset's own level list.
Usage: python check_gamma_vs_adopted.py <file> [...]
"""
import glob
import math
import os
import re
import sys

ADOPTED = r'A34/S34/new/S34_adopted.ens'


def parse(path):
    lines = open(path, encoding='utf-8', newline='').read().split('\r\n')
    levels, gammas = [], []
    cur = None
    last = None
    for i, l in enumerate(lines, 1):
        if len(l) < 20 or l[6] in 'cCdD':
            continue
        if l[7] == 'L' and l[5:7] == '  ':
            cur = {'line': i, 'e': l[9:19].strip(), 'j': l[22:39].strip(), 'g': []}
            levels.append(cur)
        elif l[7] == 'G' and l[5:7] == '  ':
            last = {'line': i, 'e': l[9:19].strip(), 'm': l[32:41].strip(),
                    'flag': l[76:77], 'lvl': cur, 'fl': None}
            gammas.append(last)
            if cur is not None:
                cur['g'].append(last)
        elif l[7] == 'G' and l[5:7] != '  ' and last is not None:
            m = re.search(r'FL=([0-9.]+)', l[9:])
            if m:
                last['fl'] = m.group(1)
    return lines, levels, gammas


def num(s):
    try:
        return float(s)
    except ValueError:
        return None


def final_level(levels, init_e, ge, fl):
    if fl:
        return num(fl)
    if init_e is None:
        return None
    tgt = init_e - ge
    best, bd = None, 3.0
    for lv in levels:
        e = num(lv['e'])
        if e is None:
            continue
        if abs(e - tgt) < bd:
            best, bd = e, abs(e - tgt)
    return best


def rnd(x, step):
    return math.floor(x / step + 0.5) * step


def fmt(x):
    return str(int(x)) if abs(x - int(x)) < 1e-9 else ('%.1f' % x)


_, adlvl, adgam = parse(ADOPTED)
ad = []
for g in adgam:
    ie = num(g['lvl']['e']) if g['lvl'] else None
    ge = num(g['e'])
    if ie is None or ge is None:
        continue
    fe = final_level(adlvl, ie, ge, g['fl'])
    ad.append({'e': ge, 'm': g['m'].strip(), 'ie': ie, 'fe': fe, 'line': g['line']})

files = sys.argv[1:] or sorted(glob.glob(r'A34/S34/new/*.ens'))
for path in files:
    if os.path.basename(path) == 'S34_adopted.ens':
        continue
    lines, levels, gammas = parse(path)
    out = []
    for g in gammas:
        ge = num(g['e'])
        ie = num(g['lvl']['e']) if g['lvl'] else None
        if ge is None or ie is None:
            continue
        fe = final_level(levels, ie, ge, g['fl'])
        cands = [a for a in ad
                 if abs(a['ie'] - ie) < 2.5 and a['fe'] is not None and fe is not None
                 and abs(a['fe'] - fe) < 3.0]
        if not cands:
            continue
        a = min(cands, key=lambda x: abs(x['e'] - ge))
        flag_e = abs(a['e'] - ge) > 0.6
        flag_m = bool(a['m']) and bool(g['m']) and a['m'] != g['m']
        if flag_e or flag_m:
            out.append((g, a, ie, fe, flag_e, flag_m))
    if out:
        print('=' * 100)
        print(os.path.basename(path))
        for g, a, ie, fe, fe_, fm in out:
            print(f"   line {g['line']:>4} Eg {g['e']:>9} (M={g['m'] or '-':<9}) "
                  f"{ie} -> {fe} | adopted Eg {fmt(a['e'])} (M={a['m'] or '-'}) "
                  f"line {a['line']} | {'E' if fe_ else ''}{'M' if fm else ''} differs")
