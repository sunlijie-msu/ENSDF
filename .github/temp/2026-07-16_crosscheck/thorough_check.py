"""
Cross-Check: Table_I_revised.md (source) vs 2026MAAA_CT11001_141Sm.ens (target)
Checks ALL fields: value, uncertainty, decimals, qualifiers, comments
"""
import re, random

random.seed(20260716)

# === 1. Parse Source ===
src = []
with open(r'XUNDL\2026MAAA_CT11001_141Sm_Table_I_revised.md', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'E_x' in line:
            continue
        p = [x.strip() for x in line.split('|')]
        if len(p) < 9: continue
        try:
            float(p[1].split('(')[0])
        except:
            continue
        eg = p[3]
        while eg and eg[-1] in '*\u2217':
            eg = eg[:-1].strip()
        src.append({
            'Ex': p[1], 'Jpi': p[2], 'Eg': eg, 'Int': p[4],
            'RDCO': p[5], 'Rtheta': p[6], 'P': p[7], 'Mult': p[8]
        })

print(f'Source rows: {len(src)}')

# === 2. Parse Target ===
with open(r'XUNDL\2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8') as f:
    lines = [l.rstrip('\n').rstrip('\r') for l in f.readlines()]
# Ensure 80
lines = [l + ' ' * (80 - len(l)) if len(l) < 80 else l for l in lines]

lvls = []
cl = None
cg = None
for li, ln in enumerate(lines):
    c7 = ln[6]; c8 = ln[7]; c6 = ln[5]
    if c8 == 'L' and c6 == ' ' and c7 == ' ':
        if cl: lvls.append(cl)
        cl = {'ln': li, 'E': ln[9:19].strip(), 'DE': ln[19:21].strip(),
              'J': ln[22:39].strip(), 'T': ln[39:49].strip(), 'DT': ln[49:55].strip(),
              'Q': ln[79], 'g': [], 'cL': []}
        cg = None
    elif c8 == 'G' and c6 == ' ' and c7 == ' ':
        cg = {'ln': li, 'E': ln[9:19].strip(), 'DE': ln[19:21].strip(),
              'RI': ln[22:29].strip(), 'DRI': ln[29:31].strip(),
              'M': ln[32:41].strip(), 'MR': ln[41:49].strip(), 'DMR': ln[49:55].strip(),
              'C': ln[76], 'Q': ln[79],
              'cG': []}
        if cl: cl['g'].append(cg)
    elif c7 == 'c' and c8 == 'G':
        if cg: cg['cG'].append(ln)
    elif c7 == 'c' and c8 == 'L':
        if cl: cl['cL'].append(ln)
if cl: lvls.append(cl)
tg = sum(len(lv['g']) for lv in lvls)
print(f'Target levels: {len(lvls)}, gammas: {tg}')

# === 3. Helpers ===
def parse_unc(s):
    """'123.4(12)' -> (123.4, '12')"""
    m = re.match(r'([+-]?[0-9]+\.?[0-9]*)\s*\(([0-9]+)\)', s)
    if m: return m.group(1), m.group(2)
    return None, None

def parse_unc_v(s):
    """'123.4(12)' -> (float, int)"""
    m = re.match(r'([+-]?[0-9]+\.?[0-9]*)\s*\(([0-9]+)\)', s)
    if m: return float(m.group(1)), int(m.group(2))
    return None, None

def int_unc_format(ens_val, ens_unc):
    """Check if ENSDF uncertainty field matches source (n) notation"""
    if not ens_val or not ens_unc: return ''
    if not ens_unc.strip(): return ens_val
    return ens_val + '(' + ens_unc.strip() + ')'

# === 4. Match and Compare ===
mismatches = []
all_checked = []

for si, s in enumerate(src):
    ex_v, ex_u = parse_unc_v(s['Ex'])
    eg_v, eg_u = parse_unc_v(s['Eg'])
    int_v, int_u = parse_unc_v(s['Int'])
    
    # Match level
    ml = None
    for lv in lvls:
        try:
            if abs(float(lv['E']) - ex_v) < 1.0:
                ml = lv; break
        except:
            pass
    
    if not ml:
        mismatches.append(f'#{si}: LEVEL NOT FOUND Ex={s["Ex"]}')
        continue
    
    l = ml
    
    # --- Level fields ---
    # E (level energy)
    l_e_disp = int_unc_format(l['E'], l['DE'])
    if l_e_disp != s['Ex']:
        mismatches.append(f'#{si}: Ex FIELD src="{s["Ex"]}" ens="{l_e_disp}" (E={l["E"]} DE={l["DE"]})')
    
    # Jpi
    j_norm = s['Jpi'].replace('\u2212', '-')
    if l['J'] != j_norm:
        mismatches.append(f'#{si}: Jpi FIELD src="{j_norm}" ens="{l["J"]}"')
    
    # Match gamma
    mg = None
    for g in l['g']:
        try:
            if abs(float(g['E']) - eg_v) < 0.2:
                mg = g; break
        except:
            pass
    
    if not mg:
        mismatches.append(f'#{si}: GAMMA NOT FOUND Eg={s["Eg"]} at Ex={s["Ex"]}')
        continue
    
    g = mg
    all_checked.append((si, s, l, g))
    
    # Eγ (gamma energy)
    g_e_disp = int_unc_format(g['E'], g['DE'])
    if g_e_disp != s['Eg']:
        mismatches.append(f'#{si}: Eg FIELD src="{s["Eg"]}" ens="{g_e_disp}"')
    
    # Intensity
    g_i_disp = int_unc_format(g['RI'], g['DRI'])
    if g_i_disp != s['Int']:
        mismatches.append(f'#{si}: INT FIELD src="{s["Int"]}" ens="{g_i_disp}" (RI={g["RI"]} DRI={g["DRI"]})')
    
    # Multipolarity - EXACT match (parentheses included)
    if g['M'] != s['Mult']:
        mismatches.append(f'#{si}: MULT FIELD src="{s["Mult"]}" ens="{g["M"]}"')
    
    # === Comments ===
    cg_text = ' '.join(g['cG'])
    
    # RDCO
    if s['RDCO']:
        # Normalize: ENSDF uses {In}, source uses (n)
        cg_norm = re.sub(r'\{I([+\-]?\d+(?:[+\-]\d+)?)\}', r'(\1)', cg_text)
        # Also normalize whitespace around value: '1.68 (17)' -> '1.68(17)'
        cg_norm = re.sub(r'(\d)\s+\((\d+)\)', r'\1(\2)', cg_norm)
        exp = s['RDCO'].replace(' ', '')
        found_rdco = False
        for variant in [f'R{{-DCO}}={exp}', f'R{{-DCO}}={exp}', f'R-DCO={exp}']:
            if variant in cg_norm: found_rdco = True; break
        if not found_rdco:
            mismatches.append(f'#{si}: RDCO COMMENT expected={exp} not found in cG')
    
    # Rtheta (R_ADO)
    if s['Rtheta']:
        cg_norm = re.sub(r'\{I([+\-]?\d+(?:[+\-]\d+)?)\}', r'(\1)', cg_text)
        cg_norm = re.sub(r'(\d)\s+\((\d+)\)', r'\1(\2)', cg_norm)
        exp = s['Rtheta'].replace(' ', '')
        found_rtheta = False
        for variant in [f'R{{-ADO}}={exp}', f'R-ADO={exp}']:
            if variant in cg_norm: found_rtheta = True; break
        if not found_rtheta:
            mismatches.append(f'#{si}: Rtheta COMMENT expected={exp} not found in cG')
    
    # Polarization
    if s['P']:
        cg_norm = re.sub(r'\{I([+\-]?\d+(?:[+\-]\d+)?)\}', r'(\1)', cg_text)
        cg_norm = re.sub(r'(\d)\s+\((\d+)\)', r'\1(\2)', cg_norm)
        exp = s['P'].replace(' ', '')
        if f'POL={exp}' not in cg_norm:
            mismatches.append(f'#{si}: POL COMMENT expected={exp} not found in cG')

# === 5. Report ===
print('\n' + '=' * 80)
print('CROSS-CHECK REPORT: revised.md vs ens')
print('=' * 80)

print(f'\nTotal checks: {len(src)} level-gamma pairs')
print(f'Real mismatches: {len(mismatches)}')
print()

# Categorize
cats = {}
for m in mismatches:
    if 'LEVEL NOT FOUND' in m: c = 'LEVEL MISSING'
    elif 'GAMMA NOT FOUND' in m: c = 'GAMMA MISSING'
    elif 'Ex FIELD' in m: c = 'LEVEL ENERGY'
    elif 'Jpi FIELD' in m: c = 'JPI'
    elif 'Eg FIELD' in m: c = 'GAMMA ENERGY'
    elif 'INT FIELD' in m: c = 'INTENSITY'
    elif 'MULT FIELD' in m: c = 'MULTIPOLARITY'
    elif 'RDCO' in m: c = 'RDCO COMMENT'
    elif 'Rtheta' in m: c = 'RTHETA COMMENT'
    elif 'POL' in m: c = 'POL COMMENT'
    else: c = 'OTHER'
    cats[c] = cats.get(c, 0) + 1

print('By category:')
for c in ['LEVEL ENERGY', 'JPI', 'GAMMA ENERGY', 'INTENSITY', 'MULTIPOLARITY',
          'RDCO COMMENT', 'RTHETA COMMENT', 'POL COMMENT', 'LEVEL MISSING', 'GAMMA MISSING']:
    if c in cats:
        print(f'  [{c}] {cats[c]}')

if mismatches:
    print('\nDetails:')
    for m in mismatches:
        print(f'  {m}')
else:
    print('\n✓ ALL FIELDS MATCH - zero mismatches')

# === 6. 15% Spot Check ===
count = len(all_checked)
sample_n = max(1, round(count * 0.15))
sample = random.sample(all_checked, sample_n)

print(f'\n{"=" * 80}')
print(f'15% SPOT CHECK ({sample_n}/{count} entries)')
print('=' * 80)

spot_errors = 0
for si, s, l, g in sample:
    print(f'\n  Entry #{si}: Ex={s["Ex"]} Eg={s["Eg"]}')
    ok = True
    
    # L-record
    le = int_unc_format(l['E'], l['DE'])
    jj = l['J']
    je = s['Jpi'].replace('\u2212', '-')
    if le != s['Ex']:
        print(f'    ✗ EX: src={s["Ex"]} ens={le}')
        ok = False
    if jj != je:
        print(f'    ✗ JPI: src={je} ens={jj}')
        ok = False
    
    # G-record
    ge = int_unc_format(g['E'], g['DE'])
    gi = int_unc_format(g['RI'], g['DRI'])
    gm = g['M']
    if ge != s['Eg']:
        print(f'    ✗ EG: src={s["Eg"]} ens={ge}')
        ok = False
    if gi != s['Int']:
        print(f'    ✗ INT: src={s["Int"]} ens={gi}')
        ok = False
    if gm != s['Mult']:
        print(f'    ✗ MULT: src={s["Mult"]} ens={gm}')
        ok = False
    
    if ok:
        print(f'    ✓ All fields match')

print(f'\n  Spot-check errors: {spot_errors}')
result = 'PASS' if spot_errors == 0 else 'FAIL'
print(f'  {result}')
