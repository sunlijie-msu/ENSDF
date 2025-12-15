import sys
import os

def pad_line(line):
    return line.ljust(80)[:80]

def main():
    file_path = r'd:\X\ND\ENSDF\XUNDL\2025DOAA_CL10995_209Po.ens'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    modified_indices = []
    
    for i, line in enumerate(lines):
        original_line = line.rstrip('\n')
        new_line = original_line
        
        # Fix 1: E=2340.0
        if original_line.startswith('209PO  L 2340.0    2'):
            # Check if J is empty (it should be empty or spaces)
            # J starts at col 23 (index 22)
            if len(original_line) < 23 or original_line[22:].strip() == '':
                # Construct new line
                # Keep first 22 chars (0-21)
                prefix = original_line[:22].ljust(22)
                # Add J
                j_val = "5/2-,7/2-"
                # Construct
                # 209PO  L 2340.0    2  5/2-,7/2-
                # 01234567890123456789012
                # Prefix is 22 chars.
                # "209PO  L 2340.0    2 "
                new_content = prefix + j_val
                new_line = pad_line(new_content)
                print(f"Modifying line {i+1}: Added J '{j_val}'")
                modified_indices.append(i)

        # Fix 2: E=2835.9
        elif '209PO  L 2835.9    2  (9/2+, 11/2-)' in original_line:
            new_content = original_line.replace('(9/2+, 11/2-)', '(9/2+,11/2-)')
            new_line = pad_line(new_content)
            print(f"Modifying line {i+1}: Removed space in J")
            modified_indices.append(i)
            
        new_lines.append(new_line + '\n')
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print("File updated.")

if __name__ == '__main__':
    main()
