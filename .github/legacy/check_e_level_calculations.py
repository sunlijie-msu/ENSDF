#!/usr/bin/env python3
"""
Check E(level) = S * 0.9711849866847 + 6370.81 calculations in ENSDF file.
Identifies levels where E(level) or DE don't match the formula.
"""

import sys

def check_calculations(filename):
    """Check all E(level) calculations against S values."""
    
    # Constants
    FACTOR = 0.9711849866847
    SP = 6370.81
    
    # Read file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = []
    
    for line_num, line in enumerate(lines, 1):
        if not line.startswith(' 35CL  L') or len(line) < 74:
            continue
            
        # Extract fields (columns are 1-indexed in ENSDF, 0-indexed in Python)
        e_str = line[9:19].strip()  # E(level) columns 10-19
        de_str = line[19:21].strip()  # DE columns 20-21
        s_str = line[64:74].strip()  # S columns 65-74
        ds_str = line[74:76].strip() if len(line) > 75 else ''  # DS columns 75-76
        
        # Skip if no S value
        if not s_str or not s_str[0].isdigit():
            continue
        
        # Skip if no DS value
        if not ds_str or not ds_str[0].isdigit():
            continue
            
        try:
            s_val = float(s_str)
            ds_val = ds_str  # DS is the uncertainty value
            
            # Calculate correct E(level)
            e_calc = s_val * FACTOR + SP
            
            # Determine decimal places from S
            if '.' in s_str:
                decimals = len(s_str.split('.')[1])
            else:
                decimals = 0
            
            # Round to match S decimals
            e_correct = round(e_calc, decimals)
            
            # Parse current E(level)
            if not e_str:
                continue
                
            e_current = float(e_str)
            
            # Check if values match (tolerance 0.01 keV for strict checking)
            e_mismatch = abs(e_current - e_correct) > 0.01
            de_mismatch = de_str != ds_val
            
            if e_mismatch or de_mismatch:
                errors.append({
                    'line': line_num,
                    'e_current': e_current,
                    'e_correct': e_correct,
                    'de_current': de_str,
                    'ds_expected': ds_val,
                    's_val': s_val,
                    'decimals': decimals,
                    'e_mismatch': e_mismatch,
                    'de_mismatch': de_mismatch
                })
        except (ValueError, IndexError):
            continue
    
    return errors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_e_level_calculations.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    errors = check_calculations(filename)
    
    if not errors:
        print("All E(level) calculations are correct!")
        sys.exit(0)
    
    print(f"Found {len(errors)} levels that need correction:\n")
    
    for err in errors:
        status = []
        if err['e_mismatch']:
            status.append(f"E: {err['e_current']} -> {err['e_correct']}")
        if err['de_mismatch']:
            status.append(f"DE: '{err['de_current']}' -> '{err['ds_expected']}'")
        
        print(f"Line {err['line']:4d}: {', '.join(status)} (S={err['s_val']}, decimals={err['decimals']})")
    
    print(f"\nTotal errors: {len(errors)}")
    sys.exit(1)
