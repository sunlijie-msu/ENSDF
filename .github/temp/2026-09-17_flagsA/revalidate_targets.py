"""Re-validate all 67 target lines against the CURRENT file state."""
import re

raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
pairs = open(r".github/temp/2026-09-17_flagsA/edit_pairs_A4.txt", encoding="utf-8").read()

ok = bad = 0
for m in re.finditer(r"OLD>>>(.*)", pairs):
    line = m.group(1).split("\n")[0]
    c = raw.count(line)
    if c != 1:
        bad += 1
        print("PROBLEM count", c, ":", repr(line[:50]))
    else:
        ok += 1
print("ok:", ok, " bad:", bad)
