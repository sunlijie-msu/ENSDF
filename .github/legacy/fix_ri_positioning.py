#!/usr/bin/env python3
"""
Fix RI Field Positioning in ENSDF G-records
============================================

Corrects G-records where RI values start at column 22 instead of column 23.

ENSDF G-Record Format:
- Columns 10-19: Energy (E field)
- Columns 20-21: Energy uncertainty (DE field)  
- Column 22: MUST BE SPACE (readability space)
- Columns 23-29: Relative intensity (RI field) - LEFT-JUSTIFIED at column 23
- Columns 30-31: RI uncertainty (DRI field)

Common Error: RI values shifted left by 1 column (starting at column 22)
This script fixes by inserting a space at column 22.
"""

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python fix_ri_positioning.py filename.ens")
    sys.exit(1)

filename = sys.argv[1]
backup_file = filename + '.backup_before_ri_fix'

print(f"Fixing RI field positioning in: {filename}")
print("=" * 80)

# Create backup
import shutil
shutil.copy2(filename, backup_file)
print(f"Backup created: {backup_file}")
print()

with open(filename, 'r') as f:
    lines = f.readlines()

fixed_lines = []
fixes_made = 0

for line_num, line in enumerate(lines, 1):
    # Check for G-record: column 8='G', columns 6 and 7 are blank
    if len(line) >= 32:
        if line[7] == 'G' and line[5] == ' ' and line[6] == ' ':
            # Check if column 22 (index 21) has non-space character
            # AND columns 23-29 have content (RI field)
            ri_area = line[22:29] if len(line) >= 29 else ''
            
            if line[21] != ' ' and ri_area.strip():
                # RI is shifted left - fix by inserting space at column 22
                # Reconstruct line: keep cols 1-21, insert space, then cols 22-79
                fixed_line = line[:21] + ' ' + line[21:79]
                
                # Ensure exactly 80 characters
                if len(fixed_line) < 80:
                    fixed_line += ' ' * (80 - len(fixed_line))
                elif len(fixed_line) > 80:
                    fixed_line = fixed_line[:80]
                
                fixed_line += '\n'
                fixed_lines.append(fixed_line)
                fixes_made += 1
                
                if fixes_made <= 10:
                    print(f"Fixed line {line_num}:")
                    print(f"  Before: {line.rstrip()}")
                    print(f"  After:  {fixed_line.rstrip()}")
                    print()
            else:
                # No fix needed
                fixed_lines.append(line)
        else:
            # Not a G-record
            fixed_lines.append(line)
    else:
        # Line too short
        fixed_lines.append(line)

# Write fixed file
with open(filename, 'w') as f:
    f.writelines(fixed_lines)

print("=" * 80)
print(f"SUMMARY:")
print(f"  Total lines processed: {len(lines)}")
print(f"  G-records fixed: {fixes_made}")
print(f"  Backup file: {backup_file}")
print()
print("CRITICAL: Run validation tools to verify fixes:")
print(f"  python .github/check_ri_positioning.py \"{filename}\"")
print(f"  python .github/column_calibrate.py \"{filename}\"")
print()

if fixes_made > 0:
    print(f"[OK] Successfully fixed {fixes_made} G-records")
    sys.exit(0)
else:
    print("[OK] No fixes needed")
    sys.exit(0)
