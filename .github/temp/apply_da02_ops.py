"""Apply 54 sequential 1977Da02 EP+WG replacement ops to Cl34_33s_p_g.ens."""
import json, sys

ops_file = r'.github\temp\da02_ops.json'
ens_file = r'A34\Cl34\new\Cl34_33s_p_g.ens'

with open(ops_file) as f:
    ops = json.load(f)

with open(ens_file, newline='') as f:
    content = f.read()

applied = 0
errors = []
for i, op in enumerate(ops):
    old = op['oldString']
    new = op['newString']
    cnt = content.count(old)
    if cnt == 1:
        content = content.replace(old, new, 1)
        applied += 1
    else:
        errors.append((i+1, op['_desc'], cnt))
        print('ERROR op %d (%s): count=%d' % (i+1, op['_desc'], cnt))

if errors:
    print('ABORTED: %d errors. File NOT written.' % len(errors))
    sys.exit(1)

with open(ens_file, 'w', newline='') as f:
    f.write(content)

print('Applied %d ops successfully. File updated.' % applied)
