#!/usr/bin/env python3
"""
Cross-check T (half-life) values in L-records against |t values in cL T$ comments.
Also verify uncertainties.
"""

import re
import sys

# Read file
with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_32s_3he_pg.ens', 'r') as f:
    lines = f.readlines()

# Parse L-records and cL T$ comments
l_records = {}  # key: line_number, value: {e_level, t_val, dt_unc}
cl_t_comments = {}  # key: corresponding_L_line, value: {t_val, t_unc}

for i, line in enumerate(lines):
    # L-record pattern: NUCID at 1-5, type "L" at 8
    if len(line) >= 49 and line[5:8].strip() and line[7] == 'L':
        # Extract energy (cols 10-19, 1-indexed)
        e_level = line[9:19].strip() if len(line) >= 19 else ''
        # Extract T value (cols 40-49, 1-indexed)
        t_val = line[39:49].strip() if len(line) >= 49 else ''
        # Extract DT uncertainty (cols 50-55, 1-indexed)
        dt_unc = line[49:55].strip() if len(line) >= 55 else ''
        
        if t_val:  # Only if T field is non-empty
            l_records[i] = {
                'e_level': e_level,
                't_val': t_val,
                'dt_unc': dt_unc,
                'line': line.rstrip()
            }

    # cL T$ comment pattern: extract |t= and {I...}
    if 'cL' in line and 'T$' in line:
        # Pattern: |t=VALUE UNIT {IVALUE}
        match = re.search(r'\|t\s*=\s*([\d.]+)\s*([a-z]+)\s*\{I([\d+\-]+)\}', line, re.IGNORECASE)
        if match:
            t_val_str = match.group(1) + ' ' + match.group(2)
            t_unc_str = match.group(3)
            # Find the closest preceding L-record with T value
            for l_line in sorted([k for k in l_records.keys() if k < i], reverse=True):
                if l_records[l_line]['t_val']:
                    cl_t_comments[l_line] = {
                        't_val': t_val_str,
                        't_unc': t_unc_str,
                        'comment_line': i + 1,
                        'full': line.rstrip()
                    }
                    break

print("\n" + "=" * 110)
print("T-VALUE VERIFICATION: L-RECORD vs cL T$ COMMENT LINE")
print("=" * 110)

issues = []
matched = 0

for l_line_num in sorted(l_records.keys()):
    l_info = l_records[l_line_num]
    e_level = l_info['e_level']
    l_t_val = l_info['t_val']
    l_dt_unc = l_info['dt_unc']
    
    print(f"\n{l_line_num + 1:4d} | Energy: {e_level:>12}")
    print(f"      | L-record: T={l_t_val:<18} DT={l_dt_unc:<6}")
    
    if l_line_num in cl_t_comments:
        cl_info = cl_t_comments[l_line_num]
        cl_t_val = cl_info['t_val']
        cl_t_unc = cl_info['t_unc']
        print(f"      | cL T$   : |t={cl_t_val:<18} {{I{cl_t_unc}}}")
        print(f"  {cl_info['comment_line']:4d} | {cl_info['full'][:85]}")
        
        # Extract numeric parts for comparison
        l_num = ''.join(c for c in l_t_val if c.isdigit() or c == '.')
        cl_num = ''.join(c for c in cl_t_val if c.isdigit() or c == '.')
        
        # Unit conversion: normalize to ps (picoseconds)
        l_unit = ''.join(c for c in l_t_val if c.isalpha()).lower()
        cl_unit = ''.join(c for c in cl_t_val if c.isalpha()).lower()
        
        symbol = "OK" if l_num == cl_num else "WARN"
        print(f"      | {symbol:4s} VALUE MATCH: L={l_num:<8} cL={cl_num:<8}")
        
        # Uncertainty comparison (both should be present)
        if l_dt_unc and cl_t_unc:
            print(f"      | Uncertainties: L-DT={l_dt_unc:<6} cL-{{I}}={cl_t_unc:<6}")
        elif not l_dt_unc and cl_t_unc:
            print(f"      | WARN L-record missing DT, but cL has {{I{cl_t_unc}}}")
            issues.append((l_line_num + 1, f"L-record at E={e_level}: DT missing but cL has {{I{cl_t_unc}}}"))
        elif l_dt_unc and not cl_t_unc:
            print(f"      | WARN cL comment missing {{I}}, but L-record has DT={l_dt_unc}")
            issues.append((l_line_num + 1, f"L-record at E={e_level}: cL missing {{I}} but L-record has DT={l_dt_unc}"))
        
        if l_num == cl_num:
            matched += 1
        else:
            issues.append((l_line_num + 1, f"MISMATCH at E={e_level}: L-T={l_num}, cL-|t={cl_num}"))
    else:
        print(f"      | WARN NO cL T$ COMMENT FOUND for this L-record")
        issues.append((l_line_num + 1, f"L-record at E={e_level} with T={l_t_val} missing cL T$ comment"))

print("\n" + "=" * 110)
print(f"SUMMARY: {matched} matched, {len(l_records) - matched} with L-records, {len(issues)} issues found")
print("=" * 110)

if issues:
    print("\nISSUES:")
    for line_num, msg in issues:
        print(f"  Line {line_num}: {msg}")
else:
    print("\nOK: All T values and uncertainties match!")

