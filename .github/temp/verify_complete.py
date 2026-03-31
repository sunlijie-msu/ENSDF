#!/usr/bin/env python3
"""
COMPREHENSIVE T vs |t VERIFICATION WITH UNCERTAINTIES
- T field in L-record = half-life (t_1/2)
- |t field in cL T$ comment = lifetime (τ)
- Relationship: T = |t × ln(2) ≈ |t × 0.693147
- Check uncertainties: DT (L-record) vs {In} (cL comment)
"""

import re
import math

LN2 = math.log(2)  # 0.693147

UNIT_TO_SECONDS = {
    'fs': 1e-15, 'FS': 1e-15,
    'ps': 1e-12, 'PS': 1e-12,
    'ns': 1e-9,  'NS': 1e-9,
    'us': 1e-6,  'US': 1e-6,
    'ms': 1e-3,  'MS': 1e-3,
    's': 1.0,    'S': 1.0,
    'm': 60.0,   'M': 60.0,
    'h': 3600.0, 'H': 3600.0,
    'd': 86400.0, 'D': 86400.0,
    'y': 365.25 * 86400.0, 'Y': 365.25 * 86400.0,
}

def decimal_places(val_str):
    """Count decimal places in value string."""
    val_str = val_str.strip()
    if '.' in val_str:
        return len(val_str.split('.')[1])
    return 0

def parse_ensdf_unc(value_str, unc_str):
    """Convert {In} to float uncertainty."""
    if unc_str.strip() in ['GT', 'LT']:
        return None, unc_str.strip()
    try:
        n = float(unc_str.strip())
        ndp = decimal_places(value_str.strip())
        return n * (10 ** (-ndp)), None
    except:
        return None, None

def extract_t_value_and_unit(t_field_str):
    """Extract T value and unit from L-record field."""
    t_field_str = t_field_str.strip()
    match = re.match(r'^([\d.\-+]+)\s*([a-zA-Z]+)$', t_field_str)
    return (match.group(1), match.group(2)) if match else (None, None)

def parse_comment_data(comment_text):
    """Extract |t values and {I...} uncertainties from cL comment."""
    lines = comment_text.split('\n')
    clean_lines = []
    for line in lines:
        if len(line) > 11:
            clean_lines.append(line[11:])
        else:
            clean_lines.append(line)
    
    full_text = ' '.join(clean_lines)
    
    # Skip summary value (appears before "average of")
    if 'average of' in full_text.lower():
        parts = re.split(r'average of\s*', full_text, flags=re.IGNORECASE, maxsplit=1)
        full_text = parts[1] if len(parts) > 1 else full_text
    
    # Truncate before "Other:"
    if 'Other:' in full_text or 'other:' in full_text:
        full_text = re.split(r'[Oo]ther:', full_text)[0]
    
    data = []
    base_unit = None
    
    # Find all |t=value unit {In} patterns
    pattern = r'\|t\s*=\s*([\d.\-+]+)\s*([a-zA-Z]+)\s*\{I(\d+)\}'
    for match in re.finditer(pattern, full_text):
        val_str = match.group(1)
        unit = match.group(2)
        unc_str = match.group(3)
        
        if base_unit is None:
            base_unit = unit
        
        data.append((val_str, unc_str, unit))
    
    return data, base_unit

# Read ENSDF file
ensdf_file = r'A34/Cl34/new/Cl34_32s_3he_pg.ens'

with open(ensdf_file, 'r', encoding='utf-8', errors='replace') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

# Parse file
current_l_index = None
l_records = []
comment_blocks = {}

i = 0
while i < len(lines):
    line = lines[i]
    
    # L-record
    if len(line) >= 8 and line[6:8] == ' L':
        current_l_index = len(l_records)
        l_records.append({
            'line_num': i + 1,
            'energy': line[9:19].strip(),
            't_field': line[39:49].strip() if len(line) >= 49 else '',
            'dt_field': line[49:55].strip() if len(line) >= 55 else '',
            'raw_line': line
        })
        comment_blocks[current_l_index] = ''
    
    # cL comment
    elif (len(line) >= 8 and line[6:8] == 'cL') and current_l_index is not None:
        if 'T$' in line or 't$' in line or 'lifetime' in line.lower() or '|t' in line:
            comment_blocks[current_l_index] += line + '\n'
    
    # Continuation cL
    elif (len(line) >= 8 and re.match(r'\s*\d+cL', line[6:8])) and current_l_index is not None:
        if 'T$' in line or 't$' in line or 'lifetime' in line.lower() or '|t' in line:
            comment_blocks[current_l_index] += line + '\n'
    
    i += 1

# Verification output
print("=" * 150)
print("VERIFICATION: L-RECORD T (half-life) vs cL T$ COMMENT |t (lifetime) WITH UNCERTAINTIES")
print("Relationship: T = |t × ln(2) where ln(2) ≈ 0.693147")
print("=" * 150)
print()

ok_list = []
mismatch_list = []
no_comment_list = []
parse_error_list = []

