"""Generate single-line R2 op pairs from CURRENT file bytes.

Per line: op1: C2+run -> C2+run+'@'  |  op2: C2+run+'@' -> C2+run+'A'
Skips any line already flagged A."""
import re

raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
pairs = open(r".github/temp/2026-09-17_flagsA/edit_pairs_A4.txt", encoding="utf-8").read()

out = []
n = 0
for m in re.finditer(r"\[R2-(\S+)\] line (\d+) level (\S+) g=(\S+)", pairs):
    kind, _, lev, g = m.groups()
    pat = re.compile(rf"^ 34S   G {re.escape(g)}\s")
    hits = [k for k, ln in enumerate(lines) if pat.match(ln)]
    if len(hits) != 1:
        out.append(f"# SKIP {lev} g={g}: {len(hits)} hits")
        continue
    i = hits[0]
    ln = lines[i]
    if len(ln) != 80:
        out.append(f"# SKIP {lev} g={g}: len={len(ln)}")
        continue
    if ln[76] == "A":
        out.append(f"# DONE {lev} g={g}")
        continue
    if ln[76] != " ":
        out.append(f"# SKIP {lev} g={g}: flag={ln[76]!r}")
        continue
    C2 = ln[:76].rstrip()
    run = 76 - len(C2)
    out.append(f"[{lev} g={g}] run={run}")
    out.append("O1>>>" + C2 + " " * run)
    out.append("O2>>>" + C2 + " " * run + "@")
    out.append("N2>>>" + C2 + " " * run + "A")
    n += 1

open(r".github/temp/2026-09-17_flagsA\r2_ops.txt", "w", encoding="utf-8").write("\n".join(out))
print("lines to do:", n)
print("written r2_ops.txt; head:")
print("\n".join(out[:12]))
