"""
Batch update E(p)(lab) comment lines in Cl34_33s_p_p_resonances.ens
Add {I15} (1989Va15) to all standalone E(p)(lab) values ending with " keV"
Remove " keV" unit from all updated lines
"""

import re
from pathlib import Path

def process_file(filepath):
    """Process the ENSDF file and update E(p)(lab) lines"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified_count = 0
    pattern = re.compile(r'^( 34CL cL \$E\(p\)\(lab\)=)(\d+\.?\d*) keV(\s*)$')
    
    for i, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            prefix = match.group(1)
            value = match.group(2)
            trailing_spaces = match.group(3)
            
            # Build new line: prefix + value + {I15} (1989Va15) + proper spacing for 80 chars
            new_content = f"{prefix}{value} {{I15}} (1989Va15)"
            # Pad to exactly 80 characters
            new_line = f"{new_content:<80}\n"
            
            lines[i] = new_line
            modified_count += 1
            print(f"Line {i+1}: {value} keV → {value} {{I15}} (1989Va15)")
    
    # Write back
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.writelines(lines)
    
    print(f"\n✓ Updated {modified_count} E(p)(lab) lines")
    return modified_count

if __name__ == "__main__":
    target_file = Path(r"d:\X\ND\ENSDF\A34\Cl34\Cl34_33s_p_p_resonances.ens")
    if target_file.exists():
        count = process_file(target_file)
        print(f"\n✓ Task complete: {count} lines updated")
    else:
        print(f"✗ File not found: {target_file}")
