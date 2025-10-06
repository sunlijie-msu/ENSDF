"""
Format CSV data from 1976SP08.ens into proper ENSDF L-record format.
This script converts resonance data to ENSDF 80-column format.
"""

def format_l_record(Ex, Ep, DEp):
    """Format L-record with exact column positions (80 characters)"""
    # Convert DEp decimal to integer (0.5 -> 5, 0.4 -> 4, 0.3 -> 3)
    DEp_int = int(round(DEp * 10))
    
    # Build L-record: cols 1-5 NUCID, col 8 'L', cols 10-19 Ex, cols 65-74 Ep, cols 75-76 DEp_int
    Ex_str = str(Ex)  # Left-justified
    Ep_str = str(Ep)  # Left-justified
    DEp_str = str(DEp_int) + ' '  # Left-justified with space padding
    
    # Build line: ' 35CL  L ' (9 chars) + Ex value
    line = ' 35CL  L ' + Ex_str
    # Pad to column 64 (before S-field starts at 65)
    line += ' ' * (64 - len(line))
    # Add S-field (Ep) starting at column 65
    line += Ep_str
    # Pad to column 74 (before DS-field starts at 75)
    line += ' ' * (74 - len(line))
    # Add DS-field (DEp_int) at columns 75-76
    line += DEp_str
    # Pad to exactly 80 characters
    line += ' ' * (80 - len(line))
    
    return line

def format_cl_comment(wg, Dwg):
    """Format cL comment line (NOT padded to 80)"""
    # Calculate uncertainty notation: n = round(Dwg × 10)
    n = int(round(Dwg * 10))
    
    # Format: ' 35CL cL $$|w|g=WG eV {In} (1976Sp08)'
    wg_str = str(wg)
    comment = ' 35CL cL $$|w|g=' + wg_str + ' eV {I' + str(n) + '} (1976Sp08)'
    
    return comment

# Process CSV data and generate formatted ENSDF lines
if __name__ == '__main__':
    import sys
    
    # Read CSV data from 1976SP08.ens
    csv_file = r'd:\X\ND\ENSDF\A35\Cl35\temp\1976SP08.ens'
    
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    
    # Extract CSV data starting from line 10 (skip header at line 9)
    csv_data = []
    for line in lines[9:]:  # Line 10 onwards
        parts = line.strip().split('\t')
        if len(parts) == 5:
            try:
                Ex = float(parts[0])
                Ep = float(parts[1])
                DEp = float(parts[2])
                wg = float(parts[3])
                Dwg = float(parts[4])
                csv_data.append((Ex, Ep, DEp, wg, Dwg))
            except ValueError:
                pass
    
    print('PROCESSING CSV DATA:')
    print('Total rows:', len(csv_data))
    print('First 2 rows already formatted as examples (Ex=8270.1, 8278.4)')
    print('Processing remaining', len(csv_data) - 2, 'rows...')
    print('')
    
    # Skip first 2 rows (already formatted as examples)
    # Process rows 3-87 (Ex=8283.2 to 9195.6)
    formatted_lines = []
    
    for i, (Ex, Ep, DEp, wg, Dwg) in enumerate(csv_data[2:], start=3):
        l_record = format_l_record(Ex, Ep, DEp)
        cl_comment = format_cl_comment(wg, Dwg)
        
        formatted_lines.append(l_record)
        formatted_lines.append(cl_comment)
        
        # Progress report every 10 rows
        if i % 10 == 0:
            print('  Processed row', i, ':', 'Ex=', Ex)
    
    print('')
    print('FORMATTING COMPLETE:')
    print('  Generated', len(formatted_lines), 'lines (', len(formatted_lines)//2, 'L-records +', len(formatted_lines)//2, 'cL comments)')
    print('')
    
    # Save formatted lines to temporary file
    output_file = r'd:\X\ND\ENSDF\.github\formatted_levels_1976sp08.txt'
    with open(output_file, 'w') as f:
        for line in formatted_lines:
            f.write(line + '\n')
    
    print('Formatted lines saved to:', output_file)
    print('')
    
    # Show first 3 and last 3 formatted pairs
    print('First 3 formatted pairs:')
    for i in range(0, 6, 2):
        print('  L-record:', repr(formatted_lines[i]))
        print('  cL comment:', repr(formatted_lines[i+1]))
        print('')
    
    print('Last 3 formatted pairs:')
    for i in range(len(formatted_lines)-6, len(formatted_lines), 2):
        print('  L-record:', repr(formatted_lines[i]))
        print('  cL comment:', repr(formatted_lines[i+1]))
        print('')
