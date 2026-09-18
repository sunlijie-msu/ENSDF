"""Final verify: all R2 targets have A (col77, len80); R1 targets clean; no '@' anywhere."""
import re

raw = open(r"A34/S34/new/S34_adopted.ens", encoding="utf-8", newline="").read().replace("\r\n", "\n")
lines = raw.split("\n")
pairs = open(r".github/temp/2026-09-17_flagsA/edit_pairs_A4.txt", encoding="utf-8").read()

print("@ residue:", raw.count("@"), " X residue:", raw.count("X   \n"))

n_bad = 0
n_ok = 0
for m in re.finditer(r"\[R2-(\S+)\] line (\d+) level (\S+) g=(\S+)", pairs):
    kind, _, lev, g = m.groups()
    hit = None
    for ln in lines:
        if re.match(rf"^ 34S   G {re.escape(g)}\s", ln):
            hit = ln
            break
    if hit is None:
        print("R2 MISSING", lev, g); n_bad += 1; continue
    if len(hit) == 80 and hit[76] == "A":
        n_ok += 1
    else:
        print(f"R2 BAD {lev} g={g}: len={len(hit)} col77={hit[76]!r}")
        n_bad += 1
print(f"R2: ok={n_ok} bad={n_bad}")

n_ok = n_bad = 0
for lev in ("10447", "10528", "10617", "10869", "10895", "10917", "11180", "11194", "11289"):
    for ln in lines:
        if ln.startswith(" 34S   L " + lev):
            if len(ln) == 80 and ln[76] == " ":
                n_ok += 1
            else:
                print(f"R1 BAD {lev}: len={len(ln)} col77={ln[76]!r}"); n_bad += 1
            break
print(f"R1: ok={n_ok} bad={n_bad}")
