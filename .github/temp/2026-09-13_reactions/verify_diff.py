"""Verify that the working-tree diff for the adopted file consists only of
comment lines whose sole change is the insertion of a target nucleus before a
bare reaction notation.

Usage: python verify_diff.py REPO_FILE
"""
import re
import subprocess
import sys

path = sys.argv[1]

RULES = [
    (r'(?<=[ $])(\(\|a,\|g\),\(\|a,n\))', '{+30}Si'),
    (r'(?<=[ $])(\(\|a,\|g\))', '{+30}Si'),
    (r'(?<=[ $])(\(\|a,n\))', '{+30}Si'),
    (r'(?<=[ $])(\(\|a,\|a\'\))', '{+34}S'),
    (r'(?<=[ $])(\(\|a,p\|g\))', '{+31}P'),
    (r'(?<=[ $])(\(n,\|g\),\(n,n\))', '{+33}S'),
    (r'(?<=[ $])(\(n,\|g\))', '{+33}S'),
    (r'(?<=[ $])(\(n,n\))', '{+33}S'),
    (r'(?<=[ $])(\(\{\+16\}O,\|a2p\|g\))', '{+24}Mg'),
    (r'(?<=[ $])(\(\{\+36\}S,\{\+34\}S\|g\))', '{+208}Pb'),
    (r'(?<=[ $])(\(p,p\),\(p,p\'\),\(pol p,p\'\))', '{+34}S'),
    (r'(?<=[ $])(\(p,p\'\|g\))', '{+34}S'),
    (r'(?<=[ $])(\(p,p\'\))', '{+34}S'),
    (r'(?<=[ $])(\(p,p\))', '{+34}S'),
    (r'(?<=[ $])(\(pol p,p\'\))', '{+34}S'),
    (r'(?<=[ $])(\(t,p\))', '{+32}S'),
    (r'(?<=[ $])(\(d,p\))', '{+33}S'),
    (r'(?<=[ $])(\(d,\{\+3\}He\))', '{+35}Cl'),
    (r'(?<=[ $])(\(pol \|g,\|g\'\))', '{+34}S'),
    (r'(?<=[ $])(\(\|g,\|g\'\))', '{+34}S'),
    (r'(?<=[ $])(\(e,e\'\))', '{+34}S'),
]


def fix(line):
    new = line
    for frag, prefix in RULES:
        new = re.sub(frag, lambda m, p=prefix: p + m.group(1), new)
    return new


diff = subprocess.run(['git', 'diff', '--unified=0', '--', path],
                      capture_output=True, text=True).stdout
removed, added = [], []
for ln in diff.split('\n'):
    if ln.startswith('---') or ln.startswith('+++'):
        continue
    if ln.startswith('-'):
        removed.append(ln[1:].rstrip('\r'))
    elif ln.startswith('+'):
        added.append(ln[1:].rstrip('\r'))

print('removed lines: %d   added lines: %d' % (len(removed), len(added)))

data_removed = sorted(set(l.rstrip() for l in removed if len(l) > 7 and l[6] == ' '))
data_added = sorted(set(l.rstrip() for l in added if len(l) > 7 and l[6] == ' '))
print('DISTINCT data-record lines touched: removed %d added %d'
      % (len(data_removed), len(data_added)))
only_removed = [l for l in data_removed if l not in data_added]
only_added = [l for l in data_added if l not in data_removed]
print('  data lines whose content changed: %d removed-only, %d added-only'
      % (len(only_removed), len(only_added)))
for l in only_removed[:10]:
    print('   - DATA %s' % l)
for l in only_added[:10]:
    print('   + DATA %s' % l)

fixed_set = set(fix(r.rstrip()) for r in removed)
unexplained_added = [a for a in added if a.rstrip() not in fixed_set]
print('added lines not explained by a removed-line fix: %d' % len(unexplained_added))
for l in unexplained_added[:30]:
    print('  ADD [%s]' % l.rstrip())

added_set = set(a.rstrip() for a in added)
unexplained_removed = [r for r in removed if r.rstrip() not in added_set
                       and fix(r.rstrip()) not in added_set]
print('removed lines not explained by an added-line fix: %d' % len(unexplained_removed))
for l in unexplained_removed[:30]:
    print('  DEL [%s]' % l.rstrip())

untouched = [l for l in removed if l.strip() and '|b{-2}' in l]
print('beta-deformation lines touched: %d' % len(untouched))
