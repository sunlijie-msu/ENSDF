"""Generate B(E2) cG comments for 17 band gammas from Table II data.
Matches each gamma energy to its G-record context in the ENSDF file.
Outputs the exact replacement strings needed."""

import re

ENSDF_FILE = r"d:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens"

# Table II B(E2) values: Eg -> (B(E2) value string, uncertainty type)
# Format: (central_value, upper_unc, lower_unc, is_limit)
BE2_DATA = {
    "486.7":  ("0.46", "0.04", "0.04", False),
    "792.4":  ("0.30", "0.02", "0.02", False),
    "1044.0": ("0.22", "0.02", "0.02", False),
    "1239.5": ("0.09", "0.01", "0.01", False),
    "1468.0": ("0.02", None, None, True),
    "1205.2": ("0.05", None, None, True),
    "457.2":  ("0.48", "0.08", "0.07", False),
    "748.2":  ("0.47", "0.04", "0.04", False),
    "841.4":  ("0.42", "0.05", "0.05", False),
    "938.3":  ("0.35", "0.03", "0.03", False),
    "1040.2": ("0.26", "0.03", "0.02", False),
    "1164.1": ("0.17", None, None, True),
    "679.9":  ("0.25", "0.04", "0.03", False),
    "783.7":  ("0.27", "0.04", "0.03", False),
    "918.8":  ("0.26", "0.03", "0.03", False),
    "1108.5": ("0.24", "0.03", "0.03", False),
    "1328.4": ("0.20", None, None, True),
}

def make_be2_comment(val, up, low, is_limit):
    """Generate ENSDF cG comment line for B(E2) value.
    Format: 141SM cG $B(E2)|_=VALUE e{+2}b{+2} {UNC} (2026MaAA)."""
    if is_limit:
        unc_str = ""
        val_str = f">{val}"
    elif up == low:
        # Symmetric uncertainty
        # Find number of decimal places in val
        decimals = len(val.split('.')[1]) if '.' in val else 0
        # Uncertainty in last digits
        unc_digits = up.replace('0.', '').lstrip('0')
        if not unc_digits:
            unc_digits = '0'
        unc_str = f" {{I{unc_digits}}}"
        val_str = val
    else:
        # Asymmetric uncertainty
        # Both up and low have same decimal places as val
        decimals = len(val.split('.')[1]) if '.' in val else 0
        up_digits = up.replace('0.', '').lstrip('0')
        low_digits = low.replace('0.', '').lstrip('0')
        if not up_digits:
            up_digits = '0'
        if not low_digits:
            low_digits = '0'
        unc_str = f" {{I+{up_digits}-{low_digits}}}"
        val_str = val
    
    comment = f"141SM cG $B(E2)|_={val_str} e{{+2}}b{{+2}}{unc_str} (2026MaAA)."
    # Pad to 80 chars
    comment = comment.ljust(80)
    return comment

# Read ENSDF file
with open(ENSDF_FILE, 'r') as f:
    lines = f.readlines()

# Find all G-records with their context
print("=" * 80)
print("B(E2) COMMENT GENERATION")
print("=" * 80)

be2_entries = []

for i, line in enumerate(lines):
    line = line.rstrip('\n').rstrip('\r')
    if len(line) < 37:
        continue
    
    # Check if it's a G-record
    if line[7] != 'G' or line[6] != ' ':
        continue
    
    # Extract gamma energy
    e_field = line[9:19].strip()
    
    if e_field in BE2_DATA:
        val, up, low, is_limit = BE2_DATA[e_field]
        comment = make_be2_comment(val, up, low, is_limit)
        
        # Find the end of existing cG comments (look ahead)
        last_cg_line = i  # G-record line itself
        for j in range(i + 1, min(i + 10, len(lines))):
            check_line = lines[j].rstrip('\n').rstrip('\r')
            if len(check_line) >= 9 and check_line[7] == 'c' and check_line[8] == 'G':
                last_cg_line = j
            else:
                # Check for continuation cG (2cG, 3cG, etc.)
                if len(check_line) >= 9 and check_line[6] in '0123456789' and check_line[7] == 'c' and check_line[8] == 'G':
                    last_cg_line = j
                elif len(check_line) >= 9 and check_line[7] in 'c' and check_line[8] in ['L', 'G']:
                    last_cg_line = j
                else:
                    break
        
        print(f"\nEG={e_field:>8s} (line {i+1}):")
        print(f"  G-record:  {lines[i].rstrip()}")
        for k in range(i+1, last_cg_line+1):
            print(f"  cG line {k+1}: {lines[k].rstrip()}")
        print(f"  NEW B(E2): {comment}")
        
        be2_entries.append({
            'eg': e_field,
            'comment': comment,
            'insert_after_line': last_cg_line + 1,  # 1-indexed
            'g_line': i + 1,
            'context_before': ''.join(lines[i:last_cg_line+1]).rstrip()
        })

print(f"\n{'='*80}")
print(f"Generated {len(be2_entries)} B(E2) comments")

# Print all comments for verification
print("\n--- ALL B(E2) COMMENTS ---")
for entry in be2_entries:
    print(f"EG={entry['eg']:>8s}: {entry['comment']}")
