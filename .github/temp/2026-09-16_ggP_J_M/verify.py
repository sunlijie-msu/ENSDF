"""Read-only verification of the g_gP J/M reconciliation in the target."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

TARGETS = ["8185.46", "8656", "9479", "9868", "10170", "10803"]

def is_level_start(s):
    return len(s) > 7 and s[5] == " " and s[6] == " " and s[7] == "L"

for t in TARGETS:
    idx = [i for i, l in enumerate(lines) if is_level_start(l) and l[9:19].strip() == t]
    for i in idx:
        j = i + 1
        while j < len(lines) and not is_level_start(lines[j]) and lines[j].rstrip() != " 34S  d":
            j += 1
        print(f"\n=== level {t} (L line {i + 1}) ===")
        for k in range(i, min(j + 1, len(lines))):
            s = lines[k]
            tag = ""
            if len(s) > 7 and s[7] == "L" and s[5] == " ":
                tag = f" J=[{s[22:39]}]"
            if len(s) > 7 and s[7] == "G":
                tag = f" M=[{s[32:41]}]"
            print(f"{k + 1:5d} len={len(s):3d} clen={len(s.rstrip()):3d}{tag} {s.rstrip()!r}")

print("\n=== summary ===")
bad = [(i, len(s)) for i, s in enumerate(lines, 1) if len(s) != 80]
print(f"lines with len != 80: {len(bad)}")
for i, n in bad:
    print(f"  {i:5d} len={n:3d} {lines[i - 1].rstrip()!r}")

print(f"total lines: {len(lines)}")
for kw in ["cG M$from |g(|q) and azimuthal asymmetry", "cL J$spin=1 from |g(|q)", "M1"]:
    cnt = sum(1 for s in lines if kw in s)
    print(f"occurrences of {kw!r}: {cnt}")
