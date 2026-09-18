"""Ground-truth measurement of probe1.ens line1 and line2."""
P = r".github/temp/2026-09-17_flagsA/probe1.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
for i, ln in enumerate(lines[:3], 1):
    print(f"line{i}: len={len(ln)}")
    print(f"   repr: {ln!r}")
    for ch in ("X", "A", "5"):
        if ch in ln:
            print(f"   '{ch}' at index {ln.index(ch)} (col {ln.index(ch)+1})")
    nz = [k for k, c in enumerate(ln) if c != " "]
    print(f"   non-space at cols: {[k+1 for k in nz[:12]]}...{([k+1 for k in nz[-4:]])}")
