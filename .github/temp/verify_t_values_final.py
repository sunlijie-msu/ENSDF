#!/usr/bin/env python3
"""
FINAL VERIFICATION: L-record T (half-life) vs cL T$ comment |t (half-life)
Both are HALF-LIFE values and should match directly (no ln(2) conversion).
"""

import re
import math

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

def get_unit_name(unit_str):
    """Convert uppercase/lowercase unit to standard display name."""
    unit_map = {
        'fs': 'fs', 'FS': 'fs',
        'ps': 'ps', 'PS': 'ps',
        'ns': 'ns', 'NS': 'ns',
        'us': 'us', 'US': 'us',
        'ms': 'ms', 'MS': 'ms',
        's': 's',   'S': 's',
        'm': 'm',   'M': 'm',
        'h': 'h',   'H': 'h',
        'd': 'd',   'D': 'd',
        'y': 'y',   'Y': 'y',
    }
    return unit_map.get(unit_str, unit_str)

def decimal_places(val_str):
    """Count decimal places in a value string."""
    val_str = val_str.strip()
    if '.' in val_str:
        return len(val_str.split('.')[1])
    return 0

def parse_ensdf_unc(value_str, unc_str):
    """Convert {In} notation to float."""
    # Handle special markers
    if unc_str.strip() in ['GT', 'LT']:
        return None, unc_str.strip()
    
    try:
        n = float(unc_str.strip())
        ndp = decimal_places(value_str.strip())
        unc_float = n * (10 ** (-ndp))
        return unc_float, None
    except:
        return None, None

def parse_comment_data(comment_text):
    """
    Extract value(s) and uncertainty from ENSDF cL T$ comment.
    Both T (L-record) and |t (comment) are HALF-LIFE values.
    Returns: (data_points, base_unit, src_max_dec)
      where data_points = list of (value_str, unc_str, unit) tuples
            base_unit = first unit found
            src_max_dec = max decimal places seen in original strings
    """
    data = []
    base_unit = None
    src_max_dec = 0
    
    # Remove ENSDF record prefix lines (NUCID cL, 2cL, 3cL)
    lines = comment_text.split('\n')
    clean_lines = []
    for line in lines:
        # Remove first ~11 columns (NUCID + cL marker)
        if len(line) > 11:
            clean_lines.append(line[11:])
        else:
            clean_lines.append(line)
    
    full_text = ' '.join(clean_lines)
    
    # Skip summary value (before "average of" keyword)
    if 'average of' in full_text.lower():
        parts = re.split(r'average of\s*', full_text, flags=re.IGNORECASE, maxsplit=1)
        full_text = parts[1] if len(parts) > 1 else full_text
    
    # Truncate before "Other:" keyword
    if 'Other:' in full_text or 'other:' in full_text:
        full_text = re.split(r'[Oo]ther:', full_text)[0]
    
    # Find all |t=value unit {In} patterns
    pattern = r'\|t\s*=\s*([\d.\-+]+)\s*([a-zA-Z]+)\s*\{I(\d+)\}'
    for match in re.finditer(pattern, full_text):
        val_str = match.group(1)
        unit = match.group(2)
        unc_str = match.group(3)
        
        # Record source decimal places
        src_max_dec = max(src_max_dec, decimal_places(val_str))
        
        # Set base unit from first match
        if base_unit is None:
            base_unit = unit
        
        data.append((val_str, unc_str, unit))
    
    return data, base_unit, src_max_dec

def extract_t_value_and_unit(t_field_str):
    """
    Extract value and unit from L-record T field (columns 40-49).
    Returns: (value_str, unit_str)
    Format examples: "4.9 PS", "51 FS", "1.2 PS", etc.
    """
    t_field_str = t_field_str.strip()
    
    # Match pattern: number (with optional decimal) followed by unit
    match = re.match(r'^([\d.\-+]+)\s*([a-zA-Z]+)$', t_field_str)
    if match:
        return match.group(1), match.group(2)
    
    return None, None

