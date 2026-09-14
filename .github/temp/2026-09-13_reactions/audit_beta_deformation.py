#!/usr/bin/env python3
"""Item 6: verify beta-2 deformation text |b{-2}(p,p') unchanged vs HEAD."""
import subprocess

REPO = r"d:\X\ND\ENSDF"
TARGET = "A34/S34/new/S34_adopted.ens"

cur = open(rf"{REPO}\A34\S34\new\S34_adopted.ens", "rb").read()
head = subprocess.run(["git", "show", f"HEAD:{TARGET}"], cwd=REPO,
                      capture_output=True).stdout


def lines(d):
    return [b.rstrip(b"\r\n") for b in d.split(b"\n")]


PATTERNS = {
    "EXACT  beta-2 (p,p')": b"|b{-2}(p,p')",
    "BROAD  any |b{-2}": b"|b{-2}",
}

for label, pat in PATTERNS.items():
    print("=" * 78)
    print(f"SEARCH: {label}   pattern={pat!r}")
    cl = [l for l in lines(cur) if pat in l]
    hl = [l for l in lines(head) if pat in l]
    print(f"  occurrences in CURRENT: {len(cl)}")
    for l in cl:
        print(f"    CURR: {l.decode('latin-1')!r}")
    print(f"  occurrences in HEAD   : {len(hl)}")
    for l in hl:
        print(f"    HEAD: {l.decode('latin-1')!r}")
    same = sorted(cl) == sorted(hl)
    print(f"  SETS IDENTICAL (content, EOL-normalized): {same}")

print("\n" + "=" * 78)
print("Explicit set-difference on the BROAD pattern, content-core compared:")
cset = set(lines(cur))
hset = set(lines(head))
bpat = b"|b{-2}"
conly = sorted(l for l in cset - hset if bpat in l)
honly = sorted(l for l in hset - cset if bpat in l)
print(f"  in CURRENT only: {len(conly)}")
for l in conly:
    print("    +", l.decode("latin-1"))
print(f"  in HEAD only   : {len(honly)}")
for l in honly:
    print("    -", l.decode("latin-1"))
print()
print("RESULT:", "PASS (unchanged)" if not conly and not honly else "FAIL (changed)")
