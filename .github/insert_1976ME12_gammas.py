#!/usr/bin/env python3
"""
Insert G-records into 1976ME12.ens file after each L+cL pair.

Logic:
1. Read main file (1976ME12.ens)
2. Read generated G-records (1976ME12_gammas_generated.txt)
3. Parse G-records grouped by Ep value
4. For each L-record with matching S field (Ep):
   - Find the L-record line
   - Find the cL comment line (next line)
   - Insert blank line + G-records + blank line after cL
5. Write updated file
"""

import re

def extract_s_field(line):
    """Extract S field value (columns 65-74) from L-record."""
    if len(line) < 74:
        return None
    s_field = line[64:74].strip()
    if s_field:
        try:
            return float(s_field)
        except ValueError:
            return None
    return None

def main():
    # Read main file
    main_file = "A35/Cl35/temp/1976ME12.ens"
    with open(main_file, 'r') as f:
        main_lines = f.readlines()
    
    # Strip newlines for processing
    main_lines = [line.rstrip('\n') for line in main_lines]
    
    print(f"[*] Read {len(main_lines)} lines from {main_file}")
    
    # Read generated G-records
    gamma_file = "A35/Cl35/temp/1976ME12_gammas_generated.txt"
    with open(gamma_file, 'r') as f:
        gamma_lines = f.readlines()
    
    gamma_lines = [line.rstrip('\n') for line in gamma_lines]
    
    # Parse G-records grouped by Ep
    gamma_groups = {}  # {Ep_keV: [G-record lines]}
    current_ep = None
    current_group = []
    
    for line in gamma_lines:
        if line.startswith('# Ep='):
            # Save previous group
            if current_ep is not None and current_group:
                gamma_groups[current_ep] = current_group
            
            # Extract Ep from comment: "# Ep=716 keV, Ex=7069 keV (10 gammas)"
            match = re.search(r'Ep=(\d+)', line)
            if match:
                current_ep = float(match.group(1))
                current_group = []
        elif line.startswith(' 35CL  G'):
            # G-record line
            current_group.append(line)
    
    # Don't forget last group
    if current_ep is not None and current_group:
        gamma_groups[current_ep] = current_group
    
    print(f"[*] Parsed {len(gamma_groups)} gamma groups")
    
    # Process main file and insert G-records
    new_lines = []
    i = 0
    gammas_inserted = 0
    
    while i < len(main_lines):
        line = main_lines[i]
        new_lines.append(line)
        
        # Check if this is an L-record with S field (resonance level)
        if line.startswith(' 35CL  L') and len(line) >= 74:
            s_value = extract_s_field(line)
            
            # Match with tolerance (S field has decimals, CSV has integers)
            if s_value:
                # Find closest match within 1 keV tolerance
                matched_ep = None
                for ep_key in gamma_groups.keys():
                    if abs(s_value - ep_key) < 1.0:
                        matched_ep = ep_key
                        break
                
                if matched_ep:
                    # Found matching L-record
                    # Next line should be cL comment
                    if i + 1 < len(main_lines):
                        cl_line = main_lines[i + 1]
                        new_lines.append(cl_line)
                        i += 1
                        
                        # Insert blank line, then G-records, then blank line
                        new_lines.append("")  # Blank before G-records
                        new_lines.extend(gamma_groups[matched_ep])
                        # Don't add blank after - it should already exist in original
                        
                        gammas_inserted += len(gamma_groups[matched_ep])
                        
                        print(f"[+] Inserted {len(gamma_groups[matched_ep])} G-records after Ep={s_value} keV (Ex line {i})")
        
        i += 1
    
    # Write updated file
    output_file = "A35/Cl35/temp/1976ME12_with_gammas.ens"
    with open(output_file, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print(f"[OK] Inserted {gammas_inserted} G-records into {len(gamma_groups)} levels")
    print(f"[OK] Original file: {len(main_lines)} lines")
    print(f"[OK] New file: {len(new_lines)} lines")
    print(f"[OK] Output: {output_file}")

if __name__ == "__main__":
    main()
