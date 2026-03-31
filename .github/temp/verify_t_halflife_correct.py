#!/usr/bin/env python3
"""
CORRECT VERIFICATION: L-record T (half-life) vs cL T$ comment |t (lifetime)
Relationship: t_1/2 = |t * ln(2)  where |t is lifetime, T is half-life
"""

import re
import math

LN2 = math.log(2)  # ≈ 0.693147

# Unit conversion to base unit (seconds)
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
    """Count decimal places in a value string."""
    val_str = val_str.strip()
    if '.' in val_str:
        return len(val_str.split('.')[1])
    return 0

def parse_ensdf_unc(value_str, unc_str):
    """Convert {In} notation to float."""
    if unc_str.strip() in ['GT', 'LT']:
        return None, unc_str.strip()
    try:
        n = float(unc_str.strip())
        ndp = decimal_places(value_str.strip())
        unc_float = n * (10 ** (-ndp))
        return unc_float, None
    except:
        return None, None

def extract_t_value_and_unit(t_field_str):
    """Extract value and unit from L-record T field (columns 40-49)."""
    t_field_str = t_field_str.strip()
    match = re.match(r'^([\d.\-+]+)\s*([a-zA-Z]+)$', t_field_str)
    if match:
        return match.group(1), match.group(2)
    return None, None

def parse_comment_data(comment_text):
    """
    Extract |t (lifetime) values and uncertainties from ENSDF cL T$ comment.
    Returns: (data_points, base_unit, src_max_dec)
    """
    lines = comment_text.split('\n')
    clean_lines = []
    for line in lines:
        if len(line) > 11:
            clean_lines.append(line[11:])
        else:
            clean_lines.append(line)
    
    full_text = ' '.join(clean_lines)
    
    # Skip summary value (before "average of")
    if 'average of' in full_text.lower():
        parts = re.split(r'average of\s*', full_text, flags=re.IGNORECASE, maxsplit=1)
        full_text = parts[1] if len(parts) > 1 else full_text
    
    # Truncate before "Other:"
    if 'Other:' in full_text or 'other:' in full_text:
        full_text = re.split(r'[Oo]ther:', full_text)[0]
    
    data = []
    base_unit = None
    src_max_dec = 0
    
    # Find all |t=value unit {In} patterns
    pattern = r'\|t\s*=\s*([\d.\-+]+)\s*([a-zA-Z]+)\s*\{I(\d+)\}'
    for match in re.finditer(pattern, full_text):
        val_str = match.group(1)
        unit = match.group(2)
        unc_str = match.group(3)
        
        src_max_dec = max(src_max_dec, decimal_places(val_str))
        if base_unit is None:
            base_unit = unit
        
        data.append((val_str, unc_str, unit))
    
    return data, base_unit, src_max_dec

print("=" * 140)
print("HALF-LIFE VERIFICATION: L-RECORD (T) vs cL T$ COMMENT (|t)")
print("T = half-life (t_1/2)  |  |t = lifetime (tau)")
print("Relationship: T = |t * ln(2), where ln(2) ≈ 0.693147")
print("=" * 140)
print()

ensdf_file = r'A34/Cl34/new/Cl34_32s_3he_pg.ens'

with open(ensdf_file, 'r', encoding='utf-8', errors='replace') as f:
    lines = [line.rstrip('\n') for line in f.readlines()]

# Parse ENSDF file
current_l_index = None
l_records = []
comment_blocks = {}

i = 0
while i < len(lines):
    line = lines[i]
    
    # Detect L-record
    if len(line) >= 8 and line[6:8] == ' L':
        current_l_index = len(l_records)
        l_records.append({
            'line_num': i + 1,
            'energy': line[9:19].strip(),
            't_field': line[39:49].strip() if len(line) >= 49 else '',
            'dt_field': line[49:55].strip() if len(line) >= 55 else '',
        })
        comment_blocks[current_l_index] = ''
        i += 1
    
    # Detect cL comment line
    elif (len(line) >= 8 and line[6:8] == 'cL') and current_l_index is not None:
        if 'T$' in line or 't$' in line or 'lifetime' in line.lower() or '|t' in line:
            comment_blocks[current_l_index] += line + '\n'
        i += 1
    
    # Detect continuation cL line (2cL, 3cL, etc.)
    elif (len(line) >= 8 and re.match(r'\s*\d+cL', line[6:8])) and current_l_index is not None:
        if 'T$' in line or 't$' in line or 'lifetime' in line.lower() or '|t' in line:
            comment_blocks[current_l_index] += line + '\n'
        i += 1
    
    else:
        i += 1

