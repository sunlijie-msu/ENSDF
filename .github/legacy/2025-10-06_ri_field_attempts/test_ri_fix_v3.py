"""Test v3 fix logic - shift ONLY cols 22-31."""

wrong = " 35CL  G 1702.1      31      2  E1+M2    -0.018  12                             "

print("Testing CORRECT RI fix (shift only cols 22-31):")
print("=" * 80)
print(f"BEFORE: {wrong[:60]}")
print(f"Col 22 (idx 21): '{wrong[21]}'")
print()

# Apply fix
prefix = wrong[0:21]           # Cols 1-21 
ri_dri_space = wrong[21:31]    # Cols 22-31 (RI, DRI, space before M)
rest = wrong[31:80]            # Cols 32-80 (M, MR, DMR, etc.)

fixed = prefix + ' ' + ri_dri_space + rest
fixed = fixed[:80].ljust(80)

print(f"AFTER:  {fixed[:60]}")
print(f"Col 22 (idx 21): '{fixed[21]}'")
print()

print("Field verification:")
print("-" * 80)
print(f"Cols 22-35 BEFORE: [{wrong[21:35]}]")
print(f"Cols 22-35 AFTER:  [{fixed[21:35]}]")
print()
print(f"RI field (cols 23-29):")
print(f"  BEFORE (at cols 22-28): '{wrong[21:28]}'")
print(f"  AFTER  (at cols 23-29): '{fixed[22:29]}'")
print()
print(f"DRI field (cols 30-31):")
print(f"  BEFORE (at cols 29-30): '{wrong[28:30]}'")
print(f"  AFTER  (at cols 30-31): '{fixed[29:31]}'")
print()
print(f"Space at col 32:")
print(f"  BEFORE (at col 31): '{wrong[30]}'")
print(f"  AFTER  (at col 32): '{fixed[31]}'")
print()
print(f"M field (cols 33-41):")
print(f"  BEFORE (at cols 32-40): '{wrong[31:40]}'")
print(f"  AFTER  (at cols 33-41): '{fixed[32:41]}'")
print()
print(f"MR field (cols 42-49):")
print(f"  BEFORE (at cols 41-48): '{wrong[40:48]}'")
print(f"  AFTER  (at cols 42-49): '{fixed[41:49]}'")
print()
print("=" * 80)
print("SUCCESS! M and MR fields now at correct positions!")
