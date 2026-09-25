"""T$-comment check: quoted tau vs tool internal/external/suggested."""
import io
import math
import re
import sys

sys.path.insert(0, r"d:\X\ND\ENSDF\.github\scripts")
import Java_Average as JA

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
TROWS = [91, 126, 165, 212, 241, 275, 439, 694, 855, 939]
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

print("%-6s %-14s %-14s %-14s %-14s %-18s %-12s" % (
    "line", "quoted", "wt-internal", "wt-external", "unweighted", "suggested", "record T(ps)"))
for n in TROWS:
    raw = units[n]
    text = re.sub(r"\s+", " ", " ".join(r[9:] for r in raw)).strip()
    owner = None
    k = n - 2
    while k >= 0:
        if is_rec(lines[k]):
            owner = lines[k]
            break
        k -= 1
    data, unit, dec = JA.parse_comment_data(text)
    n_d = len(data)
    wt = JA.weighted_average(data)
    uw = JA.unweighted_average(data)
    crit = JA.critical_chi_sq_display(n_d)
    eff = max(JA.INCONSISTENCY_THRESHOLD, crit)
    if wt["reduced_chi_sq"] <= eff:
        val, unc = wt["value"], JA.find_suggested_average(max(wt["internal_unc"], wt["external_unc"]), data)
    else:
        val, unc = uw["value"], JA.find_suggested_average(uw["final_unc"], data)
    sugg = JA.fmt_val_unc(val, unc, dec)
    pre = text[: re.search(r"\baverage\s+of\b", text, re.I).start()]
    q = re.findall(r"([\d.]+)\s*(?:[A-Za-z]{1,4}\s*)?\{I([^}]+)\}", pre)
    qs = "%s(%s)" % q[-1] if q else "-"
    print("%-6d %-14s %-14s %-14s %-14s %-18s %-12s" % (
        n, qs,
        JA.fmt_val_unc(wt["value"], wt["internal_unc"], dec),
        JA.fmt_val_unc(wt["value"], wt["external_unc"], dec),
        JA.fmt_val_unc(uw["value"], uw["final_unc"], dec),
        sugg,
        owner[39:49].strip() + "/" + owner[49:55].strip()))
