#!/usr/bin/env python3
"""Scan ENSDF file for cL comment blocks with incorrect E/J/T/S ordering."""

import re

file_path = "A35/Cl35/new/Cl35_34s_p_g.ens"
order_map = {"E": 0, "J": 1, "T": 2, "S": 3}
expected_order = [0, 1, 2, 3]  # E, J, T, S

with open(file_path, 'r') as f:
    lines = f.readlines()

current_block = []
current_block_start = 0
current_types = []

for i, line in enumerate(lines, 1):
    # Check if this is an L-record (new block)
    if re.match(r'\s*35CL\s+L\s+', line):
        # Validate previous block if it exists
        if current_types:
            current_indices = [order_map.get(t, -1) for t in current_types if t in order_map]
            if current_indices != sorted(current_indices):
                print(f"WRONG ORDER at lines {current_block_start}-{i-1}:")
                print(f"  Order: {' -> '.join(current_types)}")
                print(f"  Lines: {current_block}")
                print()
        
        # Start new block
        current_block = [i]
        current_block_start = i
        current_types = []
    
    # Check for cL identifier lines
    match = re.match(r'\s*35CL\s+cL\s+([EJTS])\$', line)
    if match:
        identifier = match.group(1)
        current_block.append(i)
        current_types.append(identifier)

# Don't forget the last block
if current_types:
    current_indices = [order_map.get(t, -1) for t in current_types if t in order_map]
    if current_indices != sorted(current_indices):
        print(f"WRONG ORDER at lines {current_block_start}-{len(lines)}:")
        print(f"  Order: {' -> '.join(current_types)}")
        print(f"  Lines: {current_block}")
