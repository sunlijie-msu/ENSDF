"""
Apply all 188 flag expansions to Cl34_adopted.ens.
This script reads the replacement JSON and applies changes directly.

This approach is used because multi_replace_string_in_file with 188 entries
would create an unmanageable payload. Direct Python file I/O is used with
explicit before/after verification.
"""
import json
import os
import sys

BASE = 'd:\\X\\ND\\ENSDF'
ENS_FILE = os.path.join(BASE, 'A34', 'Cl34', 'new', 'Cl34_adopted.ens')
JSON_FILE = os.path.join(BASE, '.github', 'temp', 'flag_expansion_replacements.json')

with open(JSON_FILE, 'r') as f:
    ops = json.load(f)

with open(ENS_FILE, 'r') as f:
    content = f.read()

print(f"File: {ENS_FILE}")
print(f"Total replacements: {len(ops)}")
print(f"File size before: {len(content)} chars, {content.count(chr(10))} lines")

# Verify all old strings present
missing = [i for i, op in enumerate(ops) if op['old'] not in content]
if missing:
    print(f"ERROR: {len(missing)} old strings not found in file!")
    for i in missing[:5]:
        print(f"  Op {i}: {ops[i].get('desc','')[:60]}")
    sys.exit(1)

print("All old strings verified present in file.")

# Apply all replacements
applied = 0
for i, op in enumerate(ops):
    old = op['old']
    new = op['new']
    count_before = content.count(old)
    if count_before != 1:
        print(f"WARNING: Op {i} old string found {count_before} times (expected 1)! desc: {op.get('desc','')[:50]}")
        if count_before == 0:
            print(f"  Old string: {repr(old[:100])}")
            continue
    content = content.replace(old, new, 1)
    applied += 1
    if applied % 20 == 0:
        print(f"  Applied {applied}/{len(ops)}...")

print(f"\nAll {applied} replacements applied.")
print(f"File size after: {len(content)} chars, {content.count(chr(10))} lines")

# Count remaining FLAG= lines
remaining_flags = []
for line in content.splitlines():
    if 'FLAG=' in line:
        remaining_flags.append(line.strip())
print(f"\nRemaining FLAG= lines (from non-expanded flags): {len(remaining_flags)}")
for fl in remaining_flags[:10]:
    print(f"  {fl}")

# Write output
with open(ENS_FILE, 'w') as f:
    f.write(content)
print(f"\nFile written successfully.")
