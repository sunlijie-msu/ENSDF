"""
Rebuild ENSDF E-records from Table III data.
Builds complete 80-char lines from scratch using ENSDF field spec.
Only touches E-records (col 8='E', col 6=blank, col 7=blank).
Extracts E, DE, LOGFT, DFT, C, UN, Q from current ENSDF.
Gets IB, DIB, IE, DIE, TI, DTI from Table III.
"""
import re, os

ENSDF_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
TABLE3_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md'

# ── Helper: sci notation conversion ─────────────────────────────
def to_ensdf_sci(val_str):
    if not val_str: return val_str
    if 'E' in val_str.upper() and chr(0xd7) not in val_str: return val_str  # × = U+00D7
    return val_str.replace(chr(0xd7)+'10', 'E').replace('\u2212', '-').replace('\u00d7'+'10','E')

def parse_val_unc(cell):
    """Parse '7.3 (15)' or '4.438E-5' -> (val_ensdf, unc_str, is_blank)"""
    cell = cell.strip()
    if not cell: return '', '', True
    m = re.match(r'^(.+?)\s*\((.+?)\)$', cell)
    if m:
        val_raw = to_ensdf_sci(m.group(1).strip())
        unc_raw = m.group(2).strip()
        return val_raw, unc_raw, False
    return to_ensdf_sci(cell), '', False

