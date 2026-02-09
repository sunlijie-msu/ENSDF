#!/usr/bin/env python3
"""Systematically extract E$ data for all 13 levels and run averaging"""

import subprocess
import re

file = r'A35/Cl35/new/Cl35_adopted.ens'

# The 13 line numbers I previously updated (from conversation summary)
level_lines = [149, 259, 443, 728, 744, 802, 1377, 1845, 1988, 2306, 2654, 2818, 2863]

with open(file, 'r', encoding='latin-1') as f:
    lines = f.readlines()

print("="*80)
print("SYSTEMATIC AVERAGING VERIFICATION FOR ALL 13 LEVELS")
print("="*80)

for line_num in level_lines:
    # Read the L-record
    l_record = lines[line_num - 1]
    energy = l_record[9:19].strip()
    unc_field = l_record[19:21].strip()
    
    print(f"\n{'='*80}")
    print(f"Level at line {line_num}: Current L-record = {energy}({unc_field})")
    print(f"{'='*80}")
    
    # Find the E$ weighted average comment following this L-record
    i = line_num  # Start from the line AFTER the L-record (line_num is 1-based, array is 0-based)
    e_comment_lines = []
    while i < len(lines) and i < line_num + 30:  # Search up to 30 lines ahead
        line = lines[i]
        if 'E$weighted average' in line and 'cL' in line[5:8]:
            # Found it! Collect all continuation lines
            e_comment_lines.append(line[:80])
            j = i + 1
            while j < len(lines) and 'cL' in lines[j][5:8]:
                e_comment_lines.append(lines[j][:80])
                j += 1
            break
        elif line[7:9] == ' L' and line[0:5].strip() and 'X' not in line[5:7]:
            # Hit next TRUE L-record (not XREF or continuation) without finding E$ comment
            break
        i += 1
    
    # Print the E$ comment
    print("\nE$ Comment:")
    for comment in e_comment_lines:
        print(comment.rstrip())
    
    # Parse values from E$ comment
    # First, clean up the text: remove NUCID markers and join lines properly
    full_text = ''
    for line in e_comment_lines:
        # Extract just the comment text (columns 10-80)
        comment_text = line[9:]
        full_text += comment_text + ' '
    
    # Extract all patterns like "VALUE {In}"
    pattern = r'(\d+(?:\.\d+)?)\s+\{I(\d+)\}'
    matches = re.findall(pattern, full_text)
    
    if not matches:
        print("WARNING: Could not parse E$ comment!")
        continue
    
    # Convert to averaging input format
    data_points = []
    for value_str, unc_digits in matches:
        value = float(value_str)
        # Determine uncertainty based on decimal places
        if '.' in value_str:
            decimals = len(value_str.split('.')[1])
            unc = float(unc_digits) / (10 ** decimals)
        else:
            unc = float(unc_digits)
        data_points.append((value, unc))
    
    print(f"\nParsed {len(data_points)} data points for averaging:")
    for i, (v, u) in enumerate(data_points, 1):
        print(f"  {i}. {v} ± {u}")
    
    # Build command for Java_Average.py
    args = []
    for v, u in data_points:
        args.extend([str(v), str(u)])
    
    cmd = ['python', '.github/scripts/Java_Average.py'] + args
    
    print(f"\nRunning averaging...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Extract suggested result from output
    for line in result.stdout.split('\n'):
        if '*** Suggested Adopted Result:' in line:
            print(f"\n>>> {line.strip()}")
            break
    
    print("")  # Blank line between levels
