#!/usr/bin/env python3
"""
Multipolarity & J$ Jpi argument audit for Fe58_adopted.ens.
Checks: G-record M fields, J$ quoted multipolarities vs G-records,
selection-rule consistency.
"""
import re, sys
from pathlib import Path

fp = Path(r"d:\X\ND\ENSDF\XUNDL\A58\Fe58\old\Fe58_adopted.ens")

def parse_levels_and_gammas(fp):
    levels = {}  # energy_str -> {energy, jpi, line}
    gammas = []  # [{energy_str, energy, m_field, parent_e, line}]
    parent = None
    with open(fp) as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        ln = i+1
        if len(line) < 10: continue
        c6,c7,c8 = line[5],line[6],line[7]
        # Must be data record: cols 6,7 blank, col8 = L or G
        if c6 != ' ' or c7 != ' ': continue
        nucid = line[:5].strip()
        if not nucid: continue
        if c8 == 'L':
            e = line[9:19].strip()
            if e and e[0] in '0123456789.-':
                try:
                    float(e)
                except ValueError:
                    continue
                jpi = line[22:39].strip() if len(line)>39 else ''
                levels[e] = {'energy': float(e), 'jpi': jpi, 'line': ln}
                parent = e
        elif c8 == 'G':
            if parent:
                e = line[9:19].strip()
                if e:
                    # This file uses M field at cols 32-40 (index 31-39)
                    m_raw = line[31:40].strip() if len(line) > 40 else ''
                    # Clean up M field
                    m = m_raw if m_raw else ''
                    gammas.append({'estr': e, 'e': float(e), 'm': m,
                                   'parent': parent, 'line': ln})
    return levels, gammas

def parse_J_comments(fp):
    """Extract multipolarities quoted in cL J$ comments with their gamma energy."""
    refs = []
    with open(fp) as f:
        lines = f.readlines()
    inJ = False; block = []; bstart = 0
    for i, line in enumerate(lines):
        ln = i+1
        if len(line) < 10: continue
        c6,c7,c8 = line[5],line[6],line[7]
        if c7=='c' and c8=='L':
            txt = line[9:80]
            if 'J$' in txt:
                if inJ and block:
                    refs.extend(_extract(block, bstart))
                inJ = True; block = [txt]; bstart = ln
            elif inJ and c6!=' ':
                block.append(txt)
            elif inJ:
                refs.extend(_extract(block, bstart))
                inJ = False; block = []
        elif inJ and c6!=' ':
            block.append(line[9:80])
        elif inJ:
            refs.extend(_extract(block, bstart))
            inJ = False; block = []
    if inJ:
        refs.extend(_extract(block, bstart))
    return refs

def _extract(block, start):
    full = ' '.join(t.strip() for t in block)
    full = re.sub(r'\s+', ' ', full)
    pattern = re.compile(
        r'(?:^|\s|\|DJ=\d+\s*,?\s*)'  # optional |DJ=N prefix
        r'((?:E[0-9]|M[0-9]|D|Q|O|D\+Q|D\(\+Q\)|\(D\+Q\)|Q\+O|'
        r'M1\+E2|E1\+M2|M1\(\+E2\)|'
        r'\(D\)|\(Q\)|\(M1\)|\(E2\)|\(E1\)|\(M2\)|\[E2\]|\[M1\])'
        r'(?:\s*,\s*(?:MM)?)?)'
        r'\s+'
        r'(\d+(?:\.\d+)?)\|g(?:\(\|q\))?')
    results = []
    for m in pattern.finditer(full):
        mul = m.group(1).strip().rstrip(',').strip()
        ge = m.group(2)
        results.append({'ge': ge, 'mul': mul, 'line': start,
                        'ctx': full[max(0,m.start()-20):m.end()+30]})
    return results

def find_gamma(gammas, e_str):
    for g in gammas:
        if g['estr'] == e_str:
            return g
    return None

