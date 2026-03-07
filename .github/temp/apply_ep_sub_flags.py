"""
For each 1992Ka39-only $E{-p}(lab)= level:
  1. Add 'K' at col 77 of the L record
  2. Remove the cL $E{-p}(lab)=... line

L-records are padded to 80 chars. Col77 index = 76 (0-based).
"""
import re

FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

raw = open(FILE, 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')
original_count = len(lines)

# Collect targets (same logic as scan_ep_sub2.py)
targets = []
for i, line in enumerate(lines):
    stripped = line.rstrip()
    if 'cL $E{-p}(lab)=' not in stripped:
        continue
    if ': weighted average' in stripped:
        continue
    if re.search(r'\(\d{4}[A-Z][a-z]', stripped):
        continue

    # Find L record above
    l_rec_idx = None
    for j in range(i-1, -1, -1):
        s = lines[j].rstrip()
        if len(s) >= 8 and s[7] == 'L' and s[5] == ' ' and s[6] == ' ':
            l_rec_idx = j
            break
    if l_rec_idx is None:
        print(f'WARNING: No L-rec for cL at {i+1}')
        continue
    targets.append((l_rec_idx, i))   # (L-rec 0-based, cL 0-based)

print(f'Targets: {len(targets)}')

# Apply changes in reverse order of line index to avoid shifting
# Process cL lines first (mark for removal) then L records
# Use a set of indices for removal, dict for L-rec modifications
cl_to_remove = set()
l_to_modify  = {}   # idx -> new line string

for l_idx, cl_idx in targets:
    cl_to_remove.add(cl_idx)
    
    l_raw = lines[l_idx]
    # Pad to 80 chars if shorter
    if len(l_raw) < 80:
        l_raw_padded = l_raw.rstrip('\r\n').ljust(80)
    else:
        l_raw_padded = l_raw.rstrip('\r\n')
    
    # Sanity: col77 (0-based index 76) should be space
    if l_raw_padded[76] != ' ':
        print(f'WARNING L{l_idx+1}: col77 already occupied: {repr(l_raw_padded[76])}')
        continue
    
    # Set col 77 to K
    new_l = l_raw_padded[:76] + 'K' + l_raw_padded[77:]
    # Trim trailing spaces to original length behavior (keep 80)
    new_l = new_l[:80]
    l_to_modify[l_idx] = new_l

print(f'L-records to modify: {len(l_to_modify)}')
print(f'cL lines to remove:  {len(cl_to_remove)}')

# Build new lines list
new_lines = []
modified_L = 0
removed_cL = 0
for i, line in enumerate(lines):
    if i in cl_to_remove:
        removed_cL += 1
        continue
    if i in l_to_modify:
        new_lines.append(l_to_modify[i])
        modified_L += 1
    else:
        new_lines.append(line)

print(f'Modified L: {modified_L}, Removed cL: {removed_cL}')
print(f'Lines: {original_count} -> {len(new_lines)} (delta {len(new_lines)-original_count})')

# Spot-check: verify a few L records got K at col77
print('\nSpot-check (first 3 modified L records):')
first3 = sorted(l_to_modify.keys())[:3]
for idx in first3:
    new_l = l_to_modify[idx]
    print(f'  L{idx+1}: col77={repr(new_l[76])}: {new_l}')

# Verify no cL $E{-p}(lab)= lines without citations remain
remaining = [i+1 for i, l in enumerate(new_lines)
             if 'cL $E{-p}(lab)=' in l
             and not re.search(r'\(\d{4}[A-Z][a-z]', l)
             and ': weighted average' not in l]
print(f'\nRemaining no-cit $E{{-p}}(lab)= lines: {len(remaining)}')
if remaining:
    for ln in remaining[:5]:
        print(f'  L{ln}: {new_lines[ln-1].rstrip()}')

# Write file
new_content = '\r\n'.join(new_lines)
with open(FILE, 'wb') as f:
    f.write(new_content.encode('ascii'))
print('\nFile written.')
