"""Analyze exact column positions for line 408 RI field."""

line = ' 35CL  G 1702.1      31      2  E1+M2    -0.018  12'

print("Column-by-column analysis of line 408:")
print("=" * 60)
print(f"Full line: [{line}]")
print(f"Line length: {len(line)}")
print()

print("Columns 18-32 (DE, SPACE, RI, DRI region):")
print("-" * 60)
for i in range(17, 32):
    col = i + 1
    if i < len(line):
        ch = line[i]
        if col == 20:
            print(f"Col {col:2d} (idx {i:2d}): [{ch}]  <- DE field starts")
        elif col == 22:
            print(f"Col {col:2d} (idx {i:2d}): [{ch}]  <- SHOULD BE SPACE, but has '{ch}'")
        elif col == 23:
            print(f"Col {col:2d} (idx {i:2d}): [{ch}]  <- RI should start HERE")
        elif col == 30:
            print(f"Col {col:2d} (idx {i:2d}): [{ch}]  <- DRI field starts")
        else:
            print(f"Col {col:2d} (idx {i:2d}): [{ch}]")
    else:
        print(f"Col {col:2d} (idx {i:2d}): [BEYOND LINE]")

print()
print("=" * 60)
print("ANALYSIS RESULT:")
print("=" * 60)
print(f"Column 22 contains: '{line[21]}' (should be SPACE)")
print(f"RI value '31' starts at: Column 22 (INCORRECT)")
print(f"RI value should start at: Column 23 (per ENSDF specs)")
print()
print("ENSDF G-record specification:")
print("  Columns 20-21: DE (energy uncertainty)")
print("  Column 22: MANDATORY SPACE separator")
print("  Columns 23-29: RI (relative intensity) LEFT-JUSTIFIED at col 23")
print("  Columns 30-31: DRI (RI uncertainty)")
print()
print("ERROR: RI field shifted left by 1 column due to missing space at col 22")
