"""
Apply all 31 $E(p)(lab)= weighted average replacements from ep_averages2.json.
Works at the raw-text level (CRLF-aware); each old string is found once and
replaced with the new single-line string. No 80-char wrapping applied.
"""
import json, re

FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
JSON = r'd:\X\ND\ENSDF\.github\temp\ep_averages2.json'

data = json.load(open(JSON))
replacements = data['replacements']

raw = open(FILE, 'rb').read()
content = raw.decode('ascii')
original_lines = content.count('\r\n') + 1

applied = 0
failed = []

for idx, r in enumerate(replacements):
    old_str = r['old']    # may contain \r\n for 2-line cases
    new_str = r['new']    # single line, no \r\n

    # Count occurrences
    count = content.count(old_str)
    if count == 0:
        failed.append((idx, 'NOT FOUND', old_str[:80]))
        print(f'[{idx:02d}] FAILED NOT FOUND: {repr(old_str[:60])}')
        continue
    if count > 1:
        failed.append((idx, 'AMBIGUOUS', old_str[:80]))
        print(f'[{idx:02d}] FAILED AMBIGUOUS ({count}x): {repr(old_str[:60])}')
        continue

    content = content.replace(old_str, new_str, 1)
    applied += 1
    # Extract avg value for display
    avg_m = re.search(r'\$E\(p\)\(lab\)=([^ ]+)', new_str)
    avg_display = avg_m.group(1) if avg_m else '?'
    print(f'[{idx:02d}] OK  avg={avg_display}  {new_str[20:70]}')

new_lines = content.count('\r\n') + 1

if not failed:
    with open(FILE, 'wb') as f:
        f.write(content.encode('ascii'))
    print(f'\nAll {applied}/31 replacements applied.')
    print(f'Lines: {original_lines} -> {new_lines} (delta {new_lines - original_lines})')
else:
    print(f'\nEXIT WITHOUT WRITING: {len(failed)} failures:')
    for idx, reason, snip in failed:
        print(f'  [{idx:02d}] {reason}: {snip[:80]}')