print("=" * 130)
print("HALF-LIFE VERIFICATION: L-RECORD (T) vs cL T$ COMMENT (|t)")
print("Both are HALF-LIFE values — direct comparison (NO ln(2) conversion)")
print("=" * 130)
print()

# Read the ENSDF file
ensdf_file = r'A34/Cl34/new/Cl34_32s_3he_pg.ens'

try:
    with open(ensdf_file, 'r', encoding='utf-8', errors='replace') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
except:
    with open(ensdf_file, 'r', encoding='latin-1', errors='replace') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

# Parse ENSDF file
current_level_data = {}
current_l_index = None
l_records = []
comment_blocks = {}  # Map from L-record index to accumulated comment text

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
            'raw_line': line
        })
        comment_blocks[current_l_index] = ''
        i += 1
    
    # Detect cL comment line (applies to previous L-record)
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
print()
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
    
    # Look for cL comment
    comment_text = comment_blocks.get(idx, '')
    
    print(f"{l_rec['line_num']:3d} | Energy:       {energy}")
    print(f"      | L-record T (half-life): {t_field:15s} |  DT={dt_field}")
    
    if not comment_text.strip():
        print(f"      | WARN NO cL T$ COMMENT FOUND")
        print()
        continue
    
    # Parse comment data
    data_points, base_unit, src_max_dec = parse_comment_data(comment_text)
    
    if not data_points:
        print(f"      | WARN NO |t VALUE EXTRACTED FROM COMMENT")
        for line in comment_text.split('\n'):
            if line.strip():
                print(f"      |  {line}")
        print()
        continue
    
    # Convert all to base unit (seconds) for comparison
    try:
        t_val = float(t_val_str)
        t_unit_factor = UNIT_TO_SECONDS[t_unit]
        t_sec = t_val * t_unit_factor
    except:
        print(f"      | ERROR parsing L-record T value")
        print()
        continue
    
    try:
        comment_val_str = data_points[0][0]
        comment_unc_str = data_points[0][1]
        comment_unit = data_points[0][2]
        
        comment_val = float(comment_val_str)
        comment_unit_factor = UNIT_TO_SECONDS[comment_unit]
        comment_sec = comment_val * comment_unit_factor
        
        # Parse uncertainty
        unc_val, unc_marker = parse_ensdf_unc(comment_val_str, comment_unc_str)
        
    except Exception as e:
        print(f"      | ERROR parsing comment: {e}")
        for line in comment_text.split('\n'):
            if line.strip():
                print(f"      |  {line}")
        print()
        continue
    
    # Calculate relative difference (both are half-life, should be nearly equal)
    if t_sec > 0 and comment_sec > 0:
        rel_diff_pct = abs(t_sec - comment_sec) / max(t_sec, comment_sec) * 100
        
        # Convert back to display units for verification
        display_unit = get_unit_name(base_unit) if base_unit else 't_unit'
        t_display = t_sec / UNIT_TO_SECONDS[base_unit if base_unit else 'ps']
        
        if rel_diff_pct > 5.0:  # 5% tolerance
            status = "WARN MISMATCH"
        else:
            status = "OK"
        
        print(f"    {l_rec['line_num']:3d} | cL T$ |t (half-life): {comment_val_str} {comment_unit} {comment_unc_str}({'{I}'}) = {comment_sec:.4e} sec")
        print(f"      | Direct comparison (both are half-life):")
        print(f"      |   L-record T:  {t_val_str} {t_unit} = {t_sec:.4e} sec")
        print(f"      |   Comment |t:  {comment_val_str} {comment_unit} = {comment_sec:.4e} sec")
        print(f"      |   Relative difference: {rel_diff_pct:.3f}%")
        print(f"      | {status}")
        
        # Uncertainties
        if unc_val is not None:
            print(f"      | Uncertainties: L-DT={dt_field:6s} cL-{{I{comment_unc_str}}}")
        
        # Print comment line
        for line in comment_text.split('\n'):
            if line.strip():
                print(f"      |  {line}")
    
    print()

print("=" * 130)
print("END OF VERIFICATION")
print("=" * 130)
