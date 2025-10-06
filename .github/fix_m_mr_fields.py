#!/usr/bin/env python3
"""
Fix M and MR field positioning errors in ENSDF G-records.
CRITICAL: LEFT-JUSTIFY M (cols 33-41) and MR (cols 42-49) fields.

M field errors: M values shifted right (have leading space)
MR field errors: MR values shifted right (have leading space)

This script:
1. Creates backup before any changes
2. Processes ONLY G-records
3. LEFT-JUSTIFIES M field in columns 33-41
4. LEFT-JUSTIFIES MR field in columns 42-49
5. Preserves all other field values exactly
"""

import sys
import shutil
from datetime import datetime


def fix_m_mr_fields(filename):
    """Fix M and MR field positioning errors."""
    
    # Create backup
    backup_name = f"{filename}.backup_before_m_mr_fix"
    shutil.copy2(filename, backup_name)
    print(f"Backup created: {backup_name}\n")
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Processing {filename}...")
    print(f"Total lines: {len(lines)}\n")
    
    m_fixed = 0
    mr_fixed = 0
    both_fixed = 0
    
    for i, original_line in enumerate(lines, start=1):
        # Skip non-G-records or lines too short
        if len(original_line) < 41:  # Need at least up to M field
            continue
        
        if not (original_line[7] == 'G' and original_line[8] == ' '):
            continue
        
        # Work with padded line for safety
        fixed_line = original_line.ljust(80, ' ')
        line_modified = False
        m_field_fixed = False
        mr_field_fixed = False
        
        # Extract M field (columns 33-41, 0-indexed: 32-41)
        m_field = fixed_line[32:41]
        
        # Check if M field needs LEFT-JUSTIFICATION
        if m_field and m_field[0] == ' ' and m_field.strip():
            # M field has leading space - need to left-justify
            m_value = m_field.strip()
            m_fixed_field = m_value.ljust(9, ' ')  # 9 chars for cols 33-41
            
            # Replace M field
            fixed_line = fixed_line[:32] + m_fixed_field + fixed_line[41:]
            line_modified = True
            m_field_fixed = True
        
        # Extract MR field (columns 42-49, 0-indexed: 41-49)
        if len(original_line) >= 49:
            mr_field = fixed_line[41:49]
            
            # Check if MR field needs LEFT-JUSTIFICATION
            if mr_field and mr_field[0] == ' ' and mr_field.strip():
                # MR field has leading space - need to left-justify
                mr_value = mr_field.strip()
                mr_fixed_field = mr_value.ljust(8, ' ')  # 8 chars for cols 42-49
                
                # Replace MR field
                fixed_line = fixed_line[:41] + mr_fixed_field + fixed_line[49:]
                line_modified = True
                mr_field_fixed = True
        
        # Update line if modified
        if line_modified:
            # Trim to original line length or 80, whichever is longer
            if fixed_line.rstrip() != original_line.rstrip():
                lines[i - 1] = fixed_line.rstrip() + '\n'
                
                # Count what was fixed
                if m_field_fixed and mr_field_fixed:
                    both_fixed += 1
                    print(f"Line {i}: Both M and MR fields left-justified")
                    print(f"  BEFORE: {original_line.rstrip()}")
                    print(f"  AFTER:  {fixed_line.rstrip()}\n")
                elif m_field_fixed:
                    m_fixed += 1
                    print(f"Line {i}: M field left-justified")
                    print(f"  BEFORE: {original_line.rstrip()}")
                    print(f"  AFTER:  {fixed_line.rstrip()}\n")
                elif mr_field_fixed:
                    mr_fixed += 1
                    print(f"Line {i}: MR field left-justified")
                    print(f"  BEFORE: {original_line.rstrip()}")
                    print(f"  AFTER:  {fixed_line.rstrip()}\n")
    
    # Write fixed file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("\nSUMMARY:")
    print(f"  M field only fixed: {m_fixed}")
    print(f"  MR field only fixed: {mr_fixed}")
    print(f"  Both M and MR fixed: {both_fixed}")
    print(f"  Total lines fixed: {m_fixed + mr_fixed + both_fixed}")
    print(f"  File updated: {filename}")
    print(f"  Backup saved: {backup_name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_m_mr_fields.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    fix_m_mr_fields(filename)


if __name__ == "__main__":
    main()
