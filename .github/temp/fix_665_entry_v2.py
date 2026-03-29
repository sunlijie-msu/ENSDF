"""
CORRECTED fix for entry 150 in flag_expansion_replacements.json.
G 665.57: RI$ must be inserted AFTER E$ block and BEFORE M$ block.

Uses readlines() (not splitlines) to avoid line-indexing discrepancy.
"""
import json
import os

BASE = 'd:\\X\\ND\\ENSDF'
ENS_FILE = os.path.join(BASE, 'A34', 'Cl34', 'new', 'Cl34_adopted.ens')
JSON_FILE = os.path.join(BASE, '.github', 'temp', 'flag_expansion_replacements.json')

with open(ENS_FILE, 'r') as f:
    file_lines = f.readlines()
    content = ''.join(file_lines)

# Verified: G 665.57 is at 0-indexed 172 (1-indexed 173)
# FLAG=AB at 173, B cont at 174, E$ at 175, 2cG at 176, first M$ at 177
base = 172
l_g_data  = file_lines[base + 0]  # G 665.57 data
l_flag_ab = file_lines[base + 1]  # FLAG=AB
l_b_cont  = file_lines[base + 2]  # B cont BM1W
l_e_line  = file_lines[base + 3]  # cG E$ weighted avg
l_2e_line = file_lines[base + 4]  # 2cG E$ cont
l_m_line  = file_lines[base + 5]  # cG M$ from

print("Lines for G 665.57 block:")
print(f"  [172] G data:    {repr(l_g_data.rstrip())}")
print(f"  [173] FLAG=AB:   {repr(l_flag_ab.rstrip())}")
print(f"  [174] B cont:    {repr(l_b_cont.rstrip())}")
print(f"  [175] cG E$:     {repr(l_e_line.rstrip())}")
print(f"  [176] 2cG E$:    {repr(l_2e_line.rstrip())}")
print(f"  [177] cG M$:     {repr(l_m_line.rstrip())}")

# Verify these are what we expect
assert '665.57' in l_g_data and l_g_data[7] == 'G', f"Unexpected l_g_data: {l_g_data!r}"
assert 'FLAG=AB' in l_flag_ab, f"Unexpected l_flag_ab: {l_flag_ab!r}"
assert 'BM1W' in l_b_cont, f"Unexpected l_b_cont: {l_b_cont!r}"
assert 'cG E$' in l_e_line and 'weighted' in l_e_line, f"Unexpected l_e_line: {l_e_line!r}"
assert '2cG' in l_2e_line and '665.57' in l_2e_line, f"Unexpected l_2e_line: {l_2e_line!r}"
assert 'cG M$' in l_m_line, f"Unexpected l_m_line: {l_m_line!r}"

# Build RI$ line padded to 80 chars
ri_text = ' 34CL cG RI$From {+32}S({+3}He,p|g)'
ri_padded = ri_text.ljust(80) + '\n'
print(f"\nRI line (len={len(ri_padded.rstrip())}): {repr(ri_padded.rstrip())}")
assert len(ri_padded.rstrip()) == 35, f"Expected 35 chars, got {len(ri_padded.rstrip())}"

# Build correct old/new
# OLD: G_data + FLAG=AB + B_cont + E$ + 2E$ + first_M$
# NEW: G_data + B_cont + E$ + 2E$ + RI$ + first_M$
new_old = l_g_data + l_flag_ab + l_b_cont + l_e_line + l_2e_line + l_m_line
new_new = l_g_data + l_b_cont + l_e_line + l_2e_line + ri_padded + l_m_line

print(f"\nnew_old count in file (must be 1): {content.count(new_old)}")
print(f"new_new not yet in file: {new_new not in content}")
assert content.count(new_old) == 1, "new_old not unique in file!"
assert new_new not in content, "new_new already in file!"

# Load JSON and fix entry 150
with open(JSON_FILE, 'r') as f:
    ops = json.load(f)

print(f"\nTotal ops: {len(ops)}")
print(f"Current entry 150 desc: {ops[150].get('desc','')}")

# Overwrite entry 150 with the correct replacement
ops[150]['old'] = new_old
ops[150]['new'] = new_new
ops[150]['desc'] = 'FLAG=AB G-record expand at line 166 (RI$ after E$ block, before M$)'
ops[150]['case'] = 'AB_add_RI_special'

# Verify ALL old strings are still unique
all_olds = [op['old'] for op in ops]
seen = {}
dups = []
for i, o in enumerate(all_olds):
    if o in seen:
        dups.append((seen[o], i))
    seen[o] = i

print(f"\nDuplicate old strings: {len(dups)} (must be 0)")
for d in dups:
    print(f"  Indices {d[0]} and {d[1]}")

assert len(dups) == 0, "Duplicate old strings found!"

with open(JSON_FILE, 'w') as f:
    json.dump(ops, f, indent=2)
print("\nJSON updated successfully.")
print("Entry 150: G 665.57 RI$ will be placed after E$ block, before M$ block.")
