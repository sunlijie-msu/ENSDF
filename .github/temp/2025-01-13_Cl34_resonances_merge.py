"""
Merge E(p)(lab) comment lines from 1989Va15 and 1964Va12 in Cl34_33s_p_p_resonances.ens
Find pairs where 1989Va15 line is immediately followed by 1964Va12 line
Merge into single line and delete the secondary 1964Va12 line
"""

import re
from pathlib import Path

def process_file(filepath):
    """Process the ENSDF file and merge E(p)(lab) pairs"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    merged_count = 0
    i = 0
    while i < len(lines) - 1:
        # Pattern for 1989Va15 line (already updated)
        pattern_1989 = re.compile(r'^( 34CL cL \$E\(p\)\(lab\)=)(\d+\.?\d*) \{I15\} \(1989Va15\)(\s*)$')
        # Pattern for 1964Va12 line (starts with $ space)
        pattern_1964 = re.compile(r'^( 34CL cL \$ E\(p\)\(lab\)=)(\d+) (\{I\d+\}) \(1964Va12\)(.*?)(\s*)$')
        
        match_1989 = pattern_1989.match(lines[i])
        match_1964 = pattern_1964.match(lines[i+1])
        
        if match_1989 and match_1964:
            # Extract values
            prefix = match_1989.group(1)
            value_1989 = match_1989.group(2)
            value_1964 = match_1964.group(2)
            uncert_1964 = match_1964.group(3)
            extra_text = match_1964.group(4).strip()  # e.g., "; could be a mixture..."
            
            # Build merged line
            if extra_text:
                # If extra text exists, we need to handle it
                merged_content = f"{prefix}{value_1989} {{I15}} (1989Va15), {value_1964} {uncert_1964} (1964Va12)"
                # Check if it fits in 80 chars
                if len(merged_content) + len(f"; {extra_text}") <= 80:
                    merged_line = f"{merged_content}; {extra_text:<{80 - len(merged_content) - 2}}\n"
                else:
                    # Create continuation line for extra text
                    merged_line = f"{merged_content:<80}\n"
                    # We won't add continuation for now - just report it
                    print(f"Line {i+1}: NEEDS MANUAL HANDLING - extra text: {extra_text}")
                    i += 1
                    continue
            else:
                merged_content = f"{prefix}{value_1989} {{I15}} (1989Va15), {value_1964} {uncert_1964} (1964Va12)"
                merged_line = f"{merged_content:<80}\n"
            
            # Replace current line with merged line
            lines[i] = merged_line
            # Delete next line
            lines.pop(i+1)
            merged_count += 1
            print(f"Line {i+1}: Merged {value_1989} (1989Va15) + {value_1964} (1964Va12)")
        
        i += 1
    
    # Write back
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.writelines(lines)
    
    print(f"\n✓ Merged {merged_count} E(p)(lab) line pairs")
    return merged_count

if __name__ == "__main__":
    target_file = Path(r"d:\X\ND\ENSDF\A34\Cl34\Cl34_33s_p_p_resonances.ens")
    if target_file.exists():
        count = process_file(target_file)
        print(f"\n✓ Task complete: {count} line pairs merged")
    else:
        print(f"✗ File not found: {target_file}")
