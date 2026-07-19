"""
Fix E-record column positions to ENSDF standard with readability spaces at cols 22, 42.
Rebuilds each E-record line preserving LOGFT/DFT from original, 
using Table III data for IB/DIB/IE/DIE/TI/DTI.
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
        # Col 6 = logft
        lft, lftu, lftb = parse(parts[6])
        ibv,ibu,ibb = parse(parts[3])
        iev,ieu,ieb = parse(parts[4])
        itv,itu,itb = parse(parts[5])
        entry = {'ex': float(m.group(1)),
                 'lft':lft,'lftu':lftu,'lftb':lftb,
                 'ib':ibv,'ibu':ibu,'ibb':ibb,
                 'ie':iev,'ieu':ieu,'ieb':ieb,
                 'it':itv,'itu':itu,'itb':itb}
        if key not in t3: t3[key] = []
        t3[key].append(entry)

# ── Format helpers ──
def fmt_val(val, w):
    if val == '' or val is None: return ' '*w
    s = str(val)
    if len(s) <= w: return s.ljust(w)
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
    if u == '' or u is None: return ' '*w
    return str(u)[:w].ljust(w)

# ── Process ──
with open(ENSDF_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cur_e_key = None
cur_e_val = None
modified = 0
new_lines = []

for line in lines:
    r = line.rstrip('\n\r')
    nl = line[len(r):] if len(line) > len(r) else '\n'
    
    # Track level
    if len(r) >= 9 and r[5:7] == '  ' and r[7:8] == 'L':
        try:
            cur_e_val = float(r[9:19].strip())
            cur_e_key = round(cur_e_val)
        except:
            cur_e_val = None
            cur_e_key = None
    
    # Primary E-record
    if len(r) >= 80 and r[5] == ' ' and r[6] == ' ' and r[7] == 'E' and cur_e_key is not None and cur_e_key in t3:
        entries = t3[cur_e_key]
        d = entries[0] if len(entries)==1 else min(entries, key=lambda e: abs(e['ex']-cur_e_val))
        
        # Extract LOGFT/DFT from current middle [40:64]
        mid = r[40:64]
        # Extract logft value from mid - it's at variable positions
        # Common patterns: ' 9.6     1              ' or ' 8.1                    '
        # Scan mid for the logft value (first non-space chars after pos 0)
        mid_stripped = mid.lstrip()
        # LOGFT is first token, DFT is second (or blank)
        tokens = mid_stripped.split()
        logft_val = tokens[0] if len(tokens) >= 1 else ''
        dft_val = tokens[1] if len(tokens) >= 2 else ''
        # Handle GT/LT markers (they're in DFT field, not LOGFT)
        if dft_val in ('GT','LT','LE','GE'):
            pass  # keep as is
        if logft_val in ('GT','LT','LE','GE'):
            # GT/LT at start means it's for LOGFT? Actually GT/LT should be in DFT
            # But some files have 'T' prefix... handle edge cases
            pass
        
        # Build standard-format line (1-indexed columns -> 0-indexed slices):
        # [0:9]   = cols 1-9: NUCID + CONT + SP + TYPE + SP
        # [9:19]  = cols 10-19: E
        # [19:21] = cols 20-21: DE
        # [21]    = col 22: readability space
        # [22:29] = cols 23-29: IB (7)
        # [29:31] = cols 30-31: DIB (2)
        # [31:39] = cols 32-39: IE (8)
        # [39:41] = cols 40-41: DIE (2)
        # [41]    = col 42: readability space
        # [42:49] = cols 43-49: LOGFT (7)
        # [49:55] = cols 50-55: DFT (6)
        # [55:64] = cols 56-64: spaces (9)
        # [64:74] = cols 65-74: TI (10)
        # [74:76] = cols 75-76: DTI (2)
        # [76:80] = cols 77-80: C + UN + Q
        
        prefix = r[0:9]
        e_val  = r[9:19]
        de_val = r[19:21]
        suffix = r[76:80]
        
        ib  = fmt_val(d['ib'] if not d['ibb'] else '', 7)
        dib = fmt_unc(d['ibu'] if not d['ibb'] else '', 2)
        ie  = fmt_val(d['ie'] if not d['ieb'] else '', 8)
        die = fmt_unc(d['ieu'] if not d['ieb'] else '', 2)
        ti  = fmt_val(d['it'] if not d['itb'] else '', 10)
        dti = fmt_unc(d['itu'] if not d['itb'] else '', 2)
        
        # LOGFT and DFT from Table III for consistency
        lft = fmt_val(d['lft'] if not d['lftb'] else '', 7)
        dft = fmt_unc(d['lftu'] if not d['lftb'] else '', 6)
        
        new_r = (prefix + e_val + de_val + ' ' + ib + dib + ie + die + ' ' +
                 lft + dft + ' '*9 + ti + dti + suffix)
        
        if len(new_r) != 80:
            print(f'ERROR: Line length {len(new_r)} for level {cur_e_val}')
            new_lines.append(line)
        else:
            new_lines.append(new_r + nl)
            if new_r != r:
                modified += 1
    else:
        new_lines.append(line)

print(f'Modified E-records: {modified}')

with open(ENSDF_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('File written.')
