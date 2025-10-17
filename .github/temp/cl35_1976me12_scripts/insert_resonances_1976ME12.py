"""
Insert 112 resonance records (56 L-records + 56 cL comments) into 1976ME12.ens
Insertion point: After line with "6493" L-record, before "Original Branching Ratio data" section
"""

# Read main ENSDF file
with open("A35/Cl35/temp/1976ME12.ens", 'r', encoding='utf-8') as f:
    main_lines = f.readlines()

# Read resonance data file
with open("A35/Cl35/temp/1976ME12_resonances.txt", 'r', encoding='utf-8') as f:
    resonance_lines = f.readlines()

# Filter out comment lines and blank lines from resonance file
# Keep only actual ENSDF records (L-records and cL comments) and their blank separators
filtered_resonance_lines = []
for line in resonance_lines:
    # Skip comment lines starting with '#'
    if line.startswith('#'):
        continue
    # Keep ENSDF records (start with space) and blank lines
    filtered_resonance_lines.append(line)

# Find insertion point: after the "6493" L-record
insertion_index = None
for i, line in enumerate(main_lines):
    # Look for L-record with energy 6493
    if line.startswith(' 35CL  L 6493'):
        # Find the end of this level's records (next blank line or end of file)
        j = i + 1
        while j < len(main_lines) and main_lines[j].strip():
            j += 1
        insertion_index = j
        break

if insertion_index is None:
    print("[ERROR] Could not find '6493' L-record insertion point!")
    exit(1)

print(f"[OK] Found insertion point at line {insertion_index + 1}")
print(f"[OK] Current line count: {len(main_lines)}")
print(f"[OK] Resonance lines to insert: {len(filtered_resonance_lines)}")

# Insert resonance data
updated_lines = main_lines[:insertion_index] + filtered_resonance_lines + main_lines[insertion_index:]

print(f"[OK] New line count: {len(updated_lines)}")

# Write updated file
with open("A35/Cl35/temp/1976ME12.ens", 'w', encoding='utf-8') as f:
    f.writelines(updated_lines)

print(f"[OK] Successfully inserted {len(filtered_resonance_lines)} lines into 1976ME12.ens")
print(f"[OK] Insertion completed at line {insertion_index + 1}")
print("")
print("Sample of inserted content:")
print(f"Line {insertion_index - 2}: {main_lines[insertion_index - 2].rstrip()}")
print(f"Line {insertion_index - 1}: {main_lines[insertion_index - 1].rstrip()}")
print(f"Line {insertion_index} (first inserted): {filtered_resonance_lines[0].rstrip()}")
print(f"Line {insertion_index + 1}: {filtered_resonance_lines[1].rstrip()}")
print(f"Line {insertion_index + 2}: {filtered_resonance_lines[2].rstrip()}")
