"""
Identify all cL $E{-p}(lab)= lines that are:
  - Single value, NO parenthetical citation (1992Ka39-only resonances)
  - Format: $E{-p}(lab)=NNNN {I1}.
Then check their L records for col77 state.
"""
import re

FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
raw = open(FILE, 'rb').read()
content = raw.decode('ascii')
lines = content.split('\r\n')

target_lines = []   # (0-based index of cL line, L-rec 0-based index)
with_citation = []
weighted_avg  = []

for i, line in enumerate(lines):
    stripped = line.rstrip()
    if 'cL $E{-p}(lab)=' not in stripped:
        continue

    # Detect category
    if ': weighted average' in stripped:
        weighted_avg.append(i+1)
        continue
    
    has_paren = bool(re.search(r'\(\d{4}[A-Z][a-z]', stripped))
    if has_paren:
        with_citation.append(i+1)
        continue

    # This is a 1992Ka39-only single-value line (no citation)
    # Find the L record above
    l_rec_idx = None
    for j in range(i-1, -1, -1):
        s = lines[j].rstrip()
        if len(s) >= 8 and s[7] == 'L' and s[5] == ' ' and s[6] == ' ':
            l_rec_idx = j
            break

    if l_rec_idx is None:
        print(f'WARNING: No L-rec found for cL at line {i+1}')
        continue

    l_rec = lines[l_rec_idx]
    # Pad to 80 chars for col77 check
    col77 = l_rec[76] if len(l_rec) >= 77 else ' '
    target_lines.append({
        'cl_idx': i,        # 0-based
        'l_idx':  l_rec_idx,  # 0-based
        'cl_line': stripped,
        'l_line': l_rec.rstrip(),
        'col77': col77,
        'l_len': len(l_rec.rstrip()),
    })

print(f'Target (1992Ka39 no-cit): {len(target_lines)}')
print(f'With citation:            {len(with_citation)}')
print(f'Weighted averages:        {len(weighted_avg)}')
print()

# Check col77 states
col77_states = {}
for t in target_lines:
    c = t['col77']
    col77_states[c] = col77_states.get(c, 0) + 1
print('Col77 distribution in target L records:', col77_states)

# Show any non-space col77
print('\nNon-space col77 in targets:')
for t in target_lines:
    if t['col77'] != ' ':
        print(f'  L{t["l_idx"]+1}: col77={repr(t["col77"])}: {t["l_line"]}')

# Also show first/last few targets
print('\nFirst 3 targets:')
for t in target_lines[:3]:
    print(f'  L-rec L{t["l_idx"]+1}: {t["l_line"]}')
    print(f'  cL    L{t["cl_idx"]+1}: {t["cl_line"]}')
    print()
print('Last 3 targets:')
for t in target_lines[-3:]:
    print(f'  L-rec L{t["l_idx"]+1}: {t["l_line"]}')
    print(f'  cL    L{t["cl_idx"]+1}: {t["cl_line"]}')
    print()
