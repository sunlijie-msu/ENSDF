import json, sys

with open(r'.github\temp\da02_ops.json') as f:
    ops = json.load(f)

filepath = r'A34\Cl34\new\Cl34_33s_p_g.ens'
with open(filepath, newline='') as f:
    content = f.read()

counts = [content.count(op['oldString']) for op in ops]
errs = [(i+1, ops[i]['_desc'], c) for i, c in enumerate(counts) if c != 1]

print('Total ops: %d' % len(ops))
print('Unique (count=1): %d' % sum(1 for c in counts if c == 1))
print('Errors: %d' % len(errs))
for num, desc, cnt in errs:
    print('  ERR op%d: %s (count=%d)' % (num, desc, cnt))

if not errs:
    print('ALL OK - safe to apply')
    sys.exit(0)
else:
    sys.exit(1)
