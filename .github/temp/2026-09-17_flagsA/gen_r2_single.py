"""Single-op pairs for ALL remaining R2 lines: OLD = current full line, NEW = line with A at col77."""
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
    new = ln[:76] + "A" + ln[77:]
    out.append(f"[{lev} g={g}]")
    out.append("OLD>>>" + ln)
    out.append("NEW>>>" + new)
    n += 1

open(r".github/temp/2026-09-17_flagsA\r2_single.txt", "w", encoding="utf-8").write("\n".join(out))
print("remaining lines:", n)
