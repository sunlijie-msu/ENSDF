#!/usr/bin/env python
"""
Check for lifetime/half-life conversion errors in ENSDF files.
Relationship: T₁/₂ = τ × ln(2) ≈ τ × 0.693147
"""

import re
import math
import sys

def check_lifetime_halflife(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    mismatches = []
    for i, line in enumerate(lines):
        # Look for L-records ONLY (column 8 = 'L', column 7 must be blank)
        # Column 6 should be blank (or continuation marker like 'X')
        if len(line) >= 8 and line[7] == 'L':
            # Make sure it's actually an L-record, not a comment
            if '35CL' in line[0:6] and (line[6] == ' ' or line[6] in 'X'):
                if len(line) >= 49:
                    t_field = line[39:49].strip()
                    line_num = i + 1
                    level_e = line[9:19].strip() if len(line) >= 19 else '?'
                
                # Look ahead for cL T$ comment (can span multiple lines)
                j = i + 1
                lifetime_value = None
                lifetime_unit = None
                lifetime_unc = None
                found_t_comment = False
                
                while j < min(len(lines), i + 15):  # Increased to 15 lines
                    next_line = lines[j]
                    
                    # Stop at next L or G record
                    if len(next_line) >= 8 and (next_line[7] in ['L', 'G']):
                        if next_line[0:6].strip() == '35CL' and 'cL' not in next_line[6:9] and 'cG' not in next_line[6:9]:
                            break
                    
                    # Look for T$ in lifetime comments
                    if 'T$' in next_line and 'lifetime' in next_line:
                        found_t_comment = True
                        # Extract lifetime value: |t=VALUE UNIT {UNC}
                        match = re.search(r'\|t=([0-9.]+)\s*([a-z]+)\s*\{', next_line)
                        if match:
                            lifetime_value = float(match.group(1))
                            lifetime_unit = match.group(2).upper()
                            match_unc = re.search(r'\{I([+-]?[0-9\-]+)\}', next_line)
                            if match_unc:
                                lifetime_unc = match_unc.group(1)
                        break  # Found T$, stop looking
                    
                    j += 1
                
                # If we found lifetime and T field, compare
                if lifetime_value and t_field and any(u in t_field for u in ['FS', 'PS', 'NS', 'US', 'MS', 'S ']):
                    t_match = re.match(r'([0-9.]+)\s*([A-Z]+)', t_field)
                    if t_match:
                        t_value = float(t_match.group(1))
                        t_unit = t_match.group(2)
                        
                        # Convert to femtoseconds
                        unit_conv = {
                            'FS': 1,
                            'PS': 1e3,
                            'NS': 1e6,
                            'US': 1e9,
                            'MS': 1e12,
                            'S': 1e15
                        }
                        
                        lifetime_fs = lifetime_value * unit_conv.get(lifetime_unit, 1)
                        t_fs = t_value * unit_conv.get(t_unit, 1)
                        
                        # Expected half-life from lifetime
                        expected_t_fs = lifetime_fs * math.log(2)
                        
                        # Check if mismatch (allow 1% tolerance + 0.1 FS minimum)
                        tolerance = max(0.1, expected_t_fs * 0.01)
                        if abs(expected_t_fs - t_fs) > tolerance:
                            pct_error = ((t_fs - expected_t_fs) / expected_t_fs * 100) if expected_t_fs > 0 else 0
                            mismatches.append({
                                'line': line_num,
                                'level_e': level_e,
                                'lifetime': lifetime_value,
                                'lifetime_unit': lifetime_unit,
                                'lifetime_unc': lifetime_unc,
                                't_field': t_field,
                                'expected_t': expected_t_fs,
                                'actual_t': t_fs,
                                'error_pct': pct_error
                            })
    
    return mismatches

if __name__ == '__main__':
    filename = r'A35/Cl35/new/Cl35_adopted.ens'
    mismatches = check_lifetime_halflife(filename)
    
    if mismatches:
        print(f'\n*** FOUND {len(mismatches)} LIFETIME/HALF-LIFE MISMATCHES ***\n')
        print('Line | Level(keV) | Lifetime {Unc}        | T-field    | Expected T | Actual T | Error %')
        print('-' * 105)
        for m in mismatches:
            print(f'{m["line"]:4d} | {m["level_e"]:>10s} | {m["lifetime"]:>5.1f} {m["lifetime_unit"]:2s} {{{m["lifetime_unc"]:>3s}}} | {m["t_field"]:>10s} | {m["expected_t"]:>10.2f} FS | {m["actual_t"]:>7.2f} FS | {m["error_pct"]:>6.1f}%')
        print('\n=== DETAILS ===\n')
        for m in mismatches:
            print(f'Line {m["line"]}: Level E={m["level_e"]} keV')
            print(f'  Lifetime: {m["lifetime"]} {m["lifetime_unit"]} {{I{m["lifetime_unc"]}}}')
            print(f'  T field:  {m["t_field"]}')
            print(f'  Expected: {m["expected_t"]:.2f} FS (from τ × ln(2) = {m["lifetime"]} × 0.693147)')
            print(f'  Actual:   {m["actual_t"]:.2f} FS')
            print(f'  Diff:     {m["actual_t"] - m["expected_t"]:+.2f} FS ({m["error_pct"]:+.1f}%)')
            print()
    else:
        print('✓ No significant mismatches found (within 5% tolerance).')
