#!/usr/bin/env python3
"""
Add missing M and S flags to Cl35 ENSDF file based on dataset source analysis.
M flag = 1971Mc23 only
S flag = 1975Sc40 only
No flags = weighted averages from both datasets
"""

import re
import sys

def add_missing_flags():
    """Add missing M and S flags to L-records based on dataset analysis."""
    
    # Lists of energies that need flags (excluding weighted averages)
    missing_M = [3774, 3825, 4372, 4390, 4438, 4454, 4489, 4638, 4693, 4710, 
                 4728, 4779, 4843, 4866, 4922, 4942, 4960, 4982, 5009, 5038, 
                 5075, 5112, 5129, 5157, 5184, 5239, 5254]
    
    missing_S = [5292, 5392, 5403]
    
    filepath = 'd:/X/ND/ENSDF/A35/Cl35/new/Cl35_31p_a_p_a_n_resonances.ens'
    
    print(f"Adding missing flags to {filepath}")
    print(f"M flags to add: {len(missing_M)} levels")
    print(f"S flags to add: {len(missing_S)} levels")
    
    # Read the file
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    modified_lines = []
    flags_added = 0
    
    for line in lines:
        # Check if this is an L-record
        if re.match(r'^ 35CL  L \d+', line):
            match = re.search(r'^ 35CL  L (\d+)', line)
            if match:
                energy = int(match.group(1))
                
                # Check if this energy needs a flag
                if energy in missing_M:
                    # Add M flag at column 77
                    if len(line.rstrip()) < 77:
                        # Pad line to reach column 77
                        new_line = line.rstrip().ljust(76) + 'M' + '\n'
                    else:
                        # Replace character at column 77 with M
                        new_line = line[:76] + 'M' + line[77:]
                    modified_lines.append(new_line)
                    flags_added += 1
                    print(f"Added M flag to {energy} keV level")
                    
                elif energy in missing_S:
                    # Add S flag at column 77
                    if len(line.rstrip()) < 77:
                        # Pad line to reach column 77
                        new_line = line.rstrip().ljust(76) + 'S' + '\n'
                    else:
                        # Replace character at column 77 with S
                        new_line = line[:76] + 'S' + line[77:]
                    modified_lines.append(new_line)
                    flags_added += 1
                    print(f"Added S flag to {energy} keV level")
                    
                else:
                    # No flag needed, keep original line
                    modified_lines.append(line)
            else:
                modified_lines.append(line)
        else:
            # Not an L-record, keep original line
            modified_lines.append(line)
    
    # Write the modified file
    with open(filepath, 'w') as f:
        f.writelines(modified_lines)
    
    print(f"\nCompleted! Added {flags_added} flags total.")
    print(f"Expected: {len(missing_M) + len(missing_S)} flags")
    
    if flags_added == len(missing_M) + len(missing_S):
        print("✅ All missing flags added successfully!")
    else:
        print(f"⚠️  Expected {len(missing_M) + len(missing_S)} but added {flags_added}")

if __name__ == "__main__":
    add_missing_flags()