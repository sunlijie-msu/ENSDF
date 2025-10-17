#!/usr/bin/env python3
"""Add Ep values to S field (columns 65-74) of L-records only"""

# Mapping: Exi -> Ep (proton resonance energy)
ep_map = {
    7179: 832,
    7547: 1212,
    7838: 1510,
    8207: 1891,
    8216: 1900,
    8381: 2070,
    8484: 2176,
    8893: 2597,
    8907: 2611,
    9081: 2791,
}

# Read current ENSDF file
with open('A35/Cl35/raw/2001VO24.ens', 'r') as f:
    lines = f.readlines()

output_lines = []

for line in lines:
    # Check if it's an L-record
    if len(line) > 8 and line[0:6] == ' 35CL ' and line[7] == 'L':
        # Extract energy from L-record (columns 10-19)
        e_field = line[9:19].strip()
        try:
            exi = float(e_field)
        except:
            output_lines.append(line)
            continue
        
        # Check if this Exi has an Ep value
        if exi in ep_map:
            ep = ep_map[exi]
            # Modify the L-record to add Ep in S field (columns 65-74)
            # Ensure line is at least 64 characters
            modified_line = line.rstrip('\n')
            while len(modified_line) < 64:
                modified_line += ' '
            
            # Format Ep as a string (left-justified in 10-character field)
            ep_str = f'{ep:<10}'  # Left-justified in 10 chars
            
            # Insert Ep at columns 65-74 (0-indexed: 64-73)
            if len(modified_line) >= 64:
                modified_line = modified_line[:64] + ep_str + modified_line[74:]
            else:
                modified_line = modified_line + ep_str + modified_line[74:] if len(modified_line) >= 74 else modified_line + ep_str
            
            # Ensure exactly 80 characters
            modified_line = (modified_line + ' ' * 80)[:80]
            output_lines.append(modified_line + '\n')
        else:
            output_lines.append(line)
    else:
        # Not an L-record, keep as-is
        output_lines.append(line)

# Write modified file
with open('A35/Cl35/raw/2001VO24.ens', 'w') as f:
    f.writelines(output_lines)

print('✅ File updated: Ep values added to S field (columns 65-74) of L-records')
print(f'   Total L-records with Ep: {len(ep_map)}')
print(f'   Total lines output: {len(output_lines)}')
