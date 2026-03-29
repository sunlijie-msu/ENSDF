"""
Fix entry 150 in flag_expansion_replacements.json for G 665.57.
The RI$ comment must be inserted AFTER the existing E$ block
and BEFORE the M$ block, not at the FLAG=AB position.
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENS_FILE = os.path.join(BASE, 'A34', 'Cl34', 'new', 'Cl34_adopted.ens')
JSON_FILE = os.path.join(BASE, '.github', 'temp', 'flag_expansion_replacements.json')

with open(ENS_FILE, 'r') as f:
    content = f.read()
    file_lines = content.splitlines(keepends=True)

# File lines (1-indexed): 173-178
# Index (0-indexed):        172-177
l173 = file_lines[172]  # G 665.57 data
l174 = file_lines[173]  # FLAG=AB
l175 = file_lines[174]  # B cont (BM1W)
l176 = file_lines[175]  # cG E$ weighted avg
l177 = file_lines[176]  # 2cG E$ cont
l178 = file_lines[177]  # cG M$ from

print("Lines identified:")
print(f"  l173: {repr(l173.rstrip())}")
print(f"  l174: {repr(l174.rstrip())}")
print(f"  l175: {repr(l175.rstrip())}")
print(f"  l176: {repr(l176.rstrip())}")
print(f"  l177: {repr(l177.rstrip())}")
print(f"  l178: {repr(l178.rstrip())}")

# Build RI$ line padded to 80 chars
ri_text = ' 34CL cG RI$From {+32}S({+3}He,p|g)'
ri_padded = ri_text.ljust(80) + '\n'
print(f"\nRI line length (without newline): {len(ri_padded.rstrip())}")
print(f"RI line: {repr(ri_padded.rstrip())}")

# Build correct old/new
# OLD: G data + FLAG=AB + B_cont + E$ + 2E$ + first M$
# NEW: G data + B_cont + E$ + 2E$ + RI$ + first M$
new_old = l173 + l174 + l175 + l176 + l177 + l178
new_new = l173 + l175 + l176 + l177 + ri_padded + l178

print(f"\nnew_old in content: {new_old in content}")
print(f"new_new not (yet) in content: {new_new not in content}")

# Load and update JSON
with open(JSON_FILE, 'r') as f:
    ops = json.load(f)

# Verify current entry 150
assert '665.57' in ops[150]['old'], "Entry 150 should contain G 665.57"
print(f"\nCurrent entry 150 old: {repr(ops[150]['old'][:80])}")
print(f"Current entry 150 old in content: {ops[150]['old'] in content}")

# Check uniqueness of new_old
count = content.count(new_old)
print(f"\nnew_old count in file (should be 1): {count}")

# Apply fix
ops[150]['old'] = new_old
ops[150]['new'] = new_new
ops[150]['desc'] = 'FLAG=AB G-record expand at line 166 (FIXED: RI$ after E$ block)'

with open(JSON_FILE, 'w') as f:
    json.dump(ops, f, indent=2)

print("\nJSON updated successfully.")
print("Entry 150 now spans FLAG=AB through first M$ to place RI$ after E$ block.")
