#!/usr/bin/env python3
"""Add Ep values and BR comments to 2001VO24.ens"""

# Mapping: Exi -> Ep
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
current_exi = None
line_idx = 0

while line_idx < len(lines):
    line = lines[line_idx]
    
    # Check if it's an L-record
    if ' L ' in line and len(line) > 8 and line[7] == 'L':
        # Extract energy from L-record
        e_field = line[9:19].strip()
        try:
            exi = float(e_field)
            current_exi = exi
        except:
            exi = None
        
        # Output the L-record as-is
        output_lines.append(line)
        
        # Add Ep value if this Exi has one
        if exi in ep_map:
            ep = ep_map[exi]
            # Insert Ep into columns 56-63 on this L-record line
            # First, remove the newline
            modified_line = line.rstrip('\n')
            # Pad to at least 55 characters
            while len(modified_line) < 55:
                modified_line += ' '
            # Add Ep value at columns 56-63 (1-indexed: col 56-63 is index 55-62)
            # Format Ep right-justified in 8 characters
            ep_str = f'{ep:8d}'
            if len(modified_line) >= 55:
                modified_line = modified_line[:55] + ep_str + modified_line[63:]
            else:
                modified_line = modified_line + ep_str + ' ' * max(0, 80 - len(modified_line) - len(ep_str))
            # Ensure exactly 80 characters
            modified_line = (modified_line + ' ' * 80)[:80]
            output_lines[-1] = modified_line + '\n'
        
    elif ' G ' in line and len(line) > 8 and line[7] == 'G':
        # Output the G-record as-is
        output_lines.append(line)
        
        # Extract BR value from columns 23-29
        br_field = line[22:29].strip()
        if br_field and current_exi in ep_map:
            try:
                br = int(br_field)
                # Create cG comment record with RI value
                # Format: ' 35CL cG RI$value'
                cg_comment = f' 35CL cG RI${br}\n'
                # Pad to 80 characters
                cg_comment = (cg_comment.rstrip('\n') + ' ' * 80)[:80] + '\n'
                output_lines.append(cg_comment)
            except:
                pass
    else:
        output_lines.append(line)
    
    line_idx += 1

# Write modified file
with open('A35/Cl35/raw/2001VO24.ens', 'w') as f:
    f.writelines(output_lines)

print('✅ File updated with Ep values and BR comments')
print(f'   Total lines in output: {len(output_lines)}')
