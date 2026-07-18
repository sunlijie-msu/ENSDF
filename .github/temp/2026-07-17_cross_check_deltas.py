"""
Comprehensive mixing ratio audit: Table I, Table IV, ENSDF MR field, ENSDF cG |d=.
v3 - fixed regex for decimal values.
"""
import re

def parse_table_I(path):
    results = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|') or 'none' in line or '---' in line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 11: continue
            ei = parts[1]; eg = parts[3]; ef = parts[5]; delta = parts[8]
            if not delta: continue
            ei_v = ei.split('(')[0].strip()
            eg_v = eg.split('(')[0].strip()
            ef_v = ef.split('(')[0].strip()
            results[(ei_v, eg_v, ef_v)] = delta
    return results

def parse_table_IV(path):
    results = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|') or '---' in line or 'TABLE' in line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 14: continue
            e1 = parts[1]; eg1 = parts[2]; eg2 = parts[3]; delta = parts[12]
            results[(e1, eg1, eg2)] = delta if delta else ''
    return results

def extract_ensdf(filepath):
    """Returns mr_vals: {(lev, gam): mr_str}, cg_deltas: {(lev, gam): delta_str}"""
    mr_vals = {}
    cg_deltas = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    current_level = None
    i = 0
    while i < len(lines):
        line = lines[i]
        if len(line) >= 9 and line[7:8] == 'L' and line[5:6] == ' ':
            e_field = line[9:19].strip()
            if e_field:
                try: current_level = float(e_field)
                except: pass
        if len(line) >= 9 and line[7:8] == 'G' and line[5:6] == ' ':
            g_e = line[9:19].strip()
            mr_field = line[41:49].strip() if len(line) > 41 else ''
            if g_e and current_level is not None:
                try:
                    ge = float(g_e)
                    if mr_field: mr_vals[(current_level, ge)] = mr_field
                except: pass
            j = i + 1
            while j < len(lines):
                nl = lines[j]
                is_cg = (len(nl) >= 9 and nl[6:7] == 'c' and
                        nl[7:8] == 'G' and nl[5:6] in ' 123')
                if is_cg:
                    # Match |d=VALUE {IUNC} - value can include +, -, ., digits
                    dm = re.search(r'\|d=([^ }]+)\s*\{I(\d+)\}', nl)
                    if dm:
                        cg_deltas[(current_level, ge)] = f"{dm.group(1)}({dm.group(2)})"
                    dg = re.search(r'\|d>([^ }]+)', nl)
                    if dg:
                        cg_deltas[(current_level, ge)] = f">{dg.group(1)}"
                    j += 1
                else:
                    break
        i += 1
    return mr_vals, cg_deltas

def parse_d(d_str):
    """Returns (val, unc_str, is_gt, dp) or (None,None,False,0)"""
    d_str = d_str.strip()
    if not d_str: return None, None, False, 0
    is_gt = d_str.startswith('>')
    if is_gt: d_str = d_str[1:].strip()
    m = re.match(r'^([+\-]?\d+\.?\d*)\s*\((\d+)\)$', d_str)
    if m:
        val = float(m.group(1)); unc = m.group(2)
        dp = len(m.group(1).split('.')[1]) if '.' in m.group(1) else 0
        return val, unc, is_gt, dp
    m = re.match(r'^([+\-]?\d+\.?\d*)\s*\{I(\d+)\}', d_str)
    if m:
        val = float(m.group(1)); unc = m.group(2)
        dp = len(m.group(1).split('.')[1]) if '.' in m.group(1) else 0
        return val, unc, is_gt, dp
    return None, None, is_gt, 0

def nlev(e):
    try: return round(float(e))
    except: return None

def ngam(e):
    try: return round(float(e))
    except: return None

# --- MAIN ---
ensdf_path = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
t1_path = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_I.md'
t4_path = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md'

t1 = parse_table_I(t1_path)
t4 = parse_table_IV(t4_path)
mr, cgd = extract_ensdf(ensdf_path)

