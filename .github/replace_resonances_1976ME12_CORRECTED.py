"""
Replace incorrect resonance records in 1976ME12.ens with CORRECTED versions.

The current file has WRONG field mappings:
- Ep in S field, but dEp is missing in DS field
- Ex has uncertainty in DE field when it should be blank

CORRECTED mappings:
- Ex → E field (exact, no DE uncertainty)  
- Ep → S field (columns 65-74)
- dEp → DS field (columns 75-76, max 2 digits)
"""

def replace_resonances():
    main_file = "A35/Cl35/temp/1976ME12.ens"
    corrected_file = "A35/Cl35/temp/1976ME12_resonances_CORRECTED.txt"
    output_file = "A35/Cl35/temp/1976ME12.ens"
    
    # Read main file
    with open(main_file, 'r', encoding='utf-8') as f:
        main_lines = f.readlines()
    
    # Read corrected resonance file
    with open(corrected_file, 'r', encoding='utf-8') as f:
        corrected_lines = f.readlines()
    
    # Filter corrected resonance lines (skip header comments starting with '#')
    filtered_corrected = [line for line in corrected_lines if not line.startswith('#')]
    
    # Find the resonance section boundaries
    # Start: line after " 35CL  G 6493         100"
    # End: line before "Original Branching Ratio data from 1976Me12:"
    
    start_marker = " 35CL  G 6493         100"
    end_marker = "Original Branching Ratio data from 1976Me12:"
    
    start_index = None
    end_index = None
    
    for i, line in enumerate(main_lines):
        if start_marker in line:
            # Find next blank line after this G-record
            for j in range(i+1, len(main_lines)):
                if main_lines[j].strip() == "":
                    start_index = j + 1  # Insert after the blank line
                    break
        if end_marker in line:
            # Find previous blank lines before this marker
            for j in range(i-1, -1, -1):
                if main_lines[j].strip() != "":
                    end_index = j + 1  # Keep blank lines before marker
                    break
            break
    
    if start_index is None or end_index is None:
        print(f"[ERROR] Could not find resonance section boundaries")
        print(f"[INFO] start_index: {start_index}, end_index: {end_index}")
        return False
    
    print(f"[OK] Found resonance section: lines {start_index}-{end_index} ({end_index - start_index} lines)")
    print(f"[OK] Will replace with {len(filtered_corrected)} corrected lines")
    
    # Create new file: before + corrected resonances + after
    new_lines = main_lines[:start_index] + filtered_corrected + main_lines[end_index:]
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        f.writelines(new_lines)
    
    original_count = len(main_lines)
    new_count = len(new_lines)
    replaced_count = end_index - start_index
    
    print(f"[OK] Original file: {original_count} lines")
    print(f"[OK] Replaced: {replaced_count} lines with {len(filtered_corrected)} corrected lines")
    print(f"[OK] New file: {new_count} lines")
    print(f"[OK] Successfully updated {output_file}")
    
    return True

if __name__ == "__main__":
    success = replace_resonances()
    if not success:
        exit(1)
