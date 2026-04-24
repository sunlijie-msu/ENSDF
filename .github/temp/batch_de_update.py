#!/usr/bin/env python3
"""
Batch update DE field for all G-records with integer energies.
Reads file, makes all replacements in memory, validates, then writes.
"""

file_path = "A34/Cl34/new/Cl34_27al_12c_ang.ens"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Track updates
updated_count = 0
total_count = len(lines)
error_count = 0

print(f"Processing {total_count} lines...")
print()

# Process each line
for i, line in enumerate(lines):
    line_num = i + 1
    line_stripped = line.rstrip('\n')
    
    # Check if it's a G-record
    if len(line_stripped) >= 21 and line_stripped[7:8] == 'G':
        # Extract energy (columns 10-19, 0-indexed: 9-19)
        if len(line_stripped) >= 19:
            energy_str = line_stripped[9:19]
            energy_trimmed = energy_str.strip()
            
            # Check if integer energy
            if energy_trimmed and energy_trimmed.isdigit() and '.' not in energy_trimmed:
                # Check if DE field is blank (columns 20-21, 0-indexed: 19-21)
                if len(line_stripped) >= 21:
                    de_field = line_stripped[19:21]
                    if de_field == '  ':
                        # Update DE field
                        new_line = line_stripped[:19] + '1 ' + line_stripped[21:]
                        
                        # Validate length
                        if len(new_line) == 80:
                            lines[i] = new_line + '\n'
                            updated_count += 1
                            print(f"✓ Line {line_num}: Energy={energy_trimmed}")
                        else:
                            print(f"✗ Line {line_num}: Length mismatch ({len(new_line)} != 80)")
                            error_count += 1

print()
print(f"Updated: {updated_count} lines")
print(f"Errors: {error_count} lines")
print()

# Write the file
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"File written: {file_path}")
print(f"Total lines in file: {len(lines)}")