print(f"Table I deltas: {len(t1)}")
print(f"Table IV deltas: {len(t4)}")
print(f"ENSDF MR fields (mixing ratios): {len(mr)}")
print(f"ENSDF cG |d= values: {len(cgd)}")

# CHECK 1: Table I vs ENSDF MR field
print("\n" + "="*70)
print("CHECK 1: Table I delta vs ENSDF MR field")
print("="*70)
issues1 = 0
for (ei, eg, ef), t1d in sorted(t1.items()):
    ekey = (nlev(ei), ngam(eg))
    if None in ekey: continue
    ekey2 = (float(ei.split('(')[0]), float(eg.split('(')[0]))
    if ekey2 in mr:
        tv, tu, tgt, tdp = parse_d(t1d)
        try: mrv = float(mr[ekey2])
        except: mrv = None
        if tv is not None and mrv is not None and not tgt:
            if abs(tv - mrv) > 0.02:
                print(f"  MISMATCH L={ei} g={eg} T1={t1d} MR={mr[ekey2]}")
                issues1 += 1
    elif ekey in mr:
        tv, tu, tgt, tdp = parse_d(t1d)
        try: mrv = float(mr[ekey])
        except: mrv = None
        if tv is not None and mrv is not None and not tgt:
            if abs(tv - mrv) > 0.02:
                print(f"  MISMATCH L={ei} g={eg} T1={t1d} MR={mr[ekey]}")
                issues1 += 1
    else:
        if not t1d.startswith('>'):
            print(f"  T1 delta NO MR field: L={ei} g={eg} T1={t1d}")
if issues1 == 0: print("  All matched OK.")
else: print(f"  {issues1} issues.")

# CHECK 2: Table I vs cG
print("\n" + "="*70)
print("CHECK 2: Table I delta vs ENSDF cG |d=")
print("="*70)
issues2 = 0
for (ei, eg, ef), t1d in sorted(t1.items()):
    ekey = (nlev(ei), ngam(eg))
    if None in ekey: continue
    if ekey in cgd:
        tv, tu, tgt, tdp = parse_d(t1d)
        cv, cu, cgt, cdp = parse_d(cgd[ekey])
        if tv is not None and cv is not None:
            if tgt != cgt:
                print(f"  GT MISMATCH L={ei} g={eg} T1={t1d} cG={cgd[ekey]}")
                issues2 += 1
            elif not tgt and abs(tv - cv) > 0.02:
                print(f"  VAL MISMATCH L={ei} g={eg} T1={t1d} cG={cgd[ekey]}")
                issues2 += 1
    else:
        print(f"  T1 delta NO cG |d=: L={ei} g={eg} T1={t1d}")
        issues2 += 1
print(f"  {issues2} issues.")

# CHECK 3: Table IV vs cG
print("\n" + "="*70)
print("CHECK 3: Table IV delta_1 vs ENSDF cG |d=")
print("="*70)
issues3 = 0; matched = 0
for (e1, eg1, eg2), t4d in sorted(t4.items()):
    ekey = (nlev(e1), ngam(eg1))
    if None in ekey: continue
    if ekey in cgd:
        matched += 1
        if t4d:
            tv, tu, tgt, tdp = parse_d(t4d)
            cv, cu, cgt, cdp = parse_d(cgd[ekey])
            if tv is not None and cv is not None:
                if tgt != cgt:
                    print(f"  GT MISMATCH L={e1} g={eg1}-{eg2} T4={t4d} cG={cgd[ekey]}")
                    issues3 += 1
                elif not tgt:
                    if abs(tv - cv) > 0.02:
                        print(f"  VAL MISMATCH L={e1} g={eg1}-{eg2} T4={t4d} cG={cgd[ekey]}")
                        issues3 += 1
                    if tdp != cdp:
                        print(f"  DP MISMATCH L={e1} g={eg1}-{eg2} T4={t4d}({tdp}dp) cG={cgd[ekey]}({cdp}dp)")
                        issues3 += 1
    else:
        if t4d:
            print(f"  NO cG |d=: L={e1} g={eg1}-{eg2} T4={t4d}")
            issues3 += 1
