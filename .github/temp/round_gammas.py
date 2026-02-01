import sys
import os

filepath = r"d:\X\ND\ENSDF\XUNDL\2026TAAA_CLR1074_173W.ens"

with open(filepath, 'r') as f:
    lines = f.readlines()

new_lines = []
stop_modifying = False

count_modified = 0

for i, line in enumerate(lines):
    original_line = line
    
    # Check stop conditions
    if "DO NOT EDIT BELOW THIS LINE" in line or "173W   L 1877.7" in line:
        stop_modifying = True
        print(f"Stopped modifying at line {i+1}")
    
    # Process only if not stopped
    if not stop_modifying:
        # Check if G record (Col 8 = 'G', Col 6 = ' ')
        # Indexes: Col 1=0, Col 6=5, Col 8=7
        if len(line) > 8 and line[7] == 'G' and line[5] == ' ':
            # E field: cols 10-19 (indices 9-19)
            # DE field: cols 20-21 (indices 19-21)
            
            e_str = line[9:19]
            print(f"Processing line {i+1}: G record found. E='{e_str}'")
            
            # Check if E is non-empty
            if e_str.strip():
                try:
                    e_val = float(e_str)
                    # Round specific logic
                    e_round = int(round(e_val))
                    e_new_str = f"{e_round:<10}" # Left justified 10 chars
                    
                    # Reconstruct line
                    # Prefix: 0-8 (cols 1-9)
                    prefix = line[:9]
                    
                    # Suffix: 21 onwards (col 22 onwards)
                    # Use slicing carefully
                    if len(line) < 21:
                        # Pad checks if needed, but usually lines are 80
                        suffix = " " * (80 - 21) + "\n" 
                    else:
                        suffix = line[21:]
                    
                    # Construct new line: Prefix + Rounded E + 2 Spaces (Clear DE) + Suffix
                    new_line_content = prefix + e_new_str + "  " + suffix
                    
                    # Ensure strict 80 columns padding
                    new_line_content = new_line_content.rstrip('\n')
                    if len(new_line_content) < 80:
                        new_line_content = new_line_content + " " * (80 - len(new_line_content))
                    
                    # Add newline char
                    new_lines.append(new_line_content + "\n")
                    count_modified += 1
                except ValueError:
                    # Not a float, assume not an Energy value
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open(filepath, 'w') as f:
    f.writelines(new_lines)

print(f"Modified {count_modified} records.")
