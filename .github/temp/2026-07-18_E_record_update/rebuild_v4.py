"""
Rebuild ENSDF E-records v4 - correct field layout.
Extracts: NUCID, E, DE, middle(LOGFT+DFT+spaces), suffix(C+UN+Q) from git original.
Replaces: IB, DIB, IE, DIE, TI, DTI from Table III.
Original format: NO readability spaces at cols 22, 32, 42.
Layout: NUCID(5)+CONT(1)+SP(1)+E(1)+SP(1)+E(10)+DE(2)+IB(7)+DIB(2)+IE(8)+DIE(2)+middle(24)+TI(10)+DTI(2)+suffix(4) = 80
"""
import re, subprocess, os

ENSDF_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
TABLE3_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md'

# ── Get original from git ─────────────────────────────────────
os.chdir('d:/X/ND/ENSDF/XUNDL')
result = subprocess.run(['git', 'show', '455d971:2026OSAA_CT11035_152Gd.ens'],
                       capture_output=True, text=True)
orig_lines = result.stdout.split('\n')

orig_e = {}
cur_e = None
for line in orig_lines:
    if len(line) >= 9 and line[5:7] == '  ' and line[7:8] == 'L':
        try: cur_e = round(float(line[9:19].strip()))
        except: cur_e = None
    if len(line) >= 9 and line[5:7] == '  ' and line[7:8] == 'E' and cur_e is not None:
        nucid  = line[:5]
        e_f    = line[9:19]   if len(line) > 18 else ' '*10
        de_f   = line[19:21]  if len(line) > 20 else '  '
        middle = line[40:64]  if len(line) > 63 else ' '*24
        suffix = line[76:80]  if len(line) > 79 else '    '
        orig_e[cur_e] = {'nucid': nucid, 'e_field': e_f, 'de_field': de_f,
                         'middle': middle, 'suffix': suffix}

print(f"Original E-records: {len(orig_e)}")

# ── Parse Table III ────────────────────────────────────────────
def to_sci(v):
    if not v: return v
    return v.replace('\u00d7'+'10','E').replace('\u2212','-')

def parse_cell(cell):
    cell = cell.strip()
    if not cell: return '', '', True
    m = re.match(r'^(.+?)\s*\((.+?)\)$', cell)
    if m: return to_sci(m.group(1).strip()), m.group(2).strip(), False
    return to_sci(cell), '', False

t3 = {}
with open(TABLE3_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line: continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8: continue
        m = re.match(r'([\d.]+)', parts[1])
        if not m: continue
        key = round(float(m.group(1)))
        ibv, ibu, ibb = parse_cell(parts[3])
        iev, ieu, ieb = parse_cell(parts[4])
        itv, itu, itb = parse_cell(parts[5])
        entry = {'ex_val': float(m.group(1)),
                 'ib_val': ibv, 'ib_unc': ibu, 'ib_blank': ibb,
                 'ie_val': iev, 'ie_unc': ieu, 'ie_blank': ieb,
                 'it_val': itv, 'it_unc': itu, 'it_blank': itb}
        if key not in t3: t3[key] = []
        t3[key].append(entry)

print(f"Table III entries: {sum(len(v) for v in t3.values())}")

# ── Field formatting ───────────────────────────────────────────
def fmt_val(val, width):
    if val == '' or val is None: return ' '*width
    s = str(val)
    if len(s) <= width: return s.ljust(width)
    em = re.match(r'^([+\-]?\d+\.?\d*)(E[+\-]\d+)$', s)
    if em:
        mantissa, exp = em.group(1), em.group(2)
        max_mant = width - len(exp)
        mval = float(mantissa)
        for dp in range(max_mant-1, -1, -1):
            short = str(int(round(mval))) if dp==0 else f'{mval:.{dp}f}'
            candidate = short + exp
            if len(candidate) <= width: return candidate.ljust(width)
    return s[:width].ljust(width)

def fmt_unc(unc, width):
    if unc == '' or unc is None: return ' '*width
    return str(unc)[:width].ljust(width)

# ── Rebuild ────────────────────────────────────────────────────
with open(ENSDF_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_e = None
modified = 0
new_lines = []

for i, line in enumerate(lines):
    if len(line) >= 9 and line[5:7] == '  ' and line[7:8] == 'L':
        try: current_e = round(float(line[9:19].strip()))
        except: current_e = None
    
    is_e = len(line) >= 9 and line[5:7] == '  ' and line[7:8] == 'E'
    
    if is_e and current_e is not None and current_e in orig_e and current_e in t3:
        entries = t3[current_e]
        d = entries[0] if len(entries)==1 else min(entries, key=lambda e: abs(e['ex_val']-current_e))
        og = orig_e[current_e]
        
        ib_field  = fmt_val(d['ib_val'] if not d['ib_blank'] else '', 7)
        dib_field = fmt_unc(d['ib_unc'] if not d['ib_blank'] else '', 2)
        ie_field  = fmt_val(d['ie_val'] if not d['ie_blank'] else '', 8)
        die_field = fmt_unc(d['ie_unc'] if not d['ie_blank'] else '', 2)
        ti_field  = fmt_val(d['it_val'] if not d['it_blank'] else '', 10)
        dti_field = fmt_unc(d['it_unc'] if not d['it_blank'] else '', 2)
        
        new_line = (og['nucid'] + '  ' + 'E' + ' ' +
                   og['e_field'] + og['de_field'] +
                   ib_field + dib_field + ie_field + die_field +
                   og['middle'] + ti_field + dti_field + og['suffix'])
        
        new_line = new_line[:80].ljust(80)
        
        if new_line != line.rstrip('\n\r'):
            new_lines.append(new_line + '\n')
            modified += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(ENSDF_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Rebuilt: {modified} E-records")
