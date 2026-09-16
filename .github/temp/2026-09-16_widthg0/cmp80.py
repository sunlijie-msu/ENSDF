"""Compare non-80-char line inventory between HEAD baseline and working file."""
from pathlib import Path

base = Path(".github/temp/2026-09-16_widthg0/baseline_head.ens").read_text(encoding="utf-16").splitlines()
work = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()


def bad(lines):
    return [(i, len(s)) for i, s in enumerate(lines, 1) if len(s) != 80]


b, w = bad(base), bad(work)
print(f"HEAD baseline lines={len(base)}  non-80 = {len(b)}")
for i, n in b:
    print(f"   {i:5d} len={n}")
print(f"\nWORKING lines={len(work)}  non-80 = {len(w)}")
for i, n in w:
    print(f"   {i:5d} len={n}")

bs = {len(base[i - 1].rstrip()) for i, _ in b}
ws = {len(work[i - 1].rstrip()) for i, _ in w}
print("\nbaseline content-length multiset:", sorted(bs))
print("working  content-length multiset:", sorted(ws))

print("\n--- logical content comparison of the two non-80 sets ---")
bcont = sorted(base[i - 1].rstrip() for i, _ in b)
wcont = sorted(work[i - 1].rstrip() for i, _ in w)
print("in baseline not in working:")
for c in bcont:
    if c not in wcont:
        print("   ", repr(c))
print("in working not in baseline:")
for c in wcont:
    if c not in bcont:
        print("   ", repr(c))
