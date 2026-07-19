"""
E-record field update: replace IB/DIB/IE/DIE/TI/DTI from Table III.
Reads ACTUAL working ENSDF file, modifies only 6 byte ranges per E-record.
Preserves ALL other content exactly.
"""
import re

ENSDF_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
T3_PATH    = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md'

# ── Parse Table III ──
def conv(v):
    if not v: return v
    return v.replace('\u00d7'+'10','E').replace('\u2212','-')

def parse(cell):
    cell = cell.strip()
    if not cell: return '', '', True
    m = re.match(r'^(.+?)\s*\((.+?)\)$', cell)
    if m: return conv(m.group(1).strip()), m.group(2).strip(), False
    return conv(cell), '', False

t3 = {}
with open(T3_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line: continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8: continue
        m = re.match(r'([\d.]+)', parts[1])
        if not m: continue
        key = round(float(m.group(1)))
        ibv,ibu,ibb = parse(parts[3])
        iev,ieu,ieb = parse(parts[4])
        itv,itu,itb = parse(parts[5])
        entry = {'ex': float(m.group(1)),
                 'ib':ibv,'ibu':ibu,'ibb':ibb,
                 'ie':iev,'ieu':ieu,'ieb':ieb,
                 'it':itv,'itu':itu,'itb':itb}
        if key not in t3: t3[key] = []
        t3[key].append(entry)

# ── Format helpers ──
def fmt_val(val, w):
    """Left-justify value in w-char field. Handle E-n overflow by shortening mantissa."""
    if val == '' or val is None: return ' '*w
    s = str(val)
    if len(s) <= w: return s.ljust(w)
    # Try shortening E-n mantissa
    em = re.match(r'^([+\-]?\d+\.?\d*)(E[+\-]\d+)$', s)
    if em:
        mant, exp = em.group(1), em.group(2)
        max_mant = w - len(exp)
        mv = float(mant)
        for dp in range(max_mant-1, -1, -1):
            short = str(int(round(mv))) if dp==0 else f'{mv:.{dp}f}'
            if len(short+exp) <= w: return (short+exp).ljust(w)
    return s[:w].ljust(w)

def fmt_unc(u, w):
    """Left-justify uncertainty in w-char field."""
    if u == '' or u is None: return ' '*w
    return str(u)[:w].ljust(w)

# ── Process ENSDF ──
with open(ENSDF_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cur_e_key = None
cur_e_val = None
modified = 0
new_lines = []

for line in lines:
    r = line.rstrip('\n\r')
    # Preserve trailing newline exactly
    nl = line[len(r):] if len(line) > len(r) else '\n'
    
    # Track level from L-record
    if len(r) >= 9 and r[5:7] == '  ' and r[7:8] == 'L':
        try:
            cur_e_val = float(r[9:19].strip())
            cur_e_key = round(cur_e_val)
        except:
            cur_e_val = None
            cur_e_key = None
    
    # Primary E-record (col 6 blank, col 7 space, col 8 = 'E')
    if len(r) >= 9 and r[5:7] == '  ' and r[7:8] == 'E' and cur_e_key is not None and cur_e_key in t3:
        entries = t3[cur_e_key]
        # Nearest-energy matching for collision resolution
        d = entries[0] if len(entries)==1 else min(entries, key=lambda e: abs(e['ex']-cur_e_val))
        
        # Build replacement fields (left-justified)
        ib  = fmt_val(d['ib'] if not d['ibb'] else '', 7)
        dib = fmt_unc(d['ibu'] if not d['ibb'] else '', 2)
        ie  = fmt_val(d['ie'] if not d['ieb'] else '', 8)
        die = fmt_unc(d['ieu'] if not d['ieb'] else '', 2)
        ti  = fmt_val(d['it'] if not d['itb'] else '', 10)
        dti = fmt_unc(d['itu'] if not d['itb'] else '', 2)
        
        # Reconstruct: replace only byte ranges 21:28, 28:30, 30:38, 38:40, 64:74, 74:76
        new_r = (r[:21] + ib + dib + ie + die + r[40:64] + ti + dti + r[76:])
        
        if new_r != r:
            new_lines.append(new_r + nl)
            modified += 1
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

print(f'Modified E-records: {modified}')

with open(ENSDF_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('File written.')
