"""Read-only: enumerate every WIDTHG0 record, its parent L record fields, and existing |G-g0 comments."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

def is_level_start(s):
    return len(s) > 19 and s[5] == " " and s[6] == " " and s[7] == "L"

def block_end(j):
    k = j + 1
    while k < len(lines) and not is_level_start(lines[k]) and lines[k].rstrip() != " 34S  d":
        k += 1
    return k

hits = [(i, s) for i, s in enumerate(lines) if "WIDTHG0" in s]
print(f"TOTAL WIDTHG0 lines: {len(hits)}\n")

for i, s in hits:
    j = i - 1
    while j >= 0 and not is_level_start(lines[j]):
        j -= 1
    L = lines[j]
    end = block_end(j)
    has_cmt = [k for k in range(j + 1, end) if "|G{-|g0}" in lines[k]]
    print(f"WIDTHG0 line {i + 1}: len={len(s)} {s.rstrip()!r}")
    print(f"    L line {j + 1}: len={len(L)} E={L[9:19].strip()} J=[{L[22:39]}] T=[{L[39:49]}] DT=[{L[49:55]}]")
    print(f"    L content: {L.rstrip()!r}")
    print(f"    existing |G-g0 comment line(s): {[x + 1 for x in has_cmt]}")
    print(f"    record type col6={s[5]!r} col7={s[6]!r} col8={s[7]!r}")

print("\n--- other WIDTH variants (context only) ---")
for i, s in enumerate(lines, 1):
    if "WIDTH" in s and "WIDTHG0" not in s:
        print(f"{i:5d} {s.rstrip()!r}")

print("\n--- all non-80-char lines ---")
bad = [(i, len(s)) for i, s in enumerate(lines, 1) if len(s) != 80]
print(f"count={len(bad)}")
for i, n in bad:
    print(f"  {i:5d} len={n:3d} {lines[i - 1].rstrip()!r}")
