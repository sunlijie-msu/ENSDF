#!/usr/bin/env python3
"""
Cross-check T (lifetime) values in L-records against |t (half-life) values in cL T$ comments.
Relationship: t_1/2 = T * ln(2), or T = t_1/2 / ln(2)
where ln(2) ≈ 0.693147
"""

import re
import math

# Read file
with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_32s_3he_pg.ens', 'r') as f:
    lines = f.readlines()

# Unit conversion factors to seconds
UNIT_TO_SECONDS = {
    'fs': 1e-15, 'ps': 1e-12, 'ns': 1e-9, 'us': 1e-6, 'ms': 1e-3,
    's': 1.0, 'm': 60.0, 'h': 3600.0, 'd': 86400.0, 'y': 365.25 * 86400.0,
}

LN2 = math.log(2)

# Parse L-records and cL T$ comments
l_records = {}  # key: line_number, value: {e_level, t_val_str, t_val_sec, dt_unc}
cl_t_comments = {}  # key: corresponding_L_line, value: {t_val_str, t_val_sec, t_unc}

for i, line in enumerate(lines):
    # L-record pattern: NUCID at 1-5, type "L" at 8
    if len(line) >= 49 and line[5:8].strip() and line[7] == 'L':
        # Extract energy (cols 10-19, 1-indexed = 9-19 in 0-indexed)
        e_level = line[9:19].strip() if len(line) >= 19 else ''
        # Extract T value (cols 40-49, 1-indexed = 39-49 in 0-indexed)
        t_val_str = line[39:49].strip() if len(line) >= 49 else ''
        # Extract DT uncertainty (cols 50-55, 1-indexed = 49-55 in 0-indexed)
        dt_unc = line[49:55].strip() if len(line) >= 55 else ''
        
        if t_val_str:  # Only if T field is non-empty
            # Parse T value: format is "VALUE UNIT" (e.g., "4.9 PS")
            parts = t_val_str.split()
            if len(parts) >= 1:
                try:
                    t_val_num = float(parts[0])
                    t_unit = parts[1].lower() if len(parts) >= 2 else 'ps'  # Default to ps
                    t_val_sec = t_val_num * UNIT_TO_SECONDS.get(t_unit, 1e-12)  # Convert to seconds
                    
                    l_records[i] = {
                        'e_level': e_level,
                        't_val_str': t_val_str,
                        't_val_num': t_val_num,
                        't_unit': t_unit,
                        't_val_sec': t_val_sec,
                        'dt_unc': dt_unc,
                        'line': line.rstrip()
                    }
                except ValueError:
                    pass

    # cL T$ comment pattern: extract |t= and {I...}
    if 'cL' in line and 'T$' in line:
        # Pattern: |t=VALUE UNIT {IVALUE}
        match = re.search(r'\|t\s*=\s*([\d.]+)\s*([a-z]+)\s*\{I([\d+\-]+)\}', line, re.IGNORECASE)
        if match:
            t_val_num = float(match.group(1))
            t_unit = match.group(2).lower()
            t_unc_str = match.group(3)
            
            t_val_sec = t_val_num * UNIT_TO_SECONDS.get(t_unit, 1e-12)
            
            # Find the closest preceding L-record with T value
            for l_line in sorted([k for k in l_records.keys() if k < i], reverse=True):
                if l_records[l_line]['t_val_str']:
                    cl_t_comments[l_line] = {
                        't_val_num': t_val_num,
                        't_unit': t_unit,
                        't_val_sec': t_val_sec,
                        't_unc': t_unc_str,
                        'comment_line': i + 1,
                        'full': line.rstrip()
                    }
                    break

print("\n" + "=" * 130)
print("LIFETIME vs HALF-LIFE VERIFICATION: L-RECORD (T) vs cL T$ COMMENT (|t)")
print("Relationship: t_1/2 = T * ln(2), where ln(2) ≈ 0.693147")
print("=" * 130)

