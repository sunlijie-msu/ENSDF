#!/usr/bin/env python3
"""Fix line lengths and ensure proper ENSDF 80-column format."""

from pathlib import Path
import sys

def fix_ensdf_file(filepath):
    """Fix ENSDF file line lengths to exactly 80 characters."""
    
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()
    
    fixed_lines = []
    changes_made = 0
    
    for i, line in enumerate(lines, 1):
        # Remove trailing newline for processing
        clean_line = line.rstrip('\r\n')
        
        # Pad or trim to exactly 80 characters
        if len(clean_line) < 80:
            fixed_line = clean_line.ljust(80)
            if len(clean_line) != len(fixed_line):
                changes_made += 1
                print(f"Line {i}: Padded from {len(clean_line)} to 80 chars")
        elif len(clean_line) > 80:
            fixed_line = clean_line[:80]
            changes_made += 1
            print(f"Line {i}: Trimmed from {len(clean_line)} to 80 chars")
        else:
            fixed_line = clean_line
        
        # Add back newline
        fixed_lines.append(fixed_line + '\n')
    
    # Write back
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.writelines(fixed_lines)
    
    print(f"\nTotal lines fixed: {changes_made}")
    return changes_made

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fix_line_lengths.py <file.ens>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    changes = fix_ensdf_file(filepath)
    sys.exit(0 if changes >= 0 else 1)
