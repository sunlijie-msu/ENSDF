"""
Inject angular correlation cG comments from Table IV into ENSDF file.
Matches on E1 (level, 2 keV tol) and Eg1 (gamma, 0.5 keV tol).
Skips cascades that already have |g|g(|q) comments.
"""
import re, sys

# ============================================================
# 1. Parse Table IV
# ============================================================
t4 = open('XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', encoding='utf-8').read().splitlines()
cascades = []
for line in t4:
    s = line.strip()
    if not s.startswith('|'): continue
    cells = [c.strip() for c in s.strip('|').split('|')]
    if len(cells) < 12: continue
    if cells[0].startswith('$E_1$'): continue
    if re.fullmatch(r'[-:\s]*', ''.join(cells)): continue
    cascades.append({
        'e1': cells[0], 'eg1': cells[1], 'eg2': cells[2],
        'a0': cells[3], 'a2': cells[4], 'a4': cells[5],
        'e2': cells[6], 'e3': cells[7],
        'j1': cells[8], 'j2': cells[9], 'j3': cells[10],
        'd1': cells[11]
    })
print(f"T4 cascades: {len(cascades)}")

# ============================================================
# 2. Parse value with uncertainty
# ============================================================
def parse_vu(s):
    """Return (value_str, unc_str_or_None, limit_str_or_None).
    Preserves exact decimal places from source string."""
    s = s.strip()
    if not s: return (None, None, None)
    if s.startswith('>'): 
        rest = s[1:].strip()
        return (rest, None, 'GT')
    if s.startswith('<'): 
        rest = s[1:].strip()
        return (rest, None, 'LT')
    m = re.match(r'([-\d\.]+)\s*\((\d+)\)', s)
    if m: return (m.group(1), m.group(2), None)
    m = re.match(r'([-\d\.]+)', s)
    if m: return (m.group(1), None, None)
    return (None, None, None)

# ============================================================
# 3. Build comment string
# ============================================================
def build_comment(eg1, eg2, a0, a2, a4, d1):
    parts = [f"${eg1}-{eg2} |g|g(|q)"]
    
    a_terms = []
    for label, vs in [('A{-0}', a0), ('A{-2}', a2), ('A{-4}', a4)]:
        v, u, lim = parse_vu(vs)
        if v is None: continue
        if u:
            a_terms.append(f"{label}={v} {{{'I'+u}}}")
        elif lim:
            a_terms.append(f"{label}{lim}{v}")
        else:
            a_terms.append(f"{label}={v}")
    
    if a_terms:
        parts.append(' ' + ', '.join(a_terms))
    
    if d1:
        v, u, lim = parse_vu(d1)
        if v is not None:
            # Ensure explicit sign: + for positive, - for negative
            if not v.startswith('-') and not v.startswith('+'):
                v_signed = '+' + v
            else:
                v_signed = v
            if lim == 'GT':
                parts.append(f", |d>{v_signed}")
            elif lim == 'LT':
                parts.append(f", |d<{v_signed}")
            elif u:
                parts.append(f", |d={v_signed} {{{'I'+u}}}")
            else:
                parts.append(f", |d={v_signed}")
    
    return ''.join(parts) + '.'

# ============================================================
# 4. Parse ENSDF — map levels→gammas
# ============================================================
ens_raw = open('XUNDL/2026OSAA_CT11035_152Gd.ens', encoding='utf-8').read().splitlines()

# Strip existing angular correlation cG comments (first pass)
ens = []
stripped = 0
for line in ens_raw:
    # Remove any cG or continuation cG containing |g|g(|q)
    if '|g|g(|q)' in line:
        # Check if it's a cG or 2cG etc. comment line
        s = line[0:9] if len(line) >= 9 else line
        if 'cG' in s:
            stripped += 1
            continue
    ens.append(line)
print(f"Stripped {stripped} existing |g|g(|q) comment lines")

levels = {}   # ei_float → [(eg_float, line_idx), ...]
cur_ei = None

