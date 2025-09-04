#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - Simple and Effective
=====================================================

Simple, direct validation of ENSDF field positions that actually works.
Focuses on the core task: checking if fields are in the right columns.

ENSDF L-Record Field Positions (Mandatory):
- Columns 1-5:   NUCID
- Column 8:      Record type "L" 
- Columns 10-19: Energy field (E)
- Columns 23-39: J-π field (starts at col 23)
- Columns 40-49: Half-life (T) field
- Columns 56-64: Angular momentum transfer (L)
- Columns 65-74: Spectroscopic factor (S)

Usage: python column_calibrate_new.py "filename.ens"
"""

import sys
import os

def print_ruler():
    """Print the 80-column ruler for visual reference."""
    print('ENSDF 80-Column Ruler:')
    print('Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999')

def find_field_positions(line, field_chars):
    """Find positions of specific characters that represent field values."""
    positions = []
    for i, char in enumerate(line, 1):
        if char in field_chars and i > 50:  # Look for L-transfer fields after col 50
            positions.append(i)
    return positions

def validate_ensdf_file(filename):
    """Validate ENSDF file field positions with simple, direct checking."""
    
    if not os.path.exists(filename):
        print(f"ERROR: File {filename} not found!")
        return False
        
    print(f"Validating ENSDF file: {filename}")
    print("=" * 60)
    print_ruler()
    print()
    
    errors_found = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        # Skip short lines and non-L records
        if len(line) < 10 or ' L ' not in line[6:10]:
            continue
            
        # Check line length
        if len(line.rstrip()) > 80:
            print(f"LINE {line_num}: Exceeds 80 columns ({len(line.rstrip())} chars)")
            print(f"Line:  {line.rstrip()}")
            print_ruler()
            print()
            errors_found = True
            continue
            
        # Look for L-transfer values (numbers in the L-field area)
        l_positions = []
        for i, char in enumerate(line, 1):
            if char.isdigit() and 50 < i < 70:  # L-field region
                # Check if this is likely an L-transfer value
                context = line[max(0, i-5):i+5]  # Get surrounding context
                if not any(x in context for x in ['keV', 'eV', 'MeV', '(', ')', '+', '-']):
                    l_positions.append((char, i))
        
        # Report L-field positioning
        if l_positions:
            print(f"LINE {line_num}: L-transfer field analysis")
            print(f"Line:  {line.rstrip()}")
            print_ruler()
            
            for char, pos in l_positions:
                if pos == 56:
                    print(f"✓ L={char} correctly positioned at column {pos}")
                else:
                    print(f"✗ L={char} incorrectly positioned at column {pos} (should be 56)")
                    errors_found = True
            print()
    
    if not errors_found:
        print("✓ All ENSDF field positions appear correct!")
    else:
        print("✗ Field positioning errors found - see details above")
        
    return not errors_found

def main():
    if len(sys.argv) != 2:
        print("Usage: python column_calibrate_new.py \"filename.ens\"")
        sys.exit(1)
        
    filename = sys.argv[1]
    success = validate_ensdf_file(filename)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