# Verify each L-record
ok_count = 0
mismatch_count = 0

for idx, l_rec in enumerate(l_records):
    energy = l_rec['energy']
    t_field = l_rec['t_field']
    dt_field = l_rec['dt_field']
    
    if not t_field:
        continue  # Skip levels with no half-life
    
    # Extract value and unit from L-record T field
    t_val_str, t_unit = extract_t_value_and_unit(t_field)
    
    if not t_val_str or not t_unit:
        continue
    
    comment_text = comment_blocks.get(idx, '')
    
    print(f"{l_rec['line_num']:3d} | Energy:     {energy:>9s}  |  T (half-life): {t_field:>12s}  DT={dt_field}")
    
    if not comment_text.strip():
        print(f"      | NO cL T$ COMMENT FOUND")
        print()
        continue
    
    # Parse comment data
    data_points, base_unit, src_max_dec = parse_comment_data(comment_text)
    
    if not data_points:
        print(f"      | CANNOT PARSE |t FROM COMMENT")
        for line in comment_text.split('\n'):
            if line.strip():
                print(f"      |  {line[:80]}")
        print()
        continue
    
    # Convert to seconds
    try:
        t_val = float(t_val_str)
        t_unit_factor = UNIT_TO_SECONDS[t_unit]
        t_sec = t_val * t_unit_factor  # T = half-life in seconds
    except Exception as e:
        print(f"      | ERROR parsing T: {e}")
        print()
        continue
    
    try:
        tau_val_str = data_points[0][0]  # |t = lifetime
        tau_unc_str = data_points[0][1]
        tau_unit = data_points[0][2]
        
        tau_val = float(tau_val_str)
        tau_unit_factor = UNIT_TO_SECONDS[tau_unit]
        tau_sec = tau_val * tau_unit_factor  # |t = lifetime in seconds
        
        # Parse uncertainty
        unc_val, unc_marker = parse_ensdf_unc(tau_val_str, tau_unc_str)
        
    except Exception as e:
        print(f"      | ERROR parsing cL |t: {e}")
        print()
        continue
    
    # Calculate expected T from |t
    t_calculated = tau_sec * LN2
    
    # Calculate relative difference
    if t_calculated > 0 and t_sec > 0:
        rel_diff = abs(t_sec - t_calculated) / max(t_sec, t_calculated) * 100
        
        if rel_diff <= 5.0:
            status = "OK"
            ok_count += 1
        else:
            status = "WARN MISMATCH"
            mismatch_count += 1
        
        print(f"      | cL T$ |t (lifetime): {tau_val_str:>8s} {tau_unit:>2s} {{I{tau_unc_str:>3s}}}  ({tau_sec:.4e} sec)")
        print(f"      | Conversion check:")
        print(f"      |   From cL |t: T_calc = {tau_val_str} * ln(2) = {tau_sec:.4e} * {LN2:.6f} = {t_calculated:.4e} sec")
        print(f"      |   From L  T: T_obs  = {t_val_str} {t_unit} = {t_sec:.4e} sec")
        print(f"      |   Relative difference: {rel_diff:.3f}%")
        print(f"      | {status}")
        
        if unc_val is not None:
            print(f"      | Uncertainties: L-DT={dt_field:>6s} cL-{{I{tau_unc_str}}}")
        
        for line in comment_text.split('\n'):
            if line.strip():
                print(f"      |  {line}")
    
    print()

print("=" * 140)
print(f"SUMMARY: {ok_count} OK  |  {mismatch_count} MISMATCHES")
print("=" * 140)
