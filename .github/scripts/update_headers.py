#!/usr/bin/env python3
"""Update ENSDF file headers to new evaluation format.
Replaces old header (cols 75-80) and inserts new H line after line 1.
"""
import os
import sys
import re

def get_nucid(line):
    """Extract NUCID from first 5 columns."""
    if len(line) >= 5:
        return line[:5]
    return None

def update_header(filepath):
    """Update header in an ENSDF file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    
    if not lines:
        return False, "Empty file"
    
    # Get NUCID from line 1
    line1 = lines[0].rstrip('\n\r')
    nucid = get_nucid(line1)
    if not nucid:
        return False, "Cannot extract NUCID"
    
    # Check if already correctly updated (exactly 80 chars with ENSDF header)
    if len(line1) == 80 and 'ENSDF    202609' in line1[74:]:
        # Check if H line already exists
        if len(lines) > 1 and 'LIJIE SUN AND JUN CHEN' in lines[1]:
            return False, "Already updated"
    
    # Build new line 1: take first 65 chars, pad to 65, then add "ENSDF    202609"
    # Cols 1-65 contain dataset info, cols 66-74 often have DSID ref, cols 75-80 have DSREF
    # We need cols 1-65 preserved, then pad, then ENSDF header at 75-80
    
    # Take first 65 characters (or pad if shorter)
    base_content = line1[:65].ljust(65)
    
    # For cols 66-74 (9 chars), try to preserve reference if exists, else space
    if len(line1) >= 74:
        ref_part = line1[65:74]
    else:
        ref_part = "         "
    
    # New line 1 = base(65) + ref(9) + "ENSDF    202609"(15 chars = cols 75-89? No, should be 80 total)
    # Wait - ENSDF format: cols 75-80 = DSREF (6 chars), but we're using "ENSDF    202609" which is 15 chars
    # Let me check the reference file format again
    # Looking at Ar34_adopted.ens: line ends with "ENSDF    202609" 
    # That's 15 chars. So cols 66-80 = 15 chars total
    
    # Build: cols 1-65 (65 chars) + cols 66-80 (15 chars) = 80 chars total
    new_line1 = base_content + "ENSDF    202609"  # 65 + 15 = 80
    
    # Build new H line (line 2)
    new_h_line = f"{nucid}  H TYP=FUL$AUT=LIJIE SUN AND JUN CHEN$CIT=ENSDF$CUT=30-Sep-2026$"
    new_h_line = new_h_line.ljust(80)
    
    # Check if line 2 already has our new H line
    if len(lines) > 1:
        line2 = lines[1].rstrip('\n\r')
        if 'LIJIE SUN AND JUN CHEN' in line2:
            # Just update line 1
            lines[0] = new_line1 + '\n'
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            return True, "Updated line 1 only (H line exists)"
    
    # Insert new H line after line 1
    new_lines = [new_line1 + '\n', new_h_line + '\n'] + lines[1:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return True, "Updated header and inserted H line"

def main():
    if len(sys.argv) < 2:
        print("Usage: python update_headers.py <directory>")
        sys.exit(1)
    
    base_dir = sys.argv[1]
    
    # Find all .ens files in new/ subdirectories
    updated = 0
    skipped = 0
    errors = 0
    
    for root, dirs, files in os.walk(base_dir):
        # Only process files in 'new' folders
        if 'new' not in root:
            continue
        
        for fname in files:
            if fname.endswith('.ens'):
                filepath = os.path.join(root, fname)
                try:
                    success, msg = update_header(filepath)
                    if success:
                        print(f"[OK] {filepath}: {msg}")
                        updated += 1
                    else:
                        print(f"[SKIP] {filepath}: {msg}")
                        skipped += 1
                except Exception as e:
                    print(f"[ERR] {filepath}: {e}")
                    errors += 1
    
    print(f"\nSummary: {updated} updated, {skipped} skipped, {errors} errors")

if __name__ == '__main__':
    main()
