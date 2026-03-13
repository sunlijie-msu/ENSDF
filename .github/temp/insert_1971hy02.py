import re
from pathlib import Path

f = Path(r'A34/Cl34/new/Cl34_33s_p_g.ens')
lines = f.read_text(encoding='utf-8').splitlines(keepends=True)

insertions = [
    ('T[$]lifetime [|]t=201 fs',   '2377.3 {I12} (1971Hy02)'),
    ('T[$]lifetime [|]t=230 fs',   '2611.2 {I13} (1971Hy02)'),
    ('T[$]lifetime [|]t>400 fs',   '2721.7 {I3} (1971Hy02)'),
    ('T[$]lifetime [|]t=147 fs',   '3545.3 {I6} (1971Hy02)'),
    ('T[$]lifetime [|]t>0.7 ps',   '3600.7 {I4} (1971Hy02)'),
    ('T[$]lifetime [|]t>700 fs',   '3632.5 {I14} (1971Hy02)'),
    ('T[$]lifetime [|]t=75 fs',    '3771.0 {I7} (1971Hy02)'),
    ('T[$]lifetime [|]t=189 fs',   '3982.1 {I3} (1971Hy02)'),
    ('T[$]lifetime [|]t>0.25 ps',  '4075.4 {I9} (1971Hy02)'),
    ('T[$]lifetime [|]t=129 fs',   '4136.6 {I12} (1971Hy02)'),
    ('T[$]lifetime [|]t=43 fs',    '4352.7 {I9} (1971Hy02)'),
    ('T[$]lifetime [|]t=35 fs',    '4415.8 {I23} (1971Hy02)'),
    ('T[$]lifetime [|]t=15 fs',    '4514.5 {I7} (1971Hy02)'),
    ('T[$]lifetime [|]t=45 fs',    '4639.0 {I23} (1971Hy02)'),
]

remaining = list(insertions)
result = []
inserted = 0

for i, line in enumerate(lines):
    for anchor, val in remaining:
        if re.search(anchor, line):
            new_line = ' 34CL cL E$other: ' + val
            new_line = new_line.ljust(80) + '\n'
            result.append(new_line)
            print('Line %d: inserted %r' % (i+1, new_line.rstrip()))
            remaining.remove((anchor, val))
            inserted += 1
            break
    result.append(line)

print('Total insertions:', inserted)
if inserted == 14:
    f.write_text(''.join(result), encoding='utf-8')
    print('File written successfully.')
else:
    print('ERROR: expected 14, got', inserted)
    print('Not matched:', [a for a,v in remaining])
