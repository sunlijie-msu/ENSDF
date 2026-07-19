"""
Update ENSDF E-records with Table III data.
Replaces IB, DIB, IE, DIE, TI, DTI fields.
Preserves E, DE, LOGFT, DFT, C, UN, Q fields.
"""
import re, os

ENSDF_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
TABLE3_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md'

# ── Parse Table III ────────────────────────────────────────────
def parse_sci(val_str):
    """Convert '9.0×10−4' or '9.0E-4' to float. Handle various formats."""
    val_str = val_str.strip()
    # Already ENSDF format
    if 'E' in val_str.upper():
        try: return float(val_str)
        except: pass
    # Unicode ×10^ format
    val_str = val_str.replace('×10', 'E').replace('−', '-')
    try: return float(val_str)
    except: return None

def parse_val_unc(cell):
    """Parse '7.3 (15)' or '9.0×10−4 (7)' → (val_str_ensdf, unc_str, is_blank)."""
    cell = cell.strip()
    if not cell or cell == '':
        return '', '', True  # blank
    
    # Match: value (uncertainty)
    m = re.match(r'^(.+?)\s*\((.+?)\)$', cell)
    if not m:
        # No uncertainty? Just value
        return cell, '', False
    
    val_raw = m.group(1).strip()
    unc_raw = m.group(2).strip()
    
    # Handle scientific notation
    if '×10' in val_raw:
        val_raw_clean = val_raw.replace('×10', 'E').replace('−', '-')
    else:
        val_raw_clean = val_raw
    
    return val_raw_clean, unc_raw, False

t3_data = {}
with open(TABLE3_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8:
            continue
        # parts[1]=Ex, parts[2]=Jpi, parts[3]=Ibeta, parts[4]=Ieps, parts[5]=Itot, parts[6]=logft
        ex_raw = parts[1]
        ib_raw = parts[3] if len(parts) > 3 else ''
        ie_raw = parts[4] if len(parts) > 4 else ''
        it_raw = parts[5] if len(parts) > 5 else ''
        
        # Parse level energy
        ex_m = re.match(r'([\d.]+)', ex_raw)
        if not ex_m:
            continue
        ex_val = float(ex_m.group(1))
        key = round(ex_val)
        
        ib_val, ib_unc, ib_blank = parse_val_unc(ib_raw)
        ie_val, ie_unc, ie_blank = parse_val_unc(ie_raw)
        it_val, it_unc, it_blank = parse_val_unc(it_raw)
        
        t3_data[key] = {
            'ex_raw': ex_raw,
            'ib_val': ib_val, 'ib_unc': ib_unc, 'ib_blank': ib_blank,
            'ie_val': ie_val, 'ie_unc': ie_unc, 'ie_blank': ie_blank,
            'it_val': it_val, 'it_unc': it_unc, 'it_blank': it_blank,
        }

print(f"Table III entries parsed: {len(t3_data)}")

# ── Update ENSDF E-records ─────────────────────────────────────
with open(ENSDF_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track level energy for E-record matching
current_level = None
modified = 0
new_lines = []

for i, line in enumerate(lines):
    # Detect L-record (for level energy tracking)
    if len(line) >= 9 and line[5:6] == ' ' and line[6:7] == ' ' and line[7:8] == 'L':
        e_field = line[9:19].strip()
        if e_field:
            try:
                current_level = round(float(e_field))
            except:
                current_level = None
    
    # Detect primary E-record (no continuation: col 6=space, col 7=space, col 8='E')
    is_e_record = (len(line) >= 9 and line[5:6] == ' ' and 
                   line[6:7] == ' ' and line[7:8] == 'E')
    
    if is_e_record and current_level is not None and current_level in t3_data:
        d = t3_data[current_level]
        orig = line
        
        # Build new field strings
        # IB: cols 23-29, 7 chars, left-justified
        # DIB: cols 30-31, 2 chars
        # IE: cols 32-39, 8 chars, left-justified
        # DIE: cols 40-41, 2 chars
        # TI: cols 65-74, 10 chars, left-justified
        # DTI: cols 75-76, 2 chars
        
        def fmt_field(val, width):
            """Format value left-justified in field of given width."""
            if val == '' or val is None:
                return ' ' * width
            s = str(val)
            if len(s) > width:
                # Truncate if too long
                return s[:width]
            return s.ljust(width)
        
        def fmt_unc(unc, width):
            """Format uncertainty in field."""
            if unc == '' or unc is None:
                return ' ' * width
            s = str(unc)
            return s.ljust(width)[:width]
        
        ib_field = fmt_field(d['ib_val'] if not d['ib_blank'] else '', 7)
        dib_field = fmt_unc(d['ib_unc'] if not d['ib_blank'] else '', 2)
        ie_field = fmt_field(d['ie_val'] if not d['ie_blank'] else '', 8)
        die_field = fmt_unc(d['ie_unc'] if not d['ie_blank'] else '', 2)
        ti_field = fmt_field(d['it_val'] if not d['it_blank'] else '', 10)
        dti_field = fmt_unc(d['it_unc'] if not d['it_blank'] else '', 2)
        
        # Build new line: preserve parts outside IB-DIB-IE-DIE and TI-DTI
        # Line structure (0-indexed):
        # [0:22] = NUCID + CONT + SP + E + SP + DE + SP (everything before IB)
        # [22:29] = IB
        # [29:31] = DIB
        # [31:39] = IE
        # [39:41] = DIE
        # [41:64] = SP + LOGFT + DFT + SP (everything between DIE and TI)
        # [64:74] = TI
        # [74:76] = DTI
        # [76:80] = C + UN + Q
        
        prefix = line[:22]   # everything before IB
        middle = line[41:64]  # SP + LOGFT + DFT + SP (between DIE and TI)
        suffix = line[76:80]  # C + UN + Q (cols 77-80, 0-idx 76-79)
        
        new_line = (prefix + ib_field + dib_field + ie_field + die_field + 
                    middle + ti_field + dti_field + suffix)
        
        # Ensure exactly 80 chars
        new_line = new_line[:80].ljust(80)
        
        if new_line != orig.rstrip('\n\r'):
            new_lines.append(new_line + '\n')
            modified += 1
            print(f"  UPDATED L{round(current_level):>5d} keV: IB={d['ib_val']}, IE={d['ie_val']}, TI={d['it_val']}")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

# Write back
with open(ENSDF_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nE-records modified: {modified}")
print(f"Done.")
