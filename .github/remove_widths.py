#!/usr/bin/env python3
"""
Script to remove resonance width values from S35_adopted.ens L-records.
Removes only the width values in T field (cols 40-49) and DT field (cols 50-55)
while preserving all other L-record content.
"""

import re
import os

def remove_resonance_widths(filepath):
    """Remove resonance width values from L-records"""
    
    # Read the current file
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    print(f"Original file has {original_count} lines")
    
    modified_lines = []
    changes_made = 0
    
    for i, line in enumerate(lines, 1):
        # Check if this is an L-record with EV width in the T field
        if (len(line) >= 55 and 
            line[:9] == " 35S   L " and 
            " EV " in line[39:56]):  # Check T and DT fields (cols 40-56)
            
            # Extract the parts: before width, width section, after width
            before_width = line[:39]  # Cols 1-39 (NUCID through J field)
            width_section = line[39:56]  # Cols 40-56 (T and DT fields)
            after_width = line[56:]   # Cols 57-80 (L, S, DS, C fields)
            
            # Clear the width fields but maintain spacing
            cleared_width = " " * 17  # 17 spaces for cols 40-56
            
            # Reconstruct the line
            new_line = before_width + cleared_width + after_width
            modified_lines.append(new_line)
            
            # Extract energy for logging
            energy_match = re.search(r'L (\d+\.\d+)', line[:25])
            energy = energy_match.group(1) if energy_match else "unknown"
            width_match = re.search(r'(\d+\.\d+\s+EV\s+\d+)', width_section)
            width = width_match.group(1) if width_match else "unknown"
            
            changes_made += 1
            print(f"  Line {i}: Removed width '{width}' from energy {energy}")
        else:
            modified_lines.append(line)
    
    print(f"\nModified {changes_made} L-records with resonance widths")
    
    if changes_made > 0:
        # Create backup first
        backup_path = filepath + '.width_backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Backup created: {backup_path}")
        
        # Write modified file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(modified_lines)
        
        print(f"Successfully removed resonance widths from {changes_made} L-records")
    else:
        print("No resonance width records found to modify")
    
    return changes_made

if __name__ == "__main__":
    filepath = r"d:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens"
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        exit(1)
    
    try:
        modified_count = remove_resonance_widths(filepath)
        print(f"\nSummary: Successfully processed {modified_count} resonance width records")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
