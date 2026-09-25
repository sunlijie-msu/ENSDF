"""Spot check: for selected average comments print quoted inputs, tool-parsed inputs,
tool results and the adopted record field, so each can be traced by hand."""
import io
import math
import re
import sys

sys.path.insert(0, r"d:\X\ND\ENSDF\.github\scripts")
import Java_Average as JA

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
SPOT = [91, 139, 202, 262, 393, 439, 457, 620, 829, 1124, 1382]
LN2 = math.log(2)

with io.open(AD, newline="") as fh:
    lines = fh.read().replace("\r\n", "\n").split("\n")

is_com = lambda l: len(l) >= 9 and l[6:7] == "c"
is_rec = lambda l: len(l) >= 9 and l[5:7] == "  " and l[7:8] in ("L", "G")

units = {}
i = 0
while i < len(lines):
    l = lines[i]
    if is_com(l) and l[5:6] == " ":
        raw = [l]
        j = i + 1
        while j < len(lines) and is_com(lines[j]) and lines[j][5:6] != " ":
            raw.append(lines[j])
            j += 1
        units[i + 1] = raw
        i = j
        continue
    i += 1

for n in SPOT:
    raw = units[n]
    text = re.sub(r"\s+", " ", " ".join(r[9:] for r in raw)).strip()
    # owner record
    owner = None
    k = n - 2
    while k >= 0:
        if is_rec(lines[k]):
            owner = lines[k]
            break
        k -= 1
    cut = re.split(r"\bOthers?\b", text[re.search(r"\baverage\s+of\b", text, re.I).end():], flags=re.I)[0]
    quoted = re.findall(r"([\d.]+)\s*(?:[A-Za-z]{1,4}\s*)?\{I([^}]+)\}", cut)
    data, unit, dec = JA.parse_comment_data(text)
    wt = JA.weighted_average(data)
    uw = JA.unweighted_average(data)
    print("=" * 100)
    print("comment line %d (owner record line %d)" % (n, k + 1))
    print("  quoted inputs : %s" % (", ".join("%s(%s)" % q for q in quoted),))
    print("  tool parsed   : %s" % (", ".join("%.6g(%.6g)" % (v, u) for v, u, _ in data),))
    print("  weighted      : %.6g(%.6g)  chi2/(n-1)=%.3f" % (wt["value"], wt["internal_unc"], wt["reduced_chi_sq"]))
    print("  unweighted    : %.6g(%.6g)" % (uw["value"], uw["final_unc"]))
    print("  owner record  : %s" % (repr(owner) if owner else "None"))
    if owner:
        print("     fields  E=%r DE=%r  RI=%r DRI=%r  T=%r DT=%r" % (owner[9:19], owner[19:21],
                                                                      owner[22:29], owner[29:31],
                                                                      owner[39:49], owner[49:55]))
