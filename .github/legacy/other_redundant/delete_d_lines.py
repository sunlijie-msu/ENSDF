#!/usr/bin/env python3
"""
Script to remove specific lines from S35_adopted.ens:
1. All lines matching pattern " 35S  d[LG] $[Letter][Numbers]" (dL and dG records only)
"""

import re
import os

def delete_d_lines(filepath):
    """Remove dL and dG records from S35 adopted file"""
    
    # Read the current file
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_count = len(lines)
    print(f"Original file has {original_count} lines")
    
    # Pattern for dL$/dG$ records: " 35S  d[LG] $[Letter][Numbers]"
    dl_dg_pattern = re.compile(r'^ 35S  d[LG] \$[A-Z][0-9]')
    
    # Track what we're removing
    removed_lines = []
    kept_lines = []
    
    for i, line in enumerate(lines, 1):
        should_remove = False
        
        # Check ONLY for dL$/dG$ pattern
        if dl_dg_pattern.match(line):
            should_remove = True
            removed_lines.append((i, "dL$/dG$ pattern", line.strip()))
        
        if not should_remove:
            kept_lines.append(line)
    
    # Show what we're removing
    print(f"\nRemoving {len(removed_lines)} lines:")
    for line_num, reason, content in removed_lines:
        print(f"  Line {line_num}: {reason} - {content[:60]}...")
    
    # Write the cleaned file
    new_count = len(kept_lines)
    print(f"\nNew file will have {new_count} lines (removed {original_count - new_count})")
    
    # Create backup first
    backup_path = filepath + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Backup created: {backup_path}")
    
    # Write cleaned file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(kept_lines)
    
    print(f"File cleaned successfully!")
    return original_count - new_count

if __name__ == "__main__":
    filepath = r"d:\X\ND\ENSDF\A35\S35\new\S35_adopted.ens"
    
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        exit(1)
    
    try:
        removed_count = delete_d_lines(filepath)
        print(f"\nSummary: Successfully removed {removed_count} lines from S35_adopted.ens")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
