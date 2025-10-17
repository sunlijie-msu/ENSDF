#!/usr/bin/env python3
"""
Analyze 2001VO24 CSV matrix to understand correct interpretation
"""

# Parse CSV
import csv

matrix = {}
header_exi = []
all_exf = set()

with open('A35/Cl35/raw/2001VO24.csv', 'r') as f:
    lines = f.readlines()
    
# Parse header row (Exi and Ep values)
header_line = lines[2].strip().split(',')
print("Header line:", header_line)
print()

# Extract Ep values (probe energies)
ep_line = lines[0].strip().split(',')
print("Ep values:", ep_line)
print()

# Extract Exi values (excitation energies of initial states)
exi_line = lines[2].strip().split(',')
print("Exi values (initial states):", exi_line)
print()

print("=" * 90)
print("CORRECT 2001VO24 INTERPRETATION:")
print("=" * 90)

# For L 7547 (Exi = 7547, which is in column index for Ep=1212)
# Find which column has Exi=7547
exi_data = [line.strip().split(',') for line in lines if line.startswith('Exi') or line.strip().startswith(',Exi')]
print("\nExi header row:", exi_data)

# Let me parse this differently
print("\nManual CSV parsing:")
for i, line in enumerate(lines[:5]):
    print(f"Line {i}: {repr(line.strip())}")

