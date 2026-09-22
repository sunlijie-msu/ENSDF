import re
from pathlib import Path

base = Path(r"d:\X\ND\ENSDF\.github\temp\quoted_check")
ens = Path(r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens")
lines = ens.read_text(encoding="utf-8", errors="replace").splitlines()

summary = (base / "fresh_summary.txt").read_text(encoding="utf-8").splitlines()

errors = {}
order = []
for ln in summary:
    m = re.match(r"^\s*\d+\s+(\d+)\s+([A-Z_]+)\s+(\S.*)$", ln)
    if m:
        ln_no = int(m.group(1))
        if ln_no not in errors:
            errors[ln_no] = []
            order.append(ln_no)
        errors[ln_no].append(f"{m.group(2)}: {m.group(3)}")


def gam_list(start):
    """gammas of the level block that starts at or before `start`"""
    i = start
    while i >= 0:
        p = lines[i]
        if len(p) > 8 and p[5] == " " and p[6] == " " and p[7] in "LG":
            break
        i -= 1
    e = lines[i][9:19].strip()
    out = []
    j = i + 1
    while j < len(lines):
        p = lines[j]
        if len(p) > 8 and p[5] == " " and p[6] == " " and p[7] in "LG":
            if p[7] == "L":
                break
            out.append(p[9:19].strip())
        j += 1
    return e, out


for ln_no in order:
    start = ln_no - 1
    i = start
    while i >= 0:
        p = lines[i]
        if len(p) > 8 and p[5] == " " and p[6] == " " and p[7] in "LG":
            break
        i -= 1
    lev, gams = gam_list(start)
    # comment block containing the error line
    s = start
    while s - 1 >= 0 and (len(lines[s - 1]) > 7 and lines[s - 1][6] == "c"):
        s -= 1
    e = start
    while e + 1 < len(lines) and (len(lines[e + 1]) > 7 and lines[e + 1][6] == "c"):
        e += 1
    print(f"=== L{ln_no}  levelE={lev}  gammas={','.join(gams)}")
    for x in errors[ln_no]:
        print(f"    ! {x}")
    for k in range(s, e + 1):
        print(f"  {k+1:>5}|{lines[k][:80]}")
    print()
