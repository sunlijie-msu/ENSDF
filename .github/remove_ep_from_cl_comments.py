#!/usr/bin/env python3
"""
Remove Ep information from cL comments in 1976ME12.ens

Changes:
  (1976Me12,Ep=716 keV) -> (1976Me12)
  
Maintains 80-character line length by padding with spaces.
"""

import re
import sys

def remove_ep_from_cl_comments(filepath):
    """Remove Ep information from cL comments."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified_count = 0
    pattern = re.compile(r'(\$\|w\|g=.*?eV\s+\{I\d+\})\s+\(1976Me12,Ep=[^\)]+\)')
    
    new_lines = []
    for i, line in enumerate(lines, 1):
        if 'cL $|w|g=' in line and '(1976Me12,Ep=' in line:
            # Find and replace the pattern
            match = pattern.search(line)
            if match:
                # Extract the part before (1976Me12,Ep=...)
                before_ref = line[:match.start()] + match.group(1) + ' (1976Me12)'
                # Pad to 80 characters
                new_line = before_ref.ljust(80) + '\n'
                
                print(f"Line {i}:")
                print(f"  OLD: {line.rstrip()}")
                print(f"  NEW: {new_line.rstrip()}")
                
                new_lines.append(new_line)
                modified_count += 1
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\nTotal lines modified: {modified_count}")
    return modified_count

if __name__ == '__main__':
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'A35/Cl35/temp/1976ME12.ens'
    
    count = remove_ep_from_cl_comments(filepath)
    print(f"\nSuccessfully removed Ep information from {count} cL comments in {filepath}")
