"""Analyze exact field positions in original (wrong) vs correct format."""

# Original (WRONG) - line 408 from backup
wrong = " 35CL  G 1702.1      31      2  E1+M2    -0.018  12                             "

# What it SHOULD be (CORRECT)
correct = " 35CL  G 1702.1       31      2  E1+M2    -0.018  12                            "

print("COLUMN-BY-COLUMN COMPARISON:")
print("=" * 80)
print("Position analysis from columns 20-50:")
print()
print("Col:  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34")
print("      DE  DE  SP  RI  RI  RI  RI  RI  RI  RI  DRI DRI SP  M   M")
print("=" * 80)

print("\nWRONG (original):")
for i in range(19, 35):
    col = i + 1
    ch = wrong[i] if i < len(wrong) else ' '
    print(f"Col {col:2d}: [{ch}]", end="  ")
print()

print("\nCORRECT (should be):")
for i in range(19, 35):
    col = i + 1
    ch = correct[i] if i < len(correct) else ' '
    print(f"Col {col:2d}: [{ch}]", end="  ")
print()

print("\n" + "=" * 80)
print("FIELD-BY-FIELD ANALYSIS:")
print("=" * 80)

print("\nDE field (cols 20-21):")
print(f"  WRONG:   '{wrong[19:21]}'")
print(f"  CORRECT: '{correct[19:21]}'")
print(f"  STATUS: Same - no change needed")

print("\nColumn 22 (MANDATORY SPACE):")
print(f"  WRONG:   '{wrong[21]}' <- ERROR! Has '3' (first digit of RI)")
print(f"  CORRECT: '{correct[21]}' <- Must be SPACE")

print("\nRI field (cols 23-29):")
print(f"  WRONG:   '{wrong[21:28]}' <- starts at col 22 (wrong)")
print(f"  CORRECT: '{correct[22:29]}' <- starts at col 23 (correct)")

print("\nDRI field (cols 30-31):")
print(f"  WRONG:   '{wrong[28:30]}' <- at cols 29-30 (wrong)")
print(f"  CORRECT: '{correct[29:31]}' <- at cols 30-31 (correct)")

print("\nColumn 32 (MANDATORY SPACE):")
print(f"  WRONG:   '{wrong[30]}' <- at col 31 (wrong)")
print(f"  CORRECT: '{correct[31]}' <- at col 32 (correct)")

print("\nM field (cols 33-41):")
print(f"  WRONG:   '{wrong[31:40]}' <- starts at col 32 (wrong)")
print(f"  CORRECT: '{correct[32:41]}' <- starts at col 33 (correct)")

print("\n" + "=" * 80)
print("SOLUTION:")
print("=" * 80)
print("Insert TWO spaces:")
print("  1. Space at col 22 (before RI)")
print("  2. Space at col 32 (before M) - this was also shifted left!")
print()
print("OR simpler: Insert ONE space at col 22, shift cols 22-31 right by 1")
print("This automatically restores both mandatory spaces!")
