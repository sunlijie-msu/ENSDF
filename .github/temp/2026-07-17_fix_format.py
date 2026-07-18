"""Fix formatting errors in ENSDF cG continuation lines:
1. `., |d=` → `, |d=...` (move period to end, remove comma after period)
2. `|d=>` → `|d>` (fix limit notation)
3. Ensure period at end of delta clause
"""
import re

with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    content = f.read()

lines = content.split('\n')
fixed = 0

for i in range(len(lines)):
    line = lines[i]
    if len(line) < 10: continue
    
    # Check if this is a continuation cG line with delta info
    # Patterns to fix:
    # 1. `{In}., |d=...` -> `{In}, |d=... .` (period at end)
    # 2. `|d=>` -> `|d>`
    
    modified = False
    
    # Fix: `{In}., |d=value...` -> `{In}, |d=value... .`
    # Pattern: anything ending with `}., |d=` followed by value
    m = re.match(r'^(.+?\{I\d+\})\.\,(\s*\|d=.+?)(\.?)\s*$', line)
    if m:
        before = m.group(1)  # e.g., "152GD2cG {I4}"
        after = m.group(2)   # e.g., " |d=-2.83 {I4}"
        # Ensure period at end
        if not after.rstrip().endswith('.'):
            after = after.rstrip() + '.'
        new_line = before + ',' + after
        new_line = new_line.ljust(80)
        lines[i] = new_line
        fixed += 1
        continue
    
    # Fix: `{In}., |d>value` for limits (no {I} uncertainty)
    m = re.match(r'^(.+?\{I\d+\})\.\,(\s*\|d=>[\d.]+)(\.?)\s*$', line)
    if m:
        before = m.group(1)
        after = m.group(2).replace('|d=>', '|d>')  # Fix => to >
        if not after.rstrip().endswith('.'):
            after = after.rstrip() + '.'
        new_line = before + ',' + after
        new_line = new_line.ljust(80)
        lines[i] = new_line
        fixed += 1
        continue
    
    # Fix standalone |d=> (in case pattern 1 didn't match)
    if '|d=>' in line:
        line = line.replace('|d=>', '|d>')
        lines[i] = line
        fixed += 1
        continue

print(f"Fixed {fixed} lines")

# Write back
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'w') as f:
    f.write('\n'.join(lines))

# Verify
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens', 'r') as f:
    verify = f.read()

# Check remaining issues
bad_comma_period = verify.count('., |d')
bad_arrow = verify.count('|d=>')
print(f"Remaining '., |d' instances: {bad_comma_period}")
print(f"Remaining '|d=>' instances: {bad_arrow}")

# Show first few fixed lines
for i, l in enumerate(lines):
    if '|d' in l and i > 60 and i < 175:
        print(f"L{i+1}: {l.rstrip()[:100]}")
        break
