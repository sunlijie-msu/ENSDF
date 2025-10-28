#!/usr/bin/env python3
"""
Fix E(level) = S * 0.9711849866847 + 6370.81 calculations in ENSDF file.
Also ensures DE = DS for all levels with S values.
"""

import sys
import shutil
from datetime import datetime

def fix_calculations(filename):
    """Fix all E(level) and DE values to match S and DS."""
    
    # Constants
    FACTOR = 0.9711849866847
    SP = 6370.81
    
    # Read file
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Create backup
    backup = filename + '.backup_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2(filename, backup)
    print(f"Created backup: {backup}")
    
    corrections = []
    
    for line_num, line in enumerate(lines):
        if not line.startswith(' 35CL  L') or len(line) < 74:
            continue
            
        # Extract fields (columns are 1-indexed in ENSDF, 0-indexed in Python)
        e_str = line[9:19].strip()  # E(level) columns 10-19
        de_str = line[19:21].strip()  # DE columns 20-21
        s_str = line[64:74].strip()  # S columns 65-74
        ds_str = line[74:76].strip() if len(line) > 75 else ''  # DS columns 75-76
        
        # Skip if no S or DS value
        if not s_str or not s_str[0].isdigit():
            continue
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
            
            # Check if corrections needed
            e_mismatch = abs(e_current - e_correct) > 0.01
            de_mismatch = de_str != ds_val
            
            if e_mismatch or de_mismatch:
                # Build new line with corrections
                new_line = line
                
                # Fix E(level) if needed
                if e_mismatch:
                    # Format E with correct decimal places
                    e_new_str = f"{e_correct:.{decimals}f}"
                    # Left-justify in 10-character field (columns 10-19)
                    e_field = e_new_str.ljust(10)
                    new_line = new_line[:9] + e_field + new_line[19:]
                
                # Fix DE if needed  
                if de_mismatch:
                    # DE is 2-character field (columns 20-21), left-justified
                    de_field = ds_val.ljust(2)
                    new_line = new_line[:19] + de_field + new_line[21:]
                
                # Record correction
                corrections.append({
                    'line_num': line_num + 1,  # 1-indexed for display
                    'old': line.rstrip(),
                    'new': new_line.rstrip(),
                    'e_old': e_current if e_mismatch else None,
                    'e_new': e_correct if e_mismatch else None,
                    'de_old': de_str if de_mismatch else None,
                    'de_new': ds_val if de_mismatch else None,
                    's_val': s_val
                })
                
                # Update line in array
                lines[line_num] = new_line
                
        except (ValueError, IndexError) as e:
            print(f"Warning: Error processing line {line_num + 1}: {e}")
            continue
    
    if not corrections:
        print("No corrections needed - all values are correct!")
        return 0
    
    # Write corrected file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\nMade {len(corrections)} corrections:\n")
    
    for i, corr in enumerate(corrections, 1):
        changes = []
        if corr['e_old'] is not None:
            changes.append(f"E: {corr['e_old']} -> {corr['e_new']}")
        if corr['de_old'] is not None:
            changes.append(f"DE: '{corr['de_old']}' -> '{corr['de_new']}'")
        
        print(f"{i:3d}. Line {corr['line_num']:4d}: {', '.join(changes)} (S={corr['s_val']})")
    
    print(f"\nTotal corrections: {len(corrections)}")
    print(f"File updated: {filename}")
    print(f"Backup saved: {backup}")
    
    return len(corrections)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_e_level_calculations.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    num_corrections = fix_calculations(filename)
    
    if num_corrections > 0:
        print("\nIMPORTANT: Run validation tools:")
        print("  python .github\\ensdf_1line_ruler.py --file \"" + filename + "\" --show-only-wrong")
        print("  python .github\\column_calibrate.py \"" + filename + "\"")
        print("  python .github\\check_e_level_calculations.py \"" + filename + "\"")
    
    sys.exit(0)
