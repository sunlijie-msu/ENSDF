"""
Integrate validated resonance data into main 1976ME12.ens file.
This script:
1. Reads lines 1-189 from original 1976ME12.ens (bound levels)
2. Keeps line 190 (resonance section comment)
3. Replaces lines 191-773 with validated 1976ME12_UPDATED_RESONANCES.txt (696 lines)
"""

import os

# File paths
original_file = os.path.join('A35', 'Cl35', 'temp', '1976ME12.ens')
updated_resonances = os.path.join('A35', 'Cl35', 'temp', '1976ME12_UPDATED_RESONANCES.txt')
output_file = os.path.join('A35', 'Cl35', 'temp', '1976ME12_COMPLETE.ens')
backup_file = os.path.join('A35', 'Cl35', 'temp', '1976ME12_BACKUP.ens')

# Read original file
print(f"Reading original file: {original_file}")
with open(original_file, 'r') as f:
    original_lines = f.readlines()

print(f"Original file has {len(original_lines)} lines")

# Read updated resonance data
print(f"Reading updated resonances: {updated_resonances}")
with open(updated_resonances, 'r') as f:
    resonance_lines = f.readlines()

print(f"Updated resonances file has {len(resonance_lines)} lines")

# Create backup of original
print(f"Creating backup: {backup_file}")
with open(backup_file, 'w') as f:
    f.writelines(original_lines)

# Integrate data
print("\nIntegrating data:")
print("- Lines 1-189: Bound levels from original file")
print("- Line 190: Resonance section comment from original file")
print("- Lines 191-886: Updated resonance data (696 lines)")

# Build complete file
complete_lines = []

# Add bound levels (lines 1-189, indices 0-188)
complete_lines.extend(original_lines[0:189])
print(f"Added {len(complete_lines)} bound level lines (1-189)")

# Add resonance section comment (line 190, index 189)
complete_lines.append(original_lines[189])
print(f"Added resonance comment: {original_lines[189].strip()}")

# Add updated resonance data (696 lines)
complete_lines.extend(resonance_lines)
print(f"Added {len(resonance_lines)} updated resonance lines")

# Write complete file
print(f"\nWriting complete file: {output_file}")
with open(output_file, 'w') as f:
    f.writelines(complete_lines)

print(f"\nComplete file has {len(complete_lines)} lines")
print(f"Expected: 189 (bound) + 1 (comment) + 696 (resonances) = 886 lines")

# Verify line counts
if len(complete_lines) == 886:
    print("[SUCCESS] Line count matches expected value!")
else:
    print(f"[WARNING] Line count mismatch: got {len(complete_lines)}, expected 886")

print("\nIntegration complete!")
print(f"- Backup saved to: {backup_file}")
print(f"- Complete file saved to: {output_file}")
print("\nNext steps:")
print("1. Validate with: python .github/column_calibrate.py A35/Cl35/temp/1976ME12_COMPLETE.ens")
print("2. Validate with: python .github/check_gamma_ordering.py A35/Cl35/temp/1976ME12_COMPLETE.ens")
print("3. Validate with: python .github/ensdf_1line_ruler.py --file A35/Cl35/temp/1976ME12_COMPLETE.ens --show-only-wrong")
