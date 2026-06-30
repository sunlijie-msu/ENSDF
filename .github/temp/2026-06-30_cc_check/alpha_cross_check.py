"""
Full alpha cross-check: Table I (source MD) vs ENSDF CC/DCC (target)
Follows data-cross-check SKILL.md procedure.
"""
import re, random, math, sys

# ============================================================
# 1. PARSE SOURCE: Table I (Markdown) — alpha column
# ============================================================
md = open('XUNDL/2026OSAA_CT11035_152Gd_Table_I.md', encoding='utf-8').read().splitlines()
src_rows = []

for line in md:
    s = line.strip()
    if not s.startswith('|'): continue
    cells = [c.strip() for c in s.strip('|').split('|')]
    if len(cells) < 9: continue
    if cells[0].startswith('$E_i$'): continue
    if re.fullmatch(r'[-:\s]*', ''.join(cells)): continue
    
    alpha_raw = cells[8]
    if not alpha_raw or alpha_raw == 'none' or alpha_raw == '': continue
    
    # Parse alpha value/uncertainty from LaTeX/mixed format
    a = alpha_raw
    
    # Remove $ signs
    a = a.replace('$','')
    # Handle LaTeX \times 10^{...} pattern FIRST
    # e.g., '8.59 \times 10^{-4}' -> '8.59E-4'
    a = re.sub(r'\s*\\times\s*10\s*\^\s*\{([\-\d]+)\}\s*', r'E\1', a)
    # Also handle unicode × and −
    a = a.replace('\u00d7','').replace('\u2212','-')
    # Remove stray backslashes
    a = a.replace('\\','')
    # Handle non-LaTeX '10^{-4}' or '10 -4' patterns
    a = re.sub(r'\s*10\s*\^\s*\{?([\-\d]+)\}?\s*', r'E\1', a)
    a = re.sub(r'\s*10\s*[-?]\s*(\d+)\s*', r'E-\1', a)
    # Collapse any double spaces
    a = re.sub(r'\s+', ' ', a).strip()
    
    m = re.match(r'([\d\.Ee\-\+]+)\s*\((\d+)\)', a)
    if m:
        alpha_val = m.group(1)
        alpha_unc = m.group(2)
    else:
        m = re.match(r'([\d\.Ee\-\+]+)', a)
        if m:
            alpha_val = m.group(1)
            alpha_unc = ''
        else:
            continue
    
    ei_match = re.match(r'([\d\.]+)', cells[0])
    eg_match = re.match(r'([\d\.]+)', cells[2])
    
    src_rows.append({
        'ei': ei_match.group(1) if ei_match else '',
        'eg': eg_match.group(1) if eg_match else '',
        'mult': cells[6],
        'alpha_val': alpha_val,
        'alpha_unc': alpha_unc,
        'alpha_raw': alpha_raw,
        'jpi': cells[1]
    })

print(f'Source (T1) rows with alpha: {len(src_rows)}')

# ============================================================
# 2. PARSE TARGET: ENSDF — CC/DCC fields
# ============================================================
ens = open('XUNDL/2026OSAA_CT11035_152Gd.ens', encoding='utf-8').read().splitlines()
tgt_gammas = []
cur_ei = None

for ln, line in enumerate(ens, 1):
    if len(line) < 10: continue
    c6, c7, c8 = line[5], line[6], line[7]
    
    if c6 == ' ' and c7 == ' ' and c8 == 'L':
        cur_ei = line[9:19].strip()
        continue
    
    if c6 == ' ' and c7 == ' ' and c8 == 'G':
        eg = line[9:19].strip()
        cc = line[55:62]   # cols 56-62
        dcc = line[62:64]  # cols 63-64
        mult = line[32:41].strip()
        tgt_gammas.append({
            'ei': cur_ei,
            'eg': eg,
            'cc': cc,
            'dcc': dcc,
            'mult': mult,
            'ln': ln
        })

print(f'Target (ENS) gammas total: {len(tgt_gammas)}')
print(f'Target (ENS) gammas with CC: {sum(1 for g in tgt_gammas if g["cc"].strip())}')

# ============================================================
# 3. UTILITY FUNCTIONS
# ============================================================
def match_ei(e1, e2):
    try: return abs(float(e1) - float(e2)) < 0.5
    except: return False

def match_eg(e1, e2):
    try: return abs(float(e1) - float(e2)) < 0.3
    except: return False

def nv(s):
    if not s or not s.strip(): return None
    try:
        ss = s.strip()
        if 'E' in ss or 'e' in ss:
            return float(ss.replace('E','e').replace('e','e'))
        return float(ss)
    except: return None

def count_decimals(s):
    s = s.strip()
    if 'E' in s or 'e' in s:
        m = re.match(r'([\d\.]+)[Ee]', s)
        if m: s = m.group(1)
    if '.' in s:
        return len(s.split('.')[1])
    return 0

def fmt_sci(s):
    return ('E' in s.upper() or 'e' in s)

