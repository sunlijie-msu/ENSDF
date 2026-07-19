"""
Update ENSDF E-records with Table III data. v2 - fixes sci notation + 3272 collision.
"""
import re, os

ENSDF_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
TABLE3_PATH = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md'

def to_ensdf_sci(val_str):
    """Convert all scientific notation to ENSDF E-format. E.g. '4.438×10−5' → '4.438E-5'"""
    if not val_str:
        return val_str
    # Already in E format
    if 'E' in val_str.upper() and '×' not in val_str:
        return val_str
    # Unicode ×10^ format
    return val_str.replace('×10', 'E').replace('−', '-')

def parse_val_unc(cell):
    """Parse '7.3 (15)' or '4.438×10−5' → (val_ensdf, unc_str, is_blank)."""
    cell = cell.strip()
    if not cell:
        return '', '', True
    
    m = re.match(r'^(.+?)\s*\((.+?)\)$', cell)
    if m:
        val_raw = to_ensdf_sci(m.group(1).strip())
        unc_raw = m.group(2).strip()
        return val_raw, unc_raw, False
    
    # No uncertainty — just a value
    val_raw = to_ensdf_sci(cell)
    return val_raw, '', False

# ── Parse Table III ────────────────────────────────────────────
t3_data = {}  # key = rounded keV → list of [(exact_E, data_dict), ...]
with open(TABLE3_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8:
            continue
        ex_raw = parts[1]
        ib_raw = parts[3] if len(parts) > 3 else ''
        ie_raw = parts[4] if len(parts) > 4 else ''
        it_raw = parts[5] if len(parts) > 5 else ''
        
        ex_m = re.match(r'([\d.]+)', ex_raw)
        if not ex_m:
            continue
        ex_val = float(ex_m.group(1))
        key = round(ex_val)
        
        ib_val, ib_unc, ib_blank = parse_val_unc(ib_raw)
        ie_val, ie_unc, ie_blank = parse_val_unc(ie_raw)
        it_val, it_unc, it_blank = parse_val_unc(it_raw)
        
        entry = {
            'ex_val': ex_val,
            'ex_raw': ex_raw,
            'ib_val': ib_val, 'ib_unc': ib_unc, 'ib_blank': ib_blank,
            'ie_val': ie_val, 'ie_unc': ie_unc, 'ie_blank': ie_blank,
            'it_val': it_val, 'it_unc': it_unc, 'it_blank': it_blank,
            'used': False
        }
        if key not in t3_data:
            t3_data[key] = []
        t3_data[key].append(entry)

print(f"Table III entries: {sum(len(v) for v in t3_data.values())}")

# ── Update ENSDF E-records ─────────────────────────────────────
with open(ENSDF_PATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

modified = 0
new_lines = []

# Track current level
current_e = None

# Helper to format fields
def fmt_field(val, width):
    """Format value left-justified in field of given width.
    For E-n values that overflow, shorten mantissa."""
    if val == '' or val is None:
        return ' ' * width
    s = str(val)
    if len(s) <= width:
        return s.ljust(width)
    # Overflow: try to shorten
    # For E-n format like '4.438E-5' (8 chars in 7-char field):
    # Reduce mantissa decimal places
    import re as _re
    em = _re.match(r'^([+\-]?\d+\.?\d*)(E[+\-]\d+)$', s)
    if em:
        mantissa = em.group(1)
        exp = em.group(2)
        # Reduce mantissa to fit
        exp_len = len(exp)
        max_mantissa = width - exp_len
        if max_mantissa >= 1:
            # Try rounding mantissa to fewer digits
            mval = float(mantissa)
            # Format with decreasing precision until it fits
            for dp in range(max_mantissa - 1, -1, -1):
                if dp == 0:
                    short = str(int(round(mval)))
                else:
                    short = f'{mval:.{dp}f}'
                candidate = short + exp
                if len(candidate) <= width:
                    return candidate.ljust(width)
    # Last resort: truncate
    return s[:width].ljust(width)

def fmt_unc(unc, width):
    if unc == '' or unc is None:
        return ' ' * width
    return str(unc)[:width].ljust(width)

for i, line in enumerate(lines):
    # Track L-record energy
    if len(line) >= 9 and line[5:6] == ' ' and line[6:7] == ' ' and line[7:8] == 'L':
        e_field = line[9:19].strip()
        if e_field:
            try:
                current_e = float(e_field)
            except:
                pass
    
    # Detect primary E-record
    is_e = (len(line) >= 9 and line[5:6] == ' ' and 
            line[6:7] == ' ' and line[7:8] == 'E')
    
    if is_e and current_e is not None:
        key = round(current_e)
        
        if key in t3_data:
            entries = t3_data[key]
            
            if len(entries) == 1:
                d = entries[0]
                d['used'] = True
            else:
                # Match collision: find closest by exact energy
                best = None
                best_dist = float('inf')
                for ent in entries:
                    dist = abs(ent['ex_val'] - current_e)
                    if dist < best_dist:
                        best_dist = dist
                        best = ent
                if best is not None:
                    d = best
                    d['used'] = True
                else:
                    new_lines.append(line)
                    continue
            
            # Build new E-record line
            prefix = line[:22]
            middle = line[41:64]
            suffix = line[76:80]
            
            ib_field = fmt_field(d['ib_val'] if not d['ib_blank'] else '', 7)
            dib_field = fmt_unc(d['ib_unc'] if not d['ib_blank'] else '', 2)
            ie_field = fmt_field(d['ie_val'] if not d['ie_blank'] else '', 8)
            die_field = fmt_unc(d['ie_unc'] if not d['ie_blank'] else '', 2)
            ti_field = fmt_field(d['it_val'] if not d['it_blank'] else '', 10)
            dti_field = fmt_unc(d['it_unc'] if not d['it_blank'] else '', 2)
            
            new_line = (prefix + ib_field + dib_field + ie_field + die_field +
                       middle + ti_field + dti_field + suffix)
            new_line = new_line[:80].ljust(80)
            
            if new_line != line.rstrip('\n\r'):
                new_lines.append(new_line + '\n')
                modified += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(ENSDF_PATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

# Report unmatched T3 entries
unmatched = []
for key, entries in t3_data.items():
    for ent in entries:
        if not ent['used']:
            unmatched.append(ent['ex_val'])

if unmatched:
    print(f"\nUnmatched T3 entries: {len(unmatched)}")
    for e in sorted(unmatched):
        print(f"  {e}")

print(f"\nE-records modified: {modified}")
print("Done.")
