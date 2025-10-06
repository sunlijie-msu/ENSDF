#!/usr/bin/env python3
"""
Comprehensive fix for M, MR, DMR field positioning in ENSDF G-records.

ROOT PROBLEM: M field starts at column 32 instead of 33, causing cascade of errors.

FIX STRATEGY:
1. Detect G-records where col 32 has non-space (M field starting early)
2. Extract all field values carefully
3. Rebuild line with correct field positions:
   - Col 32: SPACE (mandatory)
   - Cols 33-41: M field (LEFT-JUSTIFIED)
   - Cols 42-49: MR field (LEFT-JUSTIFIED)
   - Cols 50-55: DMR field (LEFT-JUSTIFIED)
   - All other fields: preserved at correct positions
"""

import sys


def fix_g_record_fields(filename):
    """Fix M, MR, DMR field positioning in G-records."""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    fixed_lines = []
    
    for line_num, line in enumerate(lines, start=1):
        original_line = line
        line_content = line.rstrip('\n')
        
        # Skip non-G-records or lines too short
        if len(line_content) < 41:
            fixed_lines.append(original_line)
            continue
        
        # ONLY fix G-records (not cG comment lines)
        if not (len(line_content) >= 9 and line_content[7] == 'G' and 
                line_content[8] == ' ' and line_content[6] == ' '):
            fixed_lines.append(original_line)
            continue
        
        # Pad to exactly 80 characters
        padded_line = line_content.ljust(80, ' ')
        
        # Check if col 32 has non-space (M field starting early)
        col32 = padded_line[31]
        m_field_raw = padded_line[32:41]
        
        if col32 != ' ' and m_field_raw.strip():
            # ERROR DETECTED: M field starts at col 32
            # Extract ALL fields from CURRENT (wrong) positions
            
            # Fields that are CORRECT (before M field):
            nucid = padded_line[0:5]
            cont = padded_line[5]
            blank7 = padded_line[6]
            g_type = padded_line[7]
            blank9 = padded_line[8]
            e_field = padded_line[9:19]
            de_field = padded_line[19:21]
            space22 = padded_line[21]
            ri_field = padded_line[22:29]
            dri_field = padded_line[29:31]
            # Col 32 currently has first char of M field (WRONG)
            
            # Extract M, MR, DMR from WRONG positions (shifted left by 1)
            # M field: currently at cols 32-40 (should be 33-41)
            m_value = (col32 + padded_line[32:40]).strip()
            
            # MR field: currently at cols 41-48 (should be 42-49)
            mr_value = padded_line[40:48].strip()
            
            # DMR field: currently at cols 49-54 (should be 50-55)
            dmr_value = padded_line[48:54].strip()
            
            # Fields after DMR (also shifted):
            # CC field: currently at cols 55-61 (should be 56-62)
            cc_value = padded_line[54:61].strip()
            
            # DCC field: currently at cols 62-63 (should be 63-64)
            dcc_value = padded_line[61:63].strip()
            
            # TI field: currently at cols 64-73 (should be 65-74)
            ti_value = padded_line[63:73].strip()
            
            # DTI field: currently at cols 74-75 (should be 75-76)
            dti_value = padded_line[73:75].strip()
            
            # C field: currently at col 76 (should be 77)
            c_flag = padded_line[75] if len(padded_line) > 75 else ' '
            
            # Q field: currently at col 79 (should be 80)
            q_flag = padded_line[78] if len(padded_line) > 78 else ' '
            
            # Now rebuild line with CORRECT positions and LEFT-JUSTIFICATION
            
            # M field (cols 33-41): LEFT-JUSTIFIED
            m_fixed = m_value.ljust(9, ' ') if m_value else ' ' * 9
            
            # MR field (cols 42-49): LEFT-JUSTIFIED
            mr_fixed = mr_value.ljust(8, ' ') if mr_value else ' ' * 8
            
            # DMR field (cols 50-55): LEFT-JUSTIFIED
            dmr_fixed = dmr_value.ljust(6, ' ') if dmr_value else ' ' * 6
            
            # CC field (cols 56-62): LEFT-JUSTIFIED
            cc_fixed = cc_value.ljust(7, ' ') if cc_value else ' ' * 7
            
            # DCC field (cols 63-64): LEFT-JUSTIFIED
            dcc_fixed = dcc_value.ljust(2, ' ') if dcc_value else ' ' * 2
            
            # TI field (cols 65-74): LEFT-JUSTIFIED
            ti_fixed = ti_value.ljust(10, ' ') if ti_value else ' ' * 10
            
            # DTI field (cols 75-76): LEFT-JUSTIFIED
            dti_fixed = dti_value.ljust(2, ' ') if dti_value else ' ' * 2
            
            # C field (col 77): single character
            c_fixed = c_flag if c_flag in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*&@' else ' '
            
            # Cols 78-79: MUST be spaces
            blank78_79 = '  '
            
            # Q field (col 80): single character
            q_fixed = q_flag if q_flag in '?S' else ' '
            
            # Build complete 80-character line
            fixed_line = (nucid + cont + blank7 + g_type + blank9 +
                         e_field + de_field + space22 +
                         ri_field + dri_field +
                         ' ' +  # Col 32: MANDATORY SPACE
                         m_fixed + mr_fixed + dmr_fixed +
                         cc_fixed + dcc_fixed +
                         ti_fixed + dti_fixed +
                         c_fixed + blank78_79 + q_fixed)
            
            # Verify length
            if len(fixed_line) != 80:
                print(f"ERROR Line {line_num}: Fixed line length is {len(fixed_line)}, expected 80")
                print(f"  M='{m_value}' MR='{mr_value}' DMR='{dmr_value}'")
                fixed_lines.append(original_line)
                continue
            
            fixed_lines.append(fixed_line + '\n')
            fixed_count += 1
            
            if fixed_count <= 3:  # Show first 3 fixes
                print(f"\nLine {line_num} fixed:")
                print(f"  BEFORE: {padded_line}")
                print(f"  AFTER:  {fixed_line}")
                print(f"  M='{m_value}' MR='{mr_value}' DMR='{dmr_value}'")
        else:
            # Line is correct, keep as-is
            fixed_lines.append(original_line)
    
    # Write fixed file
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(fixed_lines)
    
    return fixed_count


if __name__ == "__main__":
    filename = r'A35\Cl35\new\Cl35_34s_p_g.ens'
    
    print("="*80)
    print("COMPREHENSIVE M/MR/DMR FIELD FIX")
    print("="*80)
    print("\nFixing G-records where M field starts at col 32 instead of 33...")
    print("This also fixes MR and DMR field LEFT-JUSTIFICATION.\n")
    
    fixed_count = fix_g_record_fields(filename)
    
    print("\n" + "="*80)
    if fixed_count > 0:
        print(f"SUCCESS: Fixed {fixed_count} G-records")
        print("\nCorrected fields:")
        print("  - Col 32: Now has mandatory SPACE")
        print("  - M field (cols 33-41): LEFT-JUSTIFIED")
        print("  - MR field (cols 42-49): LEFT-JUSTIFIED")
        print("  - DMR field (cols 50-55): LEFT-JUSTIFIED")
        print("  - All subsequent fields: Correct positions")
    else:
        print("No errors found - file already correct")
    print("="*80)
    
    sys.exit(0)