def check_selection_rules(jpi1, jpi2, m_field):
    """Check if multipolarity is consistent with ΔJ and Δπ between jpi1 and jpi2."""
    def parse_jpi(j):
        if not j: return None, None
        j = j.strip()
        pi = None
        if j.endswith('+'):
            pi = '+'; j = j[:-1]
        elif j.endswith('-'):
            pi = '-'; j = j[:-1]
        tent = j.startswith('(') and j.endswith(')')
        j = j.strip('()')
        try:
            if '/' in j:
                n,d = j.split('/')
                spin = float(n)/float(d)
            else:
                spin = float(j)
        except:
            return None, None
        return spin, pi  # tent ignored for now
    s1,p1 = parse_jpi(jpi1)
    s2,p2 = parse_jpi(jpi2)
    if s1 is None or s2 is None:
        return "unknown_J"
    dj = abs(s1 - s2)
    dp = (p1 != p2) if (p1 and p2) else None  # None if either parity unknown
    
    m = m_field.upper().replace('(','').replace(')','')
    # Map M field to allowed ΔJ ranges
    allowed = {
        'D': (0,1), 'D+Q': (0,1), 'D(+Q)': (0,1),
        'M1': (0,1), 'E1': (0,1),
        'M1+E2': (0,1), 'E1+M2': (0,1),
        'Q': (0,2), 'E2': (0,2), 'M2': (0,2),
        'Q+O': (2,2), 'M2+E3': (2,2), 'E2+M3': (2,2),
        '(M1)': (0,1), '(E2)': (0,2), '(E1)': (0,1), '(M2)': (0,2),
        'M1(+E2)': (0,1),
    }
    rng = allowed.get(m, None)
    if rng is None:
        return "unknown_M"
    lo, hi = rng
    if dj < lo or dj > hi:
        return f"ΔJ_violation(ΔJ={dj},M={m},range=[{lo},{hi}])"
    if dp is not None:
        # Check parity
        if m.startswith('E') and int(m[1]):
            L = int(m[1])
            expected_dp = (L % 2 == 1)
            if dp != expected_dp:
                return f"Δπ_violation(Δπ={dp},M={m},expect_Δπ={expected_dp})"
        elif m.startswith('M') and int(m[1]):
            L = int(m[1])
            expected_dp = (L % 2 == 0)
            if dp != expected_dp:
                return f"Δπ_violation(Δπ={dp},M={m},expect_Δπ={expected_dp})"
        elif m == 'D': pass  # D is ambiguous (E1 or M1)
        elif m == 'Q': pass  # Q is ambiguous
    return "OK"

def main():
    levels, gammas = parse_levels_and_gammas(fp)
    print(f"Levels: {len(levels)}, Gammas: {len(gammas)}")

    # ---- 1. G-records missing M field ----
    print("\n" + "="*70)
    print("1. G-RECORDS WITH EMPTY MULTIPOLARITY (M) FIELD")
    print("="*70)
    missing_M = []
    for g in gammas:
        if not g['m']:
            parent = g['parent']
            lvl = levels.get(parent, {})
            jpi = lvl.get('jpi', '?')
            missing_M.append((g['line'], g['estr'], parent, jpi))
    print(f"Found {len(missing_M)} G-records with empty M field:")
    for ln, e, p, j in missing_M[:30]:
        print(f"  L{ln}: G {e}  parent={p}  Jpi=({j})")

    # ---- 2. MULT quoted in J$ vs G-record M field ----
    print("\n" + "="*70)
    print("2. J$ QUOTED MULTIPOLARITY vs G-RECORD M FIELD")
    print("="*70)
    jrefs = parse_J_comments(fp)
    print(f"Extracted {len(jrefs)} J$ multipolarity references")
    mismatches = []
    for r in jrefs:
        g = find_gamma(gammas, r['ge'])
        if g:
            if g['m'] and g['m'] != r['mul']:
                mismatches.append((r['line'], r['ge'], r['mul'], g['m'], r['ctx']))
        elif not g:
            mismatches.append((r['line'], r['ge'], r['mul'], 'NOT_FOUND', r['ctx']))
    for ln, ge, cmul, gmul, ctx in mismatches:
        print(f"  L{ln}: {ge}|g  J$='{cmul}'  G='{gmul}'  ctx: {ctx}")

    # ---- 3. Selection rule violations ----
    print("\n" + "="*70)
    print("3. SELECTION RULE CHECKS (G Mult vs Level Jπ differences)")
    print("="*70)
    violations = []
    for g in gammas:
        if not g['m']: continue
        parent = g['parent']
        parent_lvl = levels.get(parent, {})
        parent_j = parent_lvl.get('jpi', '')
        # Compute expected final level energy = parent - gamma
        target_e = g['e']
        # Find closest level with parent minus gamma
        expected_final = float(parent) - target_e if parent else 0
        # Find closest L-record
        best = None; best_diff = 1e9
        for ek, lv in levels.items():
            d = abs(float(ek) - expected_final)
            if d < best_diff:
                best_diff = d; best = (ek, lv)
        if best and best_diff < 2.0:  # within 2 keV
            final_j = best[1]['jpi']
            if parent_j and final_j:
                result = check_selection_rules(parent_j, final_j, g['m'])
                if result != 'OK' and result not in ('unknown_J','unknown_M'):
                    violations.append((g['line'], g['estr'], g['m'],
                                       parent, parent_j, best[0], final_j, result))
    for v in violations:
        ln, ge, m, pe, pj, fe, fj, res = v
        print(f"  L{ln}: G {ge} {m}  {pe}({pj})→{fe}({fj})  {res}")

    if not mismatches and not violations:
        print("  No issues found.")

if __name__ == '__main__':
    main()
