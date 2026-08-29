import re
d = open(r'd:\X\ND\ENSDF\.github\temp\vdiff.txt', encoding='utf-16').read()
lines = d.splitlines()
changed = [l for l in lines if l.startswith('+') and not l.startswith('+++')]
removed = [l for l in lines if l.startswith('-') and not l.startswith('---')]
print('added lines:', len(changed), 'removed lines:', len(removed))
non_g = [l for l in changed + removed if not re.match(r'^[+-] 34S   G ', l)]
print('non-G-record changed lines:', len(non_g))
for l in non_g[:30]:
    print('  ', repr(l))
# verify every added G line has V at col 77 (index 76)
bad = []
for l in changed:
    if re.match(r'^\+ 34S   G ', l):
        body = l[1:]
        if len(body) != 80 or body[76] != 'V':
            bad.append(l)
print('added G lines without V@77:', len(bad))
for l in bad[:10]:
    print('  BAD', repr(l))
