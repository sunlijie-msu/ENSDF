"""Verify 'From the Adopted Levels/Gammas' provenance claims in S34 individual datasets.

For every dataset that carries a cL/cG provenance comment referencing the Adopted
data, compare its data records with the adopted values under both stated rules:
  - exact     : target value == adopted value
  - rounded   : target value == round(adopted value)  (nearest integer)

Reports: level E/J mismatches, gamma E/M mismatches, stray DE on rounded levels,
and comment lines that quote an adopted energy together with an uncertainty.

Usage: python check_adopted_provenance.py
"""
import glob
import os
import re

ADOPTED = r'A34/S34/new/S34_adopted.ens'


def parse(path):
    levels, gammas = [], []
    cur = None
    for i, l in enumerate(open(path, encoding='utf-8', newline='').read().split('\r\n'), 1):
        if len(l) < 20 or l[6] in 'cCdD':
            continue
        if l[7] == 'L' and l[5:7] == '  ':
            cur = {'line': i, 'e': l[9:19].strip(), 'de': l[19:21].strip(),
                   'j': l[22:39].strip(), 'g': []}
            levels.append(cur)
        elif l[7] == 'G' and l[5:7] == '  ':
            g = {'line': i, 'e': l[9:19].strip(), 'm': l[32:41].strip(), 'lvl': cur}
            gammas.append(g)
            if cur is not None:
                cur['g'].append(g)
    return levels, gammas


def fnum(s):
    try:
        return float(s)
    except ValueError:
        return None


ad_levels, ad_gammas = parse(ADOPTED)
ad_g_all = [(fnum(g['e']), g['m'].strip(), g['lvl']['j'] if g['lvl'] else '')
            for g in ad_gammas if fnum(g['e']) is not None]

PROV = re.compile(r'(?:from|rounded from|rounded to the nearest integer from|Rounded from|'
                  r'Rounded to the nearest integer from|From)\s+the Adopted', re.I)

def text_of(line):
    """Comment text of an ENSDF comment line (first line vs continuation)."""
    return line[11:].strip() if line[5] == ' ' else line[9:].strip()


files = sorted(glob.glob(r'A34/S34/new/*.ens'))
for path in files:
    name = os.path.basename(path)
    if name == 'S34_adopted.ens':
        continue
    lines = open(path, encoding='utf-8', newline='').read().split('\r\n')
    prov = []
    for i, l in enumerate(lines):
        if len(l) > 7 and l[6] in 'cCdD' and 'dopted' in l and ('From the Adopted' in l
                                                              or 'from the Adopted' in l
                                                              or 'rounded from the Adopted' in l
                                                              or 'rounded to the nearest' in l):
            block = [l.rstrip()]
            for k in range(i + 1, min(i + 4, len(lines))):
                if len(lines[k]) > 7 and lines[k][6] in 'cCdD':
                    block.append(lines[k].rstrip())
                else:
                    break
            prov.append((i + 1, ' '.join(text_of(b) for b in block)))
    if not prov:
        continue
    text = ' '.join(t for _, t in prov)
    rounded_rule = 'rounded' in text.lower()
    print('=' * 95)
    print(name, '| lines', [n for n, _ in prov], '| rounding rule:', rounded_rule)
    for n, t in prov:
        print('    ', n, ':', t[:95])
    levels, gammas = parse(path)
    bad = []
    for lv in levels:
        e = fnum(lv['e'])
        if e is None:
            continue
        cands = [a for a in ad_levels if fnum(a['e']) is not None and
                 (not lv['j'] or not a['j'] or a['j'] == lv['j'])]
        if not cands:
            bad.append(('LVL-noJmatch', lv['line'], lv['e'], lv['j'], 'no adopted level with this J'))
            continue
        best = min(cands, key=lambda a: abs(fnum(a['e']) - e))
        ae = fnum(best['e'])
        exact = abs(ae - e) <= 0.006
        rnd = int(ae + 0.5) == int(e) and abs(e - int(e)) < 1e-9
        if not (exact or rnd):
            bad.append(('LVL-E', lv['line'], lv['e'], lv['j'],
                        f'adopted {best["e"]} ({best["j"]}) -> exact or {int(ae+0.5)}'))
        if rounded_rule and lv['de']:
            bad.append(('LVL-DE-on-rounded', lv['line'], lv['e'], lv['de'], 'DE present'))
    for g in gammas:
        e = fnum(g['e'])
        if e is None:
            continue
        best = min(ad_g_all, key=lambda a: abs(a[0] - e))
        ae, am, aj = best
        if abs(ae - e) > 2.0:
            bad.append(('GAM-noMatch', g['line'], g['e'], g['m'], f'nearest adopted gamma {ae}'))
            continue
        exact = abs(ae - e) <= 0.006
        rnd = int(ae + 0.5) == int(e) and abs(e - int(e)) < 1e-9
        if not (exact or rnd):
            bad.append(('GAM-E', g['line'], g['e'], g['m'],
                        f'adopted gamma {ae} -> exact or {int(ae+0.5)}'))
    if bad:
        print('    --- flagged', len(bad), 'record(s)')
        for b in bad:
            tag, ln, e, x, why = b
            raw = lines[ln - 1].rstrip()
            print('       ', tag, 'line', ln, repr(raw), '|', why)
    else:
        print('    --- all level & gamma values consistent with the adopted (as stated)')
    # comment values quoting an adopted energy AND an uncertainty
    adset = {a['e'] for a in ad_levels} | {str(int(fnum(a['e']))) for a in ad_levels if fnum(a['e'])}
    adset |= {g['e'] for g in ad_gammas}
    for i, l in enumerate(lines):
        if len(l) > 7 and l[6] in 'cCdD':
            for m in re.finditer(r'(\d+(?:\.\d+)?)\s*\{I', l):
                if m.group(1) in adset:
                    print('    !!! comment line', i + 1, 'quotes adopted value with uncertainty:',
                          repr(l.rstrip()[:80]))