for idx, line in enumerate(ens):
    if len(line) < 10: continue
    # Primary L-record: col6=' ', col7=' ', col8='L'
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'L':
        try: cur_ei = float(line[9:19].strip())
        except: cur_ei = None
        if cur_ei is not None and cur_ei not in levels:
            levels[cur_ei] = []
        continue
    # Primary G-record: col6=' ', col7=' ', col8='G'
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'G':
        if cur_ei is not None:
            try:
                eg = float(line[9:19].strip())
                levels[cur_ei].append((eg, idx))
            except: pass
        continue

print(f"ENSDF levels: {len(levels)}, total gammas: {sum(len(v) for v in levels.values())}")

# ============================================================
# 5. Match cascades
# ============================================================
def find_level(e1_str):
    try: e1f = float(e1_str)
    except: return None
    best, best_d = None, 999
    for lei in levels:
        d = abs(lei - e1f)
        if d < 2.0 and d < best_d:
            best, best_d = lei, d
    return best

def find_gamma(eg1_str, lei):
    try: egf = float(eg1_str)
    except: return None, None
    gammas = levels.get(lei, [])
    best, best_d = None, 999
    for eg, lidx in gammas:
        d = abs(eg - egf)
        if d < 1.5 and d < best_d:
            best, best_d = (eg, lidx), d
    return best

def find_gblock_end(g_idx):
    """Find last line of the G-record block (including continuation and cG lines)."""
    j = g_idx + 1
    while j < len(ens):
        line = ens[j]
        if len(line) < 10: break
        c6, c7, c8 = line[5], line[6], line[7]
        # Continuation G: col8='G', col6 is non-space alnum
        if c8 == 'G' and c6 != ' ' and c6.isalnum(): 
            j += 1; continue
        # Primary cG: col6=' ', col7='c', col8='G'
        if c6 == ' ' and c7 == 'c' and c8 == 'G':
            j += 1; continue
        # Continuation cG: col7='c', col8='G', col6 alnum
        if c7 == 'c' and c8 == 'G' and c6.isalnum():
            j += 1; continue
        break
    return j - 1

# Build insertions
insertions = {}  # after_line → comment_string
matched = 0; no_match = 0; skipped_existing = 0

for c in cascades:
    lei = find_level(c['e1'])
    if lei is None: 
        no_match += 1
        print(f"NO-LEVEL: E1={c['e1']}, Eg1={c['eg1']}, Eg2={c['eg2']}")
        continue
    
    result = find_gamma(c['eg1'], lei)
    if result is None: 
        no_match += 1
        print(f"NO-GAMMA: E1={c['e1']}(ENS={lei}), Eg1={c['eg1']}, Eg2={c['eg2']}")
        continue
    
    eg_float, g_idx = result
    ins_point = find_gblock_end(g_idx)
    
    # Check if |g|g(|q) already in block
    has_existing = any('|g|g(|q)' in ens[k] for k in range(g_idx, ins_point + 1))
    if has_existing:
        skipped_existing += 1; continue
    
    comment = build_comment(c['eg1'], c['eg2'], c['a0'], c['a2'], c['a4'], c['d1'])
    insertions[ins_point] = comment
    matched += 1

print(f"Matched: {matched}, No match: {no_match}, Skipped (existing): {skipped_existing}")

# ============================================================
# 6. Rebuild file with insertions
# ============================================================
insert_at = sorted(insertions.keys())
ins_ptr = 0
new_lines = []

for i, line in enumerate(ens):
    new_lines.append(line)
    while ins_ptr < len(insert_at) and insert_at[ins_ptr] == i:
        comment = insertions[insert_at[ins_ptr]]
        nucid = line[:5] if len(line) >= 5 else '152GD'
        # cG line: NUCID(5) + ' ' + 'c' + 'G' + ' ' + comment
        cg_line = f"{nucid} cG {comment}"
        new_lines.append(cg_line)
        ins_ptr += 1

with open('XUNDL/2026OSAA_CT11035_152Gd.ens', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines) + '\n')

print("Done writing ENSDF.")

# ============================================================
# 7. Spot-check 15% of newly added comments
# ============================================================
import random
random.seed(20260630125)
all_inserts = list(insertions.values())
n_sample = max(1, (15 * len(all_inserts) + 99) // 100)
sample = random.sample(all_inserts, min(n_sample, len(all_inserts)))
print(f"\n--- {len(sample)} spot-check samples ---")
for s in sample:
    print(s[:120])