for idx, l_rec in enumerate(l_records):
    energy = l_rec['energy']
    t_field = l_rec['t_field']
    dt_field = l_rec['dt_field']
    
    if not t_field:
        continue  # No half-life value
    
    # Extract T value
    t_val_str, t_unit = extract_t_value_and_unit(t_field)
    if not t_val_str or not t_unit:
        continue
    
    comment_text = comment_blocks.get(idx, '')
    
    # No comment case
    if not comment_text.strip():
        no_comment_list.append({
            'line': l_rec['line_num'],
            'energy': energy,
            't_field': t_field,
            'dt_field': dt_field
        })
        continue
    
    # Parse comment
    data_points, base_unit = parse_comment_data(comment_text)
    
    if not data_points:
        parse_error_list.append({
            'line': l_rec['line_num'],
            'energy': energy,
            't_field': t_field,
            'comment': comment_text[:100]
        })
        continue
    
    # Convert T to seconds
    try:
        t_val = float(t_val_str)
        t_sec = t_val * UNIT_TO_SECONDS[t_unit]
    except:
        parse_error_list.append({
            'line': l_rec['line_num'],
            'energy': energy,
            'reason': f'Cannot parse T={t_field}'
        })
        continue
    
    # Convert |t to seconds
    try:
        tau_val_str = data_points[0][0]
        tau_unc_str = data_points[0][1]
        tau_unit = data_points[0][2]
        
        tau_val = float(tau_val_str)
        tau_sec = tau_val * UNIT_TO_SECONDS[tau_unit]
        
        # Calculate expected T from |t
        t_expected = tau_sec * LN2
        
        # Calculate relative difference
        rel_diff = abs(t_sec - t_expected) / max(t_sec, t_expected) * 100 if t_sec > 0 else 999
        
        # Parse uncertainties
        tau_unc_float, tau_unc_marker = parse_ensdf_unc(tau_val_str, tau_unc_str)
        
        # Status
        if rel_diff <= 5.0:
            ok_list.append({
                'line': l_rec['line_num'],
                'energy': energy,
                't_obs': t_val_str,
                't_unit': t_unit,
                'dt_field': dt_field,
                'tau_val': tau_val_str,
                'tau_unit': tau_unit,
                'tau_unc': tau_unc_str,
                't_calc': t_expected,
                'rel_diff': rel_diff,
                'match': True
            })
        else:
            mismatch_list.append({
                'line': l_rec['line_num'],
                'energy': energy,
                't_obs': t_val,
                't_calc': t_expected,
                't_unit': t_unit,
                'tau_val': tau_val,
                'tau_unit': tau_unit,
                'dt_field': dt_field,
                'tau_unc': tau_unc_str,
                'rel_diff': rel_diff
            })
    
    except Exception as e:
        parse_error_list.append({
            'line': l_rec['line_num'],
            'energy': energy,
            'reason': str(e)
        })

# Print results
print("\n" + "=" * 150)
print(f"MATCHES: {len(ok_list)}  |  MISMATCHES: {len(mismatch_list)}  |  NO COMMENT: {len(no_comment_list)}  |  PARSE ERRORS: {len(parse_error_list)}")
print("=" * 150)

if ok_list:
    print("\n[OK] VERIFIED MATCHES (T = |t × ln(2)):\n")
    for item in ok_list:
        print(f"  L{item['line']:3d} E={item['energy']:>9s} | T={item['t_obs']:>7s}{item['t_unit']:>2s} DT={item['dt_field']:>6s} | |t={item['tau_val']:>7s}{item['tau_unit']:>2s} {{I{item['tau_unc']:>3s}}}")
        t_expected_formatted = f"{item['t_calc']:.4e}"
        print(f"       T_calc={t_expected_formatted} | Rel.Diff={item['rel_diff']:.3f}%")

if mismatch_list:
    print("\n[WARN] MISMATCHES (Rel.Diff > 5%):\n")
    for item in mismatch_list:
        print(f"  L{item['line']:3d} E={item['energy']:>9s} | T={item['t_obs']:.4e}{item['t_unit']:>2s} DT={item['dt_field']:>6s} | |t={item['tau_val']:.4e}{item['tau_unit']:>2s} {{I{item['tau_unc']:>3s}}}")
        print(f"       T_calc={item['t_calc']:.4e} | Rel.Diff={item['rel_diff']:.3f}%")

if no_comment_list:
    print("\n[INFO] NO cL T$ COMMENT:\n")
    for item in no_comment_list:
        print(f"  L{item['line']:3d} E={item['energy']:>9s} | T={item['t_field']:>15s} DT={item['dt_field']:>6s}")

if parse_error_list:
    print("\n[ERROR] PARSE ERRORS:\n")
    for item in parse_error_list:
        print(f"  L{item['line']:3d} E={item['energy']:>9s} | {item.get('reason', 'Unknown error')}")

print("\n" + "=" * 150)
print("END VERIFICATION")
print("=" * 150)