# ── Parse Table III ────────────────────────────────────────────
t3 = {}
with open(TABLE3_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line: continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8: continue
        ex_raw = parts[1]; ib_raw = parts[3]; ie_raw = parts[4]; it_raw = parts[5]
        ex_m = re.match(r'([\d.]+)', ex_raw)
        if not ex_m: continue
        ex_val = float(ex_m.group(1))
        key = round(ex_val)
        ib_val, ib_unc, ib_blank = parse_val_unc(ib_raw)
        ie_val, ie_unc, ie_blank = parse_val_unc(ie_raw)
        it_val, it_unc, it_blank = parse_val_unc(it_raw)
        entry = {'ex_val': ex_val,
                 'ib_val': ib_val, 'ib_unc': ib_unc, 'ib_blank': ib_blank,
                 'ie_val': ie_val, 'ie_unc': ie_unc, 'ie_blank': ie_blank,
                 'it_val': it_val, 'it_unc': it_unc, 'it_blank': it_blank}
        if key not in t3: t3[key] = []
        t3[key].append(entry)

# ── Field formatting ───────────────────────────────────────────
def fmt_val(val, width):
    """Format value left-justified. For E-n overflow, shorten mantissa."""
    if val == '' or val is None: return ' ' * width
    s = str(val)
    if len(s) <= width: return s.ljust(width)
    # Try to shorten E-n mantissa
    em = re.match(r'^([+\-]?\d+\.?\d*)(E[+\-]\d+)$', s)
    if em:
        mantissa, exp = em.group(1), em.group(2)
        exp_len = len(exp)
        max_mant = width - exp_len
        if max_mant >= 1:
            mval = float(mantissa)
            for dp in range(max_mant - 1, -1, -1):
                if dp == 0: short = str(int(round(mval)))
                else: short = f'{mval:.{dp}f}'
                candidate = short + exp
                if len(candidate) <= width: return candidate.ljust(width)
    return s[:width].ljust(width)

def fmt_unc(unc, width):
    if unc == '' or unc is None: return ' ' * width
    return str(unc)[:width].ljust(width)

# ── Read ENSDF, rebuild E-records ──────────────────────────────
with open(ENSDF_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_e = None
modified = 0
new_lines = []

for i, line in enumerate(lines):
    # Track level energy
    if len(line) >= 9 and line[5:6] == ' ' and line[6:7] == ' ' and line[7:8] == 'L':
        e_field = line[9:19].strip()
        if e_field:
            try: current_e = float(e_field)
            except: current_e = None
    
    # Primary E-record
    is_primary_e = (len(line) >= 9 and line[5:6] == ' ' and 
                    line[6:7] == ' ' and line[7:8] == 'E')
    
    if is_primary_e and current_e is not None:
        key = round(current_e)
        
        if key in t3 and t3[key]:
            entries = t3[key]
            # Pick closest-energy entry
            if len(entries) == 1:
                d = entries[0]
            else:
                d = min(entries, key=lambda e: abs(e['ex_val'] - current_e))
            
            # Extract preserved fields from current line (cols from ENSDF spec)
            # E field: cols 10-19 (idx 9-18), 10 chars
            e_field = line[9:19]
            # DE field: cols 20-21 (idx 19-20), 2 chars
            de_field = line[19:21]
            # LOGFT: cols 43-49 (idx 42-48), 7 chars
            logft_field = line[42:49]
            # DFT: cols 50-55 (idx 49-54), 6 chars
            dft_field = line[49:55]
            # C: col 77 (idx 76), 1 char
            c_field = line[76:77] if len(line) > 76 else ' '
            # UN: cols 78-79 (idx 77-78), 2 chars
            un_field = line[77:79] if len(line) > 78 else '  '
            # Q: col 80 (idx 79), 1 char
            q_field = line[79:80] if len(line) > 79 else ' '
            
            # Build new IB/DIB/IE/DIE/TI/DTI fields
            ib_field = fmt_val(d['ib_val'] if not d['ib_blank'] else '', 7)
            dib_field = fmt_unc(d['ib_unc'] if not d['ib_blank'] else '', 2)
            ie_field = fmt_val(d['ie_val'] if not d['ie_blank'] else '', 8)
            die_field = fmt_unc(d['ie_unc'] if not d['ie_blank'] else '', 2)
            ti_field = fmt_val(d['it_val'] if not d['it_blank'] else '', 10)
            dti_field = fmt_unc(d['it_unc'] if not d['it_blank'] else '', 2)
            
            # Assemble complete 80-char line using exact ENSDF E-record spec
            # NUCID: cols 1-5 (idx 0-4)
            # CONT: col 6 (idx 5) = ' '
            # SPACE: col 7 (idx 6) = ' '
            # TYPE: col 8 (idx 7) = 'E'
            # SPACE: col 9 (idx 8) = ' '
            # E: cols 10-19 (idx 9-18) = e_field
            # DE: cols 20-21 (idx 19-20) = de_field
            # SPACE: col 22 (idx 21) = ' '
            # IB: cols 23-29 (idx 22-28) = ib_field
            # DIB: cols 30-31 (idx 29-30) = dib_field
            # IE: cols 32-39 (idx 31-38) = ie_field
            # DIE: cols 40-41 (idx 39-40) = die_field
            # SPACE: col 42 (idx 41) = ' '
            # LOGFT: cols 43-49 (idx 42-48) = logft_field
            # DFT: cols 50-55 (idx 49-54) = dft_field
            # SPACE: cols 56-64 (idx 55-63) = 9 spaces
            # TI: cols 65-74 (idx 64-73) = ti_field
            # DTI: cols 75-76 (idx 74-75) = dti_field
            # C: col 77 (idx 76) = c_field
            # UN: cols 78-79 (idx 77-78) = un_field
            # Q: col 80 (idx 79) = q_field
            
            nucid = line[:5]  # preserve NUCID exactly
            
            new_line = (nucid + ' ' + ' ' + 'E' + ' ' + 
                       e_field + de_field + ' ' +
                       ib_field + dib_field + ie_field + die_field + ' ' +
                       logft_field + dft_field + ' ' * 9 +
                       ti_field + dti_field + c_field + un_field + q_field)
            
            # Safety: ensure exactly 80 chars
            new_line = new_line[:80].ljust(80)
            
            old_line = line.rstrip('\n\r')
            if new_line != old_line:
                new_lines.append(new_line + '\n')
                modified += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

# Write
with open(ENSDF_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"E-records rebuilt: {modified} modified")
print("Done.")
