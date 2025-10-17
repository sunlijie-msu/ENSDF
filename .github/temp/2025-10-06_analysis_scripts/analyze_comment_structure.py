"""Analyze comment line structure."""

comment_line = " 35CL cG $A{-2}=-0.03 {I3}, A{-4}=-0.002 {I50} (1971Wi13)"
g_record = " 35CL  G 1702.1      31      2  E1+M2    -0.018  12"

print("Comment line (cG) analysis:")
print("=" * 80)
for i in range(10):
    col = i + 1
    ch = comment_line[i] if i < len(comment_line) else ' '
    print(f"Col {col:2d} (idx {i}): [{ch}]")

print("\n" + "=" * 80)
print("G-record (data) analysis:")
print("=" * 80)
for i in range(10):
    col = i + 1
    ch = g_record[i] if i < len(g_record) else ' '
    print(f"Col {col:2d} (idx {i}): [{ch}]")

print("\n" + "=" * 80)
print("CRITICAL DIFFERENCE:")
print(f"  cG comment line col 6 (idx 5): '{comment_line[5]}'")
print(f"  G  data record col 6 (idx 5): '{g_record[5]}'")
print(f"  cG comment line col 7 (idx 6): '{comment_line[6]}'")
print(f"  G  data record col 7 (idx 6): '{g_record[6]}'")
