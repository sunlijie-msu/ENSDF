"""
Batch B: Add periods to all single-line $E(p)(lab)= comment lines that
are missing a period at the end.
Also handles:
- Lines WITHOUT uncertainty but WITH citation: 1900 (1977Da02) → add period
- Lines WITHOUT citation (1992Ka39 style): `1898 {I1}` → add period
"""
import re

raw_bytes = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read()
content = raw_bytes.decode('ascii')
lines = content.split('\r\n')
original_lines = len(lines)

# Pattern: lines starting with " 34CL cL $E(p)(lab)=" that don't end with "."
# (checking the stripped content, not including trailing spaces)
ep_pattern = re.compile(r'^( 34CL cL \$E\(p\)\(lab\)=.+?)(\s*)$')

modified_count = 0
new_lines = []
for i, line in enumerate(lines):
    # Check if this is an Ep comment line
    if ' 34CL cL $E(p)(lab)=' not in line:
        new_lines.append(line)
        continue
    stripped = line.rstrip()
    if stripped.endswith('.'):
        # Already has period, skip
        new_lines.append(line)
        continue
    # Add period to stripped content (no padding needed - user said no 80-col)
    new_content = stripped + '.'
    new_lines.append(new_content)
    modified_count += 1
    print(f'L{i+1}: Added period: {repr(stripped[-30:])}')

if modified_count == 0:
    print('No lines needed period additions.')
else:
    new_content_str = '\r\n'.join(new_lines)
    with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'wb') as f:
        f.write(new_content_str.encode('ascii'))
    print(f'\nModified {modified_count} lines. File written.')
    print(f'Original lines: {original_lines}, New lines: {len(new_lines)}')
