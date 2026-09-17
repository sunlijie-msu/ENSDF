"""Exact tail structure of the 8 flagged-in-error lines and 10430/10800/11350/11500."""
P = r"A34/S34/new/S34_adopted.ens"
lines = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
probe = [(1084, "10097"), (1089, "10140"), (1111, "10201"), (1119, "10236"),
         (1168, "10447"), (1183, "10528"), (1195, "10617"), (1276, "10869")]
for n, tag in probe:
    ln = lines[n - 1]
    if "A" in ln:
        ai = ln.index("A", 60)
        before = len(ln[:ai].rstrip())  # content end
        sp_before = ai - before
        sp_after = len(ln) - ai - 1
    else:
        ai = -1
        sp_before = sp_after = -1
        before = len(ln.rstrip())
    print(f"{tag:7s} line {n:5d} len={len(ln)} content_end={before} "
          f"Apos={ai+1 if ai>=0 else '-'} sp_before_A={sp_before} sp_after_A={sp_after}")
    print("   ", repr(ln))
for n, tag in [(1187, "10430"), (1246, "10800"), (1401, "11350"), (1530, "11500")]:
    ln = lines[n - 1]
    print(f"{tag:7s} line {n:5d} len={len(ln)} content_end={len(ln.rstrip())} tail={repr(ln[70:])}")
    print("   ", repr(ln))
