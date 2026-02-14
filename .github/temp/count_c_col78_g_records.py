#!/usr/bin/env python3
"""
Count 'C' characters in column 78 of G-records only (not comment lines).
G-records have TYPE='G' at column 8 (0-based index 7).
Comment lines have 'c' at column 7 (0-based index 6).
"""

import sys

def count_c_in_col78_g_records(filename):
    """Count 'C' in column 78 of G-records only."""
    c_count = 0
    total_g_records = 0
    findings = []
    
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, 1):
            # Ensure line is at least 78 characters
            if len(line.rstrip('\r\n')) < 78:
                continue
            
            # Check if this is a comment line (column 7 = 'c')
            if line[6] == 'c':
                # Skip comment lines
                continue
            
            # Check if this is a G-record (column 8 = 'G')
            if line[7] == 'G':
                total_g_records += 1
                col78_char = line[77]  # 0-based index for column 78
                
                if col78_char == 'C':
                    c_count += 1
                    findings.append({
                        'line': line_num,
                        'line_content': line.rstrip('\r\n')
                    })
    
    return c_count, total_g_records, findings

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python check_col78_g_records.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    c_count, total_g_records, findings = count_c_in_col78_g_records(filename)
    
    print(f"\nG-Record Analysis (Column 78 only, excluding comment lines):")
    print(f"Total G-records: {total_g_records}")
    print(f"G-records with 'C' in column 78: {c_count}\n")
    
    if findings:
        print(f"Details of {c_count} G-record(s) with 'C' in column 78:")
        for i, item in enumerate(findings[:20], 1):  # Show first 20
            print(f"\n{i}. Line {item['line']}:")
            print(f"   {item['line_content']}")
        
        if len(findings) > 20:
            print(f"\n... and {len(findings) - 20} more")
    else:
        print("No G-records with 'C' in column 78 found.")
