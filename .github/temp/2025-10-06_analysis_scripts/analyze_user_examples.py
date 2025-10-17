#!/usr/bin/env python3
"""Analyze the exact column positions of user's example lines."""

def analyze_line(line_text, line_desc):
    """Analyze a single line showing all relevant field positions."""
    
    print(f"\n{'='*80}")
    print(f"{line_desc}")
    print(f"{'='*80}")
    print(f"Line: {repr(line_text)}")
    print(f"Length: {len(line_text)} chars")
    print()
    
    # Pad to 80 characters
    padded = line_text.ljust(80, ' ')
    
    # Extract fields
    mr_field = padded[41:49]  # cols 42-49 (0-indexed: 41-49)
    dmr_field = padded[49:55]  # cols 50-55 (0-indexed: 49-55)
    c_field = padded[76] if len(line_text) > 76 else '?'  # col 77 (0-indexed: 76)
    q_field = padded[79] if len(line_text) > 79 else '?'  # col 80 (0-indexed: 79)
    
    print(f"MR field (cols 42-49):  [{mr_field}]")
    print(f"DMR field (cols 50-55): [{dmr_field}]")
    print(f"C field (col 77):      [{c_field}]")
    print(f"Q field (col 80):      [{q_field}]")
    print()
    
    # Character-by-character for relevant columns
    print("Character-by-character analysis (cols 40-60, 75-80):")
    print("Col 40-60:")
    for i in range(39, min(60, len(line_text))):
        print(f"  Col {i+1:2d} (idx {i:2d}): {repr(line_text[i])}")
    
    if len(line_text) >= 75:
        print("Col 75-80:")
        for i in range(74, min(80, len(line_text))):
            print(f"  Col {i+1:2d} (idx {i:2d}): {repr(line_text[i])}")
    
    # Check for errors
    errors = []
    
    # DMR field should be LEFT-JUSTIFIED at col 50 (index 49)
    if dmr_field.strip() and dmr_field[0] == ' ':
        errors.append(f"DMR field has leading space - should start at col 50, but starts at col {50 + len(dmr_field) - len(dmr_field.lstrip())}")
    
    # C field (col 77) should only contain A-Z, a-z, *, &, @ or space
    if len(line_text) >= 77:
        if c_field not in ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*&@':
            errors.append(f"Column 77 (C field) contains invalid character: {repr(c_field)} (should be A-Z, a-z, *, &, @ or space)")
    
    # Q field (col 80) should only contain space, ?, or S
    if len(line_text) >= 80:
        if q_field not in ' ?S':
            errors.append(f"Column 80 (Q field) contains invalid character: {repr(q_field)} (should be space, '?', or 'S')")
    
    if errors:
        print("\n❌ ERRORS FOUND:")
        for err in errors:
            print(f"  - {err}")
    else:
        print("\n✅ No formatting errors detected")


# Example 1
line1 = " 35CL  G 1702.1       31     2  E1+M2    -0.018   12"
analyze_line(line1, "Example 1: DMR field '12' positioning")

# Example 2
line2 = " 35CL  G 4545.1       2.0    1  E1(+M2)  +0.6     4                          P"
analyze_line(line2, "Example 2: DMR field '4' and comment flag 'P' positioning")
