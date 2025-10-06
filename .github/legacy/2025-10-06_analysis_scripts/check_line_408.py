#!/usr/bin/env python3
"""Check exact formatting of line 408 in Cl35_34s_p_g.ens"""

with open(r'A35\Cl35\new\Cl35_34s_p_g.ens', 'r', encoding='utf-8') as f:
    lines = f.readlines()

line = lines[407].rstrip('\n')  # Line 408 (0-indexed 407)

print("Full line:")
print(repr(line))
print(f"\nLine length: {len(line)}")

print("\nColumns 33-55 (M, MR, DMR fields):")
for i in range(32, min(55, len(line))):
    col_num = i + 1
    char = line[i]
    field_info = ""
    if 33 <= col_num <= 41:
        field_info = " [M field]"
    elif 42 <= col_num <= 49:
        field_info = " [MR field]"
    elif 50 <= col_num <= 55:
        field_info = " [DMR field]"
    print(f"Col {col_num} (idx {i}): [{char}]{field_info}")

print("\nField extraction:")
print(f"M field (cols 33-41):  [{line[32:41]}]")
print(f"MR field (cols 42-49): [{line[41:49]}]")
print(f"DMR field (cols 50-55): [{line[49:55]}]")

print("\nAnalysis:")
m_field = line[32:41]
mr_field = line[41:49]
dmr_field = line[49:55]

print(f"M field: '{m_field.strip()}' (LEFT-JUSTIFIED: {m_field[0] != ' ' if m_field else 'EMPTY'})")
print(f"MR field: '{mr_field.strip()}' (LEFT-JUSTIFIED: {mr_field[0] != ' ' if mr_field.strip() else 'EMPTY'})")
print(f"DMR field: '{dmr_field.strip()}' (LEFT-JUSTIFIED: {dmr_field[0] != ' ' if dmr_field.strip() else 'EMPTY'})")

if dmr_field.strip() and dmr_field[0] != ' ':
    print("\n✓ DMR field IS LEFT-JUSTIFIED at column 50")
elif dmr_field.strip():
    print(f"\n✗ DMR field NOT LEFT-JUSTIFIED - starts at column {50 + len(dmr_field) - len(dmr_field.lstrip())}")
else:
    print("\n- DMR field is empty")