# ============================================================
# 4. COMPARISON ENGINE
# ============================================================
def compare_cc(src, tgt):
    issues = []
    
    sv = src['alpha_val']
    su = src['alpha_unc']
    tv = tgt['cc'].strip()
    tu = tgt['dcc'].strip()
    
    if not sv and not tv: return ['BOTH_BLANK']
    if sv and not tv: return ['MISSING_IN_ENS']
    if not sv and tv: return ['EXTRA_IN_ENS']
    
    # Value comparison
    n_sv = nv(sv)
    n_tv = nv(tv)
    
    if n_sv is not None and n_tv is not None:
        if abs(n_tv) > 1e-30:
            rel_diff = abs(n_sv - n_tv) / abs(n_tv)
        else:
            rel_diff = abs(n_sv - n_tv)
        if rel_diff > 0.001:
            issues.append('VALUE: src={} tgt={} (rel_diff={:.2e})'.format(sv, tv, rel_diff))
    elif sv != tv:
        issues.append('VALUE_STR: src={} tgt={}'.format(sv, tv))
    
    # Uncertainty comparison
    if su and tu:
        if su != tu:
            issues.append('UNC: src={} tgt={}'.format(su, tu))
    elif su and not tu:
        issues.append('UNC_MISSING: src has unc={}, tgt blank'.format(su))
    elif not su and tu:
        issues.append('UNC_EXTRA: src no unc, tgt has unc={}'.format(tu))
    
    # Decimal places
    sv_dec = count_decimals(sv)
    tv_dec = count_decimals(tv)
    if sv_dec != tv_dec:
        issues.append('DEC_PLACES: src={}dp tgt={}dp (src={} tgt={})'.format(sv_dec, tv_dec, sv, tv))
    
    # Scientific notation consistency
    src_sci = fmt_sci(sv)
    tgt_sci = fmt_sci(tv)
    if src_sci != tgt_sci:
        issues.append('SCI_NOTATION: src_sci={} tgt_sci={}'.format(src_sci, tgt_sci))
    
    return issues if issues else ['MATCH']

# ============================================================
# 5. MAIN MATCHING LOOP
# ============================================================
report = []
spot_pool = []
val_mismatch = 0; unc_mismatch = 0; dec_mismatch = 0
sci_mismatch = 0; missing = 0; extra = 0; full_match = 0

for src in src_rows:
    tgt_level_matches = [g for g in tgt_gammas if match_ei(src['ei'], g['ei'])]
    tgt_matches = [g for g in tgt_level_matches if match_eg(src['eg'], g['eg'])]
    
    if not tgt_matches:
        report.append(('NO_MATCH', src, None, ['NO_ENS_MATCH']))
        missing += 1
        continue
    
    for tgt in tgt_matches:
        issues = compare_cc(src, tgt)
        
        if issues == ['MATCH']:
            full_match += 1
            status = 'MATCH'
        else:
            status = '; '.join(issues)
            for iss in issues:
                if iss.startswith('VALUE:'): val_mismatch += 1
                elif iss.startswith('UNC'): unc_mismatch += 1
                elif iss.startswith('DEC_PLACES'): dec_mismatch += 1
                elif iss.startswith('SCI'): sci_mismatch += 1
                elif 'MISSING' in iss: missing += 1
                elif 'EXTRA' in iss: extra += 1
        
        report.append((status, src, tgt, issues))
        spot_pool.append((src, tgt))

# Check for ENS CC entries with no matching source
src_pairs = set()
for src in src_rows:
    for g in tgt_gammas:
        if match_ei(src['ei'], g['ei']) and match_eg(src['eg'], g['eg']):
            src_pairs.add((g['ei'], g['eg']))

for g in tgt_gammas:
    cc = g['cc'].strip()
    if not cc: continue
    if (g['ei'], g['eg']) not in src_pairs:
        report.append(('EXTRA_ENS_ONLY', None, g, ['ENS_HAS_CC_NO_SRC']))
        extra += 1

# ============================================================
# 6. SUMMARY
# ============================================================
total_issues = val_mismatch + unc_mismatch + dec_mismatch + sci_mismatch + missing + extra
print('\n=== CROSS-CHECK SUMMARY ===')
print('Full MATCH: {}'.format(full_match))
print('Value mismatches: {}'.format(val_mismatch))
print('Uncertainty mismatches: {}'.format(unc_mismatch))
print('Decimal place mismatches: {}'.format(dec_mismatch))
print('Sci-notation mismatches: {}'.format(sci_mismatch))
print('Missing/Extra: {}/{}'.format(missing, extra))
print('Total issues: {}'.format(total_issues))

# ============================================================
# 7. DETAILED MISMATCH REPORT
# ============================================================
print('\n=== DETAILED MISMATCHES ===')
has_mismatch = False
for status, src, tgt, issues in report:
    if status == 'MATCH': continue
    has_mismatch = True
    if src:
        print('  Src: Ei={}, Eg={}, alpha={}'.format(src['ei'], src['eg'], src['alpha_raw']))
    if tgt:
        print('  Tgt: Ei={}, Eg={}, CC={}, DCC={}, Ln={}'.format(tgt['ei'], tgt['eg'], tgt['cc'].strip(), tgt['dcc'].strip(), tgt['ln']))
    print('  Issues: {}'.format(' | '.join(issues)))
    print()

if not has_mismatch:
    print('  None! All alpha values match perfectly between source and target.')

# ============================================================
# 8. 15% RANDOM SPOT-CHECK
# ============================================================
print('\n=== 15% RANDOM SPOT-CHECK ===')
random.seed(20260630150)
n_pool = len(spot_pool)
k = max(1, (15 * n_pool + 99) // 100)
if k < n_pool:
    sample = random.sample(spot_pool, k)
else:
    sample = spot_pool

spot_fails = 0
for src, tgt in sorted(sample, key=lambda x: float(x[0]['ei'])):
    issues = compare_cc(src, tgt)
    if issues != ['MATCH']:
        spot_fails += 1
        print('  FAIL: Ei={}, Eg={} -> {}'.format(src['ei'], src['eg'], ' | '.join(issues)))

print('Sample size: {}'.format(k))
print('Failures: {}'.format(spot_fails))
print('Seed: 20260630150')

if spot_fails == 0 and not has_mismatch:
    print('\n*** ALL CHECKS PASSED. Source alpha == Target CC/DCC. ***')
