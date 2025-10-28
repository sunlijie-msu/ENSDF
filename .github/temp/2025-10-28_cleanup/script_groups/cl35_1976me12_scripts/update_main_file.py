# Update main file with complete resonance data

# Read original file (lines 1-190)
with open('1976ME12.ens', 'r') as f:
    orig_lines = f.readlines()

bound_section = orig_lines[:190]  # Lines 1-190 (bound levels)

# Read new complete resonances (preserve all trailing spaces!)
with open('1976ME12_COMPLETE_RESONANCES.txt', 'r') as f:
    resonance_lines = f.readlines()  # Do NOT use rstrip() - preserves 80-char lines

# Combine
final_content = bound_section + resonance_lines + ['\n']

# Write to main file
with open('1976ME12.ens', 'w') as f:
    f.writelines(final_content)

print(f'Updated 1976ME12.ens:')
print(f'  Lines 1-190: Bound levels (preserved)')
print(f'  Lines 191-{190 + len(resonance_lines)}: Complete resonances ({len(resonance_lines)} lines)')
print(f'  Total lines: {len(final_content)}')