print(f"  Matched: {matched}, Issues: {issues3}")

# CHECK 4: Table I vs Table IV
print("\n" + "="*70)
print("CHECK 4: Table I delta vs Table IV delta_1 (same cascade)")
print("="*70)
issues4 = 0
for (ei, eg, ef), t1d in sorted(t1.items()):
    ei_n = nlev(ei); eg_n = ngam(eg)
    if ei_n is None or eg_n is None: continue
    for (e1, eg1, eg2), t4d in t4.items():
        if nlev(e1) == ei_n and ngam(eg1) == eg_n:
            if t1d and t4d:
                tv, tu, tgt, tdp = parse_d(t1d)
                fv, fu, fgt, fdp = parse_d(t4d)
                if tv is not None and fv is not None:
                    if tgt != fgt:
                        print(f"  GT MISMATCH L={ei} g={eg} T1={t1d} T4={t4d}")
                        issues4 += 1
                    elif not tgt and abs(tv - fv) > 0.01:
                        print(f"  VAL MISMATCH L={ei} g={eg} T1={t1d} T4={t4d}")
                        issues4 += 1
            break
print(f"  {issues4} issues.")

# CHECK 5: MR field with cG |d= (should agree)
print("\n" + "="*70)
print("CHECK 5: MR field vs cG |d= consistency (both present)")
print("="*70)
issues5 = 0
for (lev, gam), mrv in sorted(mr.items()):
    rlev = round(lev); rgam = round(gam)
    if (rlev, rgam) in cgd:
        try: mr_float = float(mrv)
        except: mr_float = None
        cv, cu, cgt, cdp = parse_d(cgd[(rlev, rgam)])
        if mr_float is not None and cv is not None and not cgt:
            if abs(mr_float - cv) > 0.02:
                print(f"  MISMATCH L={rlev} g={rgam} MR={mrv} cG={cgd[(rlev,rgam)]}")
                issues5 += 1
    else:
        print(f"  MR={mrv} at L={rlev} g={rgam} -- NO cG |d=")
print(f"  {issues5} issues.")

# CHECK 6: MR fields that appear in Table I
print("\n" + "="*70)
print("CHECK 6: MR field values vs Table I (source verification)")
print("="*70)
for (lev, gam), mrv in sorted(mr.items()):
    rlev = round(lev); rgam = round(gam)
    found = False
    for (ei, eg, ef), t1d in t1.items():
        if nlev(ei) == rlev and ngam(eg) == rgam:
            tv, tu, tgt, tdp = parse_d(t1d)
            try: mr_float = float(mrv)
            except: mr_float = None
            if mr_float is not None and tv is not None and not tgt:
                if abs(mr_float - tv) > 0.005:
                    print(f"  MR vs T1 MISMATCH: L={rlev} g={rgam} MR={mrv} T1={t1d}")
            found = True; break
    if not found:
        print(f"  MR NO T1: L={rlev} g={rgam} MR={mrv}")

# SUMMARY
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
total = issues1 + issues2 + issues3 + issues4 + issues5
print(f"  Table I: {len(t1)} deltas")
print(f"  Table IV: {len(t4)} deltas")
print(f"  ENSDF MR fields: {len(mr)}")
print(f"  ENSDF cG |d=: {len(cgd)}")
print(f"  Check1 (T1 vs MR): {issues1}")
print(f"  Check2 (T1 vs cG): {issues2}")
print(f"  Check3 (T4 vs cG): {issues3}")
print(f"  Check4 (T1 vs T4): {issues4}")
print(f"  Check5 (MR vs cG): {issues5}")
print(f"  TOTAL ISSUES: {total}")
