"""
Sort L-records in 1972HU10_corrected.ens by energy (ascending order).

ENSDF requirement: ALL L-records MUST be in ascending energy order.
Currently the file has new L-records appended at the end - need to sort them properly.
"""

def extract_energy_from_l_record(line):
    """Extract energy value from L-record (columns 10-19)."""
    try:
        e_field = line[9:19].strip()
        return float(e_field)
    except (ValueError, IndexError):
        return 0.0

def main():
    input_file = r"A35\Cl35\temp\1972HU10_corrected.ens"
    output_file = r"A35\Cl35\temp\1972HU10_corrected_sorted.ens"
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Find header section (everything before first L-record)
    header_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        if len(line) >= 8 and line[7] == 'L' and line[0:5].strip():  # L-record with NUCID
            break
        header_lines.append(lines[i])
        i += 1
    
    # Collect all L-records with their G-records and cL comments
    level_blocks = []
    current_block = []
    
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Check if this is an L-record
        if len(line) >= 8 and line[7] == 'L':
            # Save previous block if exists
            if current_block:
                level_blocks.append(current_block)
            
            # Start new block with this L-record
            current_block = [lines[i]]
            energy = extract_energy_from_l_record(line)
        else:
            # Add to current block (G-records, cL comments, etc.)
            if current_block:
                current_block.append(lines[i])
        
        i += 1
    
    # Add last block
    if current_block:
        level_blocks.append(current_block)
    
    # Sort level blocks by energy
    def get_block_energy(block):
        """Get energy of first L-record in block."""
        for line in block:
            line_str = line.rstrip('\n')
            if len(line_str) >= 8 and line_str[7] == 'L':
                return extract_energy_from_l_record(line_str)
        return 0.0
    
    level_blocks.sort(key=get_block_energy)
    
    # Write sorted file
    with open(output_file, 'w') as f:
        # Write header
        f.writelines(header_lines)
        
        # Write sorted level blocks
        for block in level_blocks:
            f.writelines(block)
    
    print(f"[SUCCESS] Sorted {len(level_blocks)} level blocks")
    print(f"[SUCCESS] Output file: {output_file}")
    
    # Print first and last energies for verification
    first_energy = get_block_energy(level_blocks[0])
    last_energy = get_block_energy(level_blocks[-1])
    print(f"[INFO] Energy range: {first_energy:.1f} keV to {last_energy:.1f} keV")

if __name__ == "__main__":
    main()
