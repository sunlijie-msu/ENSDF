"""Dump every average-related comment block in an ENSDF file, joined, with owning data record."""
import re

PATH = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"

lines = open(PATH, encoding="utf-8", errors="replace").read().split("\n")
if lines and lines[-1] == "":
    lines.pop()


def is_data(l):
    return len(l) > 8 and l[5] == " " and l[6] == " " and l[7] in "LG" and l[8] == " "


def is_comment_start(l):
    return len(l) > 6 and l[5] == " " and l[6] == "c"


def is_cont(l):
    return len(l) > 7 and l[5] != " " and l[6] == "c"


blocks = []
i = 0
while i < len(lines):
    if is_comment_start(lines[i]):
        j = i
        txt = []
        ident = None
        while j < len(lines) and (is_comment_start(lines[j]) or is_cont(lines[j])):
            body = lines[j][7:].rstrip()
            if ident is None:
                m = re.match(r"^([A-Z0-9,$()+-]*\$)", body)
                ident = m.group(1) if m else "?"
            txt.append(body)
            j += 1
        joined = " ".join(t.strip() for t in txt)
        blocks.append((i + 1, ident, joined, j - i))
        i = j
    else:
        i += 1

out = []
for start, ident, joined, n in blocks:
    if not re.search(r"averag|mean", joined, re.I):
        continue
    owner = None
    for k in range(start - 2, -1, -1):
        if is_data(lines[k]):
            owner = (k + 1, lines[k])
            break
    out.append((start, owner, ident, joined, n))

for start, owner, ident, joined, n in out:
    print("=" * 100)
    print("CMT line %d (%d lines) id=%s OWNER %s: %s" % (start, n, ident, owner[0] if owner else "-", owner[1] if owner else "-"))
    print(joined)
print("TOTAL average blocks:", len(out))
