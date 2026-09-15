"""Compare the unplaced G block now present in the .ens file against expected_block.txt."""
import os, sys

ENS = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
HERE = os.path.dirname(os.path.abspath(__file__))
exp = [l for l in open(os.path.join(HERE, 'expected_block.txt'), encoding='ascii').read().split('\n') if l]
raw = open(ENS, encoding='ascii').read()
crlf = raw.count('\r\n')
print("CRLF endings:", crlf, "| bare LF:", raw.count('\n') - crlf)
lines = raw.split('\r\n') if crlf else raw.split('\n')


def typ(s):
    return s[6:8].strip() if len(s) >= 8 else ''


pn = next(i for i, s in enumerate(lines) if typ(s) == 'PN')
blk = []
i = pn + 1
while i < len(lines):
    s = lines[i]
    if typ(s) == 'G':
        blk.append((i + 1, s))
    elif typ(s) == 'L':
        break
    i += 1
print("PN at line", pn + 1, "| block records:", len(blk), "| expected:", len(exp))
bad = 0
for k in range(max(len(blk), len(exp))):
    got = blk[k][1] if k < len(blk) else None
    want = exp[k] if k < len(exp) else None
    if got != want:
        bad += 1
        if bad <= 30:
            print("DIFF idx %d (file line %s)" % (k + 1, blk[k][0] if k < len(blk) else '-'))
            print("  want |%s| len=%s" % (want, len(want) if want else None))
            print("  got  |%s| len=%s" % (got, len(got) if got else None))
print("mismatched records:", bad)
lens = set(len(b[1]) for b in blk)
print("record lengths present:", sorted(lens))
