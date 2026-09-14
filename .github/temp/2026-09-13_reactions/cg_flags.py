"""Report G-record comment-flag (column 77) usage and check which G-records are
described by a cG comment that cites {+31}P(|a,p|g) while carrying no flag.

Usage: python cg_flags.py FILE
"""
import re
import sys
from collections import Counter

raw = open(sys.argv[1], 'r', encoding='utf-8', errors='replace').read().replace('\r\n', '\n')
lines = raw.split('\n')

records = []          # (index, line)
comments = []         # (index, line)
for i, ln in enumerate(lines):
    if len(ln) < 8:
        continue
    if ln[6] != ' ' and ln[7] == 'G':          # cG / 2cG / dG comment line
        comments.append((i, ln))
    elif ln[6] == ' ' and ln[7] == 'G':        # G data record
        records.append((i, ln))

flag_hist = Counter()
p31 = []
for idx, ln in records:
    flag = ln[76] if len(ln) > 76 else ' '
    flag_hist[flag] += 1
    # collect immediately following comment lines about this gamma
    txt = []
    for j, cl in comments:
        if j < idx:
            continue
        if any(idx < k < j for k, _ in records):
            break
        txt.append(cl[8:].strip())
    body = ' '.join(txt)
    if '{+31}P(|a,p|g)' in body:
        p31.append((idx + 1, ln[:33].rstrip(), repr(flag), body[:70]))

print('G-records: %d' % len(records))
print('column 77 usage:', dict(flag_hist))
print()
print('G-records whose cG comment cites {+31}P(|a,p|g): %d' % len(p31))
with_flag = [r for r in p31 if r[2] != "' '"]
without = [r for r in p31 if r[2] == "' '"]
print('  with a col-77 flag   : %d' % len(with_flag))
print('  WITHOUT any col-77 flag: %d' % len(without))
print()
print('--- WITHOUT flag (line, G-record head, flag, comment) ---')
for r in without:
    print('%6d | %-32s | flag=%s | %s' % r)
print()
print('--- WITH flag ---')
for r in with_flag:
    print('%6d | %-32s | flag=%s | %s' % r)

# breakdown: which comment identifier cites 31P
buckets = Counter()
for idx, head, flag, body in p31:
    ids = []
    for ident in ('E,RI$', 'RI$', 'E$', 'M$', 'MR$'):
        if ident in body:
            ids.append(ident)
    buckets[('%s' % '+'.join(ids) if ids else 'general', flag)] += 1
print()
print('--- breakdown (comment identifier(s) citing 31P | col-77 flag) ---')
for k, v in sorted(buckets.items(), key=lambda kv: -kv[1]):
    print('%-14s | flag=%-4s : %d' % (k[0], k[1], v))

print()
print('--- G-records whose RI is cited from 31P and col 77 is blank ---')
ri_needs = []
for idx, head, flag, body in p31:
    if flag == "' '" and ('RI$' in body):
        ri_needs.append(idx + 1)
        print('%6d | %s' % (idx + 1, head))
print('count: %d' % len(ri_needs))
print('lines: %s' % ','.join(str(x) for x in ri_needs))

print()
print('--- every G-record that already carries M in col 77 ---')
for idx, ln in records:
    if len(ln) > 76 and ln[76] == 'M':
        body = []
        for j, cl in comments:
            if j < idx:
                continue
            if any(idx < k < j for k, _ in records):
                break
            body.append(cl[8:].strip())
        print('%6d | %-33s | %s' % (idx + 1, ln[:33].rstrip(), ' '.join(body)[:60]))
