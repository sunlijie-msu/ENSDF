"""Coverage check: comment units mentioning 'averag' but not phrased 'average of'."""
import io
import re

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
with io.open(AD, newline="") as fh:
    lines = fh.read().replace("\r\n", "\n").split("\n")

is_com = lambda l: len(l) >= 9 and l[6:7] == "c"
units = []
i = 0
while i < len(lines):
    l = lines[i]
    if is_com(l) and l[5:6] == " ":
        raw = [l]
        j = i + 1
        while j < len(lines) and is_com(lines[j]) and lines[j][5:6] != " ":
            raw.append(lines[j])
            j += 1
        units.append((i + 1, re.sub(r"\s+", " ", " ".join(r[9:] for r in raw)).strip()))
        i = j
        continue
    i += 1

tot = [u for u in units if re.search(r"averag", u[1], re.I)]
withof = [u for u in tot if re.search(r"averag\w*\s+of", u[1], re.I)]
print("comment units mentioning 'averag'      : %d" % len(tot))
print("  phrased 'average of' (checked by v4): %d" % len(withof))
print("  other phrasing (needs review)       : %d" % (len(tot) - len(withof)))
for n, t in tot:
    if not re.search(r"averag\w*\s+of", t, re.I):
        print("   line %d: %s" % (n, t[:150]))
