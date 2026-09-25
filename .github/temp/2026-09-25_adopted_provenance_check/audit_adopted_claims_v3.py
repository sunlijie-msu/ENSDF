"""Audit 'From the Adopted ...' claims in the S34 individual datasets (field + scope aware).

A claim such as
    cL E(A),J(A)$From the Adopted Levels.      -> only the E and J of L-records flagged 'A'
    cG M,MR$From the Adopted Gammas.           -> only the M/MR of G-records
    cP J,T$From the Adopted Levels of 34Cl.    -> parent record, ignored here
is checked only for the fields it names, and only for records whose col-77 flag is
named in the identifier (all records when no letters are named).

Precision comes from the text: 'nearest integer' (1 keV), 'nearest 0.1 keV',
otherwise exact.

Usage: python audit_adopted_claims_v3.py
"""
import glob
import math
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
                   'j': l[22:39].strip(), 'flag': l[76:77]}
            levels.append(cur)
        elif l[7] == 'G' and l[5:7] == '  ':
            gammas.append({'line': i, 'e': l[9:19].strip(), 'm': l[32:41].strip(),
                           'flag': l[76:77], 'lvl': cur})
    return levels, gammas


def num(s):
    try:
        return float(s)
    except ValueError:
        return None


def rnd(x, step):
    return math.floor(x / step + 0.5) * step


def fmt(x):
    return str(int(x)) if abs(x - int(x)) < 1e-9 else ('%.1f' % x)


def text_of(line):
    if len(line) < 12:
        return line.strip()
    return line[11:].strip() if line[5] == ' ' else line[9:].strip()


def ident_of(line):
    d = line.find('$')
    return line[9:d].strip() if d > 0 else ''


def fields_of(ident):
    out = {}
    for tok in ident.split(','):
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r'([A-Za-z]+)(?:\(([A-Za-z]+)\))?', tok)
        if m:
            out[m.group(1).upper()] = set(m.group(2) or '')
    return out


def precision(txt):
    if re.search(r'nearest\s+integer', txt, re.I):
        return 1.0
    m = re.search(r'nearest\s+([\d.]*)\s*keV', txt, re.I)
    if m:
        return float(m.group(1)) if m.group(1) else 1.0
    return None


alvl, agam = parse(ADOPTED)
agn = [(num(g['e']), g['m'].strip(), g['line']) for g in agam if num(g['e']) is not None]

for path in sorted(glob.glob(r'A34/S34/new/*.ens')):
    name = os.path.basename(path)
    if name == 'S34_adopted.ens':
        continue
    lines = open(path, encoding='utf-8', newline='').read().split('\r\n')
    claims = []
    for i, l in enumerate(lines):
        if len(l) > 12 and l[6] == 'c' and l[5] == ' ' and 'dopted' in l and 'rom the Adopted' in l:
            blk = [l]
            for k in range(i + 1, min(i + 5, len(lines))):
                if len(lines[k]) > 12 and lines[k][6] == 'c':
                    blk.append(lines[k])
                else:
                    break
            claims.append({'line': i + 1, 'rectype': l[7], 'ident': ident_of(l),
                           'fields': fields_of(ident_of(l)),
                           'text': ' '.join(text_of(b) for b in blk)})
    if not claims:
        continue
    levels, gammas = parse(path)
    findings = []
    for c in claims:
        if c['rectype'] not in 'LG':
            continue
        step = precision(c['text'])
        for fld, flags in c['fields'].items():
            if c['rectype'] == 'L' and fld == 'E':
                for lv in levels:
                    if flags and lv['flag'] not in flags:
                        continue
                    e = num(lv['e'])
                    if e is None:
                        continue
                    cands = [a for a in alvl if num(a['e']) is not None and
                             (not lv['j'] or not a['j'] or a['j'].strip() == lv['j'].strip())]
                    if not cands:
                        findings.append(('LVL-noJmatch', lv['line'], lv['e'], lv['j'], 'no adopted level with this J', c['line']))
                        continue
                    best = min(cands, key=lambda a: abs(num(a['e']) - e))
                    ae = num(best['e'])
                    want = fmt(rnd(ae, step)) if step else best['e']
                    ok = (abs(rnd(ae, step) - e) < 1e-9) if step else (abs(ae - e) < 0.006)
                    if not ok:
                        findings.append(('LVL-E', lv['line'], lv['e'], lv['j'], f'adopted {best["e"]} -> {want}', c['line']))
            if c['rectype'] == 'L' and fld == 'J':
                for lv in levels:
                    if flags and lv['flag'] not in flags:
                        continue
                    cands = [a for a in alvl if num(a['e']) is not None and
                             abs(num(a['e']) - num(lv['e'])) <= (0.6 if step in (None, 1.0) else 0.06)
                             and a['j'].strip()]
                    if cands and lv['j'].strip() and all(a['j'].strip() != lv['j'].strip() for a in cands):
                        findings.append(('LVL-J', lv['line'], lv['e'], lv['j'], 'adopted J: ' + '/'.join(sorted({a['j'].strip() for a in cands})), c['line']))
            if c['rectype'] == 'G' and fld == 'E':
                for g in gammas:
                    if flags and g['flag'] not in flags:
                        continue
                    e = num(g['e'])
                    if e is None:
                        continue
                    ae, am, aline = min(agn, key=lambda a: abs(a[0] - e))
                    if abs(ae - e) > 2.0:
                        continue  # gamma not present in the adopted list (level-difference value)
                    want = fmt(rnd(ae, step)) if step else fmt(ae)
                    ok = (abs(rnd(ae, step) - e) < 1e-9) if step else (abs(ae - e) < 0.006)
                    if not ok:
                        findings.append(('GAM-E', g['line'], g['e'], g['m'], f'adopted gamma {fmt(ae)} -> {want}', c['line']))
            if c['rectype'] == 'G' and fld == 'M':
                for g in gammas:
                    if flags and g['flag'] not in flags:
                        continue
                    e = num(g['e'])
                    if e is None:
                        continue
                    ae, am, aline = min(agn, key=lambda a: abs(a[0] - e))
                    if abs(ae - e) > 2.0 or not am or not g['m'].strip():
                        continue
                    if g['m'].strip() != am:
                        findings.append(('GAM-M', g['line'], g['e'], g['m'], f'adopted gamma {fmt(ae)} has M={am}', c['line']))
    print('=' * 100)
    print(name)
    for c in claims:
        print('   claim line', c['line'], c['rectype'], repr(c['ident']), '|', c['text'][:85])
    if findings:
        for f in findings:
            print('   !!', f[0], 'line', f[1], repr(lines[f[1] - 1].rstrip()[:58]), '|', f[4], '| claim', f[5])
    else:
        print('   OK - nothing inconsistent with the claim(s)')