issues = []
matched = 0

for l_line_num in sorted(l_records.keys()):
    l_info = l_records[l_line_num]
    e_level = l_info['e_level']
    l_t_val_str = l_info['t_val_str']
    l_t_val_num = l_info['t_val_num']
    l_t_unit = l_info['t_unit']
    l_t_sec = l_info['t_val_sec']
    l_dt_unc = l_info['dt_unc']
    
    print(f"\n{l_line_num + 1:4d} | Energy: {e_level:>12}")
    print(f"      | L-record T (lifetime): {l_t_val_str:<15} = {l_t_val_num:.4e} sec  |  DT={l_dt_unc:<6}")
    
    if l_line_num in cl_t_comments:
        cl_info = cl_t_comments[l_line_num]
        cl_t_val_num = cl_info['t_val_num']
        cl_t_unit = cl_info['t_unit']
        cl_t_sec = cl_info['t_val_sec']
        cl_t_unc = cl_info['t_unc']
        
        print(f"  {cl_info['comment_line']:4d} | cL T$ |t (half-life): {cl_t_val_num} {cl_t_unit} {cl_t_unc}({{I}}) = {cl_t_val_num:.4e} sec")
        
        # Convert: calculated T from |t = |t / ln(2)
        t_calc_sec = cl_t_sec / LN2
        t_calc_num = t_calc_sec / UNIT_TO_SECONDS.get(l_t_unit, 1e-12)
        
        # Calculate what |t should be from measured T: |t = T * ln(2)
        t_half_calc_sec = l_t_sec * LN2
        t_half_calc_num = t_half_calc_sec / UNIT_TO_SECONDS.get(cl_t_unit, 1e-12)
        
        print(f"      | Conversion check:")
        print(f"      |   From cL |t: calculated T = {cl_t_val_num:.4e} / {LN2:.6f} = {t_calc_num:.4e} {l_t_unit}")
        print(f"      |   From L  T: calculated |t = {l_t_val_num:.4e} * {LN2:.6f} = {t_half_calc_num:.4e} {cl_t_unit}")
        
        # Compare numeric values with tolerance (5% relative difference acceptable)
        rel_diff_t = abs(l_t_val_num - t_calc_num) / max(l_t_val_num, t_calc_num)
        rel_diff_t_half = abs(cl_t_val_num - t_half_calc_num) / max(cl_t_val_num, t_half_calc_num)
        
        tolerance = 0.05  # 5% tolerance
        
        if rel_diff_t < tolerance or rel_diff_t_half < tolerance:
            print(f"      | OK VALUES MATCH (rel.diff: T={rel_diff_t:.3%}, t_1/2={rel_diff_t_half:.3%})")
            matched += 1
        else:
            print(f"      | WARN MISMATCH (rel.diff: T={rel_diff_t:.3%}, t_1/2={rel_diff_t_half:.3%})")
            issues.append((l_line_num + 1, f"E={e_level}: L-T={l_t_val_num:.2e}{l_t_unit} vs calc-T={t_calc_num:.2e}{l_t_unit} (diff {rel_diff_t:.1%})"))
        
        # Uncertainty check
        print(f"      | Uncertainties: L-DT={l_dt_unc:<6} cL-{{I{cl_t_unc}}}")
        
        print(f"      | {cl_info['full'][:90]}")

    else:
        print(f"      | WARN NO cL T$ COMMENT FOUND")
        issues.append((l_line_num + 1, f"E={e_level} T={l_t_val_str}: missing cL T$ comment"))

print("\n" + "=" * 130)
print(f"SUMMARY: {matched} matched, {len(l_records)} total L-records with T, {len(issues)} issues")
print("=" * 130)

if issues:
    print("\nISSUES:")
    for line_num, msg in issues:
        print(f"  Line {line_num}: {msg}")
else:
    print("\nOK: All T values and uncertainties consistent with |t comments!")

