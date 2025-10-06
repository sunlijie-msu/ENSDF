"""Test RI fix script on sample lines before applying to full file."""

# Sample G-records with RI at col 22 (wrong)
test_lines = [
    " 35CL  G 1219.4      100                                                        ",
    " 35CL  G 543.7       0.2     LT                                                 ",
    " 35CL  G 1763.1       100       M1+E2    0.42    17                             ",
    " 35CL  G 1702.1      31      2  E1+M2    -0.018  12                             ",
]

# Sample cG comment line that should NOT be modified
comment_line = " 35CL cG $A{-2}=-0.03 {I3}, A{-4}=-0.002 {I50} (1971Wi13)                       "

print("Testing RI fix logic on sample lines:")
print("=" * 80)

for i, line in enumerate(test_lines, 1):
    line_content = line.rstrip('\n')
    
    # Check if this is a G-record (NOT cG comment)
    # Column 7 (index 6) must NOT be 'c' (excludes cG, cL, cE, cB)
    if (len(line_content) >= 9 and 
        line_content[7] == 'G' and 
        line_content[8] == ' ' and 
        line_content[6] != 'c'):
        
        # Pad to 80 chars
        line_content = line_content.ljust(80)
        
        # Check column 22
        col_22 = line_content[21]
        print(f"\nTest {i}:")
        print(f"  Line: {line_content[:50]}")
        print(f"  Col 22: '{col_22}' (index 21)")
        
        if col_22 != ' ':
            # Extract RI from wrong position (cols 22-28)
            ri_wrong = line_content[21:28].rstrip()
            dri_wrong = line_content[28:30]
            
            # Build fixed line
            fixed = (
                line_content[0:21] +  # Everything up to col 21
                ' ' +                  # Col 22 - SPACE
                ri_wrong.ljust(7) +   # Cols 23-29 - RI LEFT-JUSTIFIED
                dri_wrong +           # Cols 30-31 - DRI
                line_content[30:]     # Everything after col 31
            )
            fixed = fixed[:80].ljust(80)
            
            print(f"  BEFORE col 22-32: [{line_content[21:32]}]")
            print(f"  AFTER  col 22-32: [{fixed[21:32]}]")
            print(f"  RI='{ri_wrong}' DRI='{dri_wrong}'")
            print(f"  Fixed: {fixed[:50]}")
        else:
            print(f"  [OK] Column 22 already has space")

# Test comment line exclusion
print(f"\n{'=' * 80}")
print("Testing comment line exclusion:")
print(f"  Comment: {comment_line[:50]}")
print(f"  Col 7 (idx 6): '{comment_line[6]}' (should be 'c' for comment)")
print(f"  Col 8 (idx 7): '{comment_line[7]}' (should be 'G')")

if comment_line[6] == 'c':
    print("  [OK] This is a cG comment line - EXCLUDED from fixes")
else:
    print("  [ERROR] Not detected as comment line!")

print("\n" + "=" * 80)
print("Test completed - logic appears correct")
